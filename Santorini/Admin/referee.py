import sys, copy

from Design.referee import Referee
from Common.board import GameBoard
from Common.turn_phase import TurnPhase
from Common.rule_checker import RuleChecker
from Lib.continuous_iterator import ContinuousIterator
from Admin.game_over import GameOver, GameOverCondition

from timeout_decorator import timeout, TimeoutError


class BreakingPlayer(Exception):
    """
    Error for when player breaks.
    """

    def __init__(self, player, condition):
        """
        :param player: Player, player who breaks
        :param condition: GameOverCondition, condition for breaking
        """
        self.player = player
        self.condition = condition


class SantoriniReferee(Referee):
    """
    The Referee runs a game of Santorini between two players. It prompts players for their
    turn specifications, and execute turn specifications if valid. In case of timeout
    or invalid action, the opponent is deemed winner automatically. 
    """

    def __init__(self, player_1, player_2, checker_cls=RuleChecker, observers=[]):
        """
        Initialize Referee.

        players take turns making the first move after every game, starting with player_1 

        :param player_1: Player, player 1
        :param player_2: Player, player 2
        :param checker_cls: RuleChecker, class to instantiate rule checker from
                            use standard Santorini rule checker as default
        :param board: GameBoard, board to instantiate from if given
        :raise ValueError: if players are the same
        """
        if player_1 == player_2:
            raise ValueError("Players cannot be the same")

        self.__checker_cls = checker_cls
        self.players = [player_1, player_2]
        self.__init_board_and_checker()

        self.observers = observers
        self.__turn_history = []

    
    def add_observer(self, observer):
        """
        Add another observer.

        :param observer: Observer, observer of series of games.
        """
        self.observers.append(observer)


    def __update_state_observers(self, board):
        """
        Update observers about state of game.

        :param board: GameBoard, state of game
        """
        for observer in self.observers:
            observer.update_state_of_game(board)

    def __update_action_observers(self, wid, move_action, build_action):
        """
        Update observers about recent action.

        :param wid: string, worker id
        :param move_action: Action, move specification
        :param build_action: Action, build specification
        """
        for observer in self.observers:
            observer.update_action(wid, move_action, build_action)
            observer.update_state_of_game(self.__board)


    def __give_up_observers(self, pid):
        """
        Update observers about player who gives up.

        :param pid: string, id of player
        """
        for observer in self.observers:
            observer.give_up(pid)

    def __error_observers(self, pid, message):
        """
        Update observers about player error.

        :param pid: string, player id
        :param message: string, error message
        """
        for observer in self.observers:
            observer.error(pid, message)

    def __game_over_observers(self, pid, wid, move_action):
        """
        Update observers about game over.

        :param pid: string, winner id
        :param wid: string, winning move worker id
        :param move_action: Action, winning move action
        """
        for observer in self.observers:
            observer.game_over(pid, wid, move_action)


    def __init_board_and_checker(self):
        """ 
        Initialize board with copy of originally given board, and
        checker with originally given checker class.
        """
        self.__board = GameBoard()
        self.__checker = self.__checker_cls(self.__board)


    def __reset(self):
        """
        Reset board and checker, and reverse order of players. 
        """
        self.__init_board_and_checker()
        self.players = self.players[::-1] 

    
    @property
    def board(self):
        """
        Get deep copy of board.

        :return: GameBoard, copy of board
        """
        return copy.deepcopy(self.__board)


    @property
    def __players_iter(self):
        """
        Get continuous iterator of players.

        :return: iterator, continuous iterator of players
        """
        return iter(ContinuousIterator(self.players))


    def run_games(self, best_of=1):
        """
        Run the game between the two players once or as many as the given 
        number of matches. If best_of is even, Referee adds 1 more match. 

        :param best_of: N, odd number of matches at least 1
        :return: GameOver, the game over state
        """
        if best_of % 2 is 0:
            best_of += 1

        game_outcomes = []

        for _ in range(best_of):
            game_over = self.__run_game(self.__board, self.__checker, self.players)
            if game_over.condition is not GameOverCondition.FairGame:
                return game_over 
            game_outcomes.append(game_over)   
        
        winners = list(map(lambda game: game.winner, game_outcomes))
        overall_winner = max(self.players, key=lambda p: winners.count(p))
        loser = self.__opponent_of(overall_winner)
        return GameOver(overall_winner, loser, GameOverCondition.FairGame)

    
    def __run_game(self, board, checker, players):
        """
        Run a game of Santorini between given players and reset the
        Referee after running game.

        :param board: GameBoard, board to play with
        :param checker: RuleChecker, rule checker for game
        :param players: [Player, Player], list of players 
        :return: Player, winner of game
        """
        winner = None
        loser = None
        condition = GameOverCondition.FairGame

        try:
            # Init: placement
            self.__run_init_phase(board, checker, players)
            self.__update_state_observers(board)

            # Steady: move and build
            winner = self.__run_steady_phase(board, checker, players)
            loser = self.__opponent_of(winner)

        except BreakingPlayer as e:
            loser = e.player
            winner = self.__opponent_of(loser)
            condition = e.condition

            self.__error_observers(loser.get_id(), condition)

        # Notify players game has ended
        self.__game_over_players(winner, loser)
        # self.__game_over_observers(
        self.__reset()
        return GameOver(winner, loser, condition)


    def __game_over_players(self, winner, loser):
        """
        Notify winner and loser of game over.

        :param winner: Player, winner of game
        :param loser: Player, loser of game
        """
        self.__game_over_player(winner, "WIN")
        self.__game_over_player(loser, "LOSE")


    def __game_over_player(self, player, message):
        """
        Notify player of game over with message.

        :param player: Player, player to notify
        :param message: string, message to send
        :raise BreakingPlayer: if player times out
        """
        try:
            timeout(10)(player.game_over)(message)
        except TimeoutError:
            raise BreakingPlayer(player, GameOverCondition.Timeout)


    def __run_init_phase(self, board, checker, players):
        """
        Run the initialization phase of a Santorini game, placing four workers
        on the board, two for each player. 

        :param board: GameBoard, the board to place workers on
        :param checker: RuleChecker, the rule checker for current game
        :param players: [Player, ...], list of players involved in game.
        :raise TimeoutOrInvalidActionWinner: if a player times out or makes an invalid action
        """

        for player, wid in zip(self.__players_iter, [0, 0, 1, 1]):
            self.__prompt_and_act(TurnPhase.PLACE, player, wid)


    def __run_steady_phase(self, board, checker, players):
        """
        Run the steady phase of the game by prompting each player for their
        move and build turns.

        :param board: GameBoard, the board to use
        :param checker: RuleChecker, the rule checker for current game
        :param players: [Player, ...], list of players involved in game.
        :return: Player, winner of game
        :raise TimeoutOrInvalidActionWinner: if a player times out or makes an invalid action
        """

        for player in self.__players_iter: 
            if self.__is_game_over() is not None:
                winner_id = self.__is_game_over()
                winning_move = self.__checker.get_winning_move(winner_id)

                if winning_move is None:
                    self.__give_up_observers(self.__opponent_of(self.__get_player_from_id(winner_id)))
                else:
                    worker_id = self.__board.get_worker_id(*winning_move['xy1'])
                    self.__game_over_observers(winner_id, worker_id, winning_move)

                return self.__get_player_from_id(self.__is_game_over())

            wid = self.__prompt_and_act(TurnPhase.MOVE, player)
            self.__prompt_and_act(TurnPhase.BUILD, player, wid)


    def __get_player_from_id(self, player_id):
        """
        Get player from id.

        :param player_id: id of player
        :return: Player, player
        """
        for p in self.players:
            if p.get_id() is player_id:
                return p

    

    def __prompt_and_act(self, turn_phase, player, wid=None):
        """
        Prompt player for placement and make placement on board.

        :param player: Player, player to prompt
        :param wid: string, id of worker to place
        :raise TimeoutOrInvalidActionWinner: if player times out or makes an invalid move
        :return: string, id of worker moved only if turn_phase is TurnPhase.MOVE
        """
        try: 
            action = self.__prompt(turn_phase, player, wid)
            if not self.check(player, action):
                raise BreakingPlayer(player, GameOverCondition.InvalidAction)
            self.__act(player, action)

            self.__turn_history.append(action)

            if turn_phase is TurnPhase.BUILD:
                self.__update_action_observers(wid, self.__turn_history[-2], self.__turn_history[-1])

            if turn_phase is TurnPhase.MOVE:
                return self.__board.get_worker_id(*action['xy2'])

        except TimeoutError:
            raise BreakingPlayer(player, GameOverCondition.Timeout)


    def __act(self, player, action):
        """
        Act on given action by player.

        :param player: Player, player that acts
        :param action: Action, action made by player
        """
        action_type = action['type']

        if action_type is "place":
            self.__board.place_worker(player.get_id(), action['wid'], *action['xy'])
        elif action_type is "move":
            self.__board.move_worker(*(action['xy1'] + action['xy2']))
        else:
            self.__board.build_floor(*action['xy2'])


    def __is_game_over(self):
        """
        Check if current game is over.

        :return: string | None, id of winner, else None
        """
        return self.__checker.check_game_over(*self.players)


    def __opponent_of(self, player):
        """
        Get opponent of given player.

        :param player: Player, given player
        :return: Player, opponent of given Player
        """
        for p in self.players:
            if p.get_id() is not player.get_id():
                return p


    @timeout(10)
    def __prompt(self, turn_phase, player, wid=None):
        """
        Prompt the given player for their turn specifications.

        :param turn_phase: TurnPhase, the type of turn
        :param player: Player, the player to prompt
        :param wid: string, id of worker if given
        :return: Action, action specifications
        """

        prompt_methods = {
            TurnPhase.PLACE: lambda p: self.__prompt_place(p, wid),
            TurnPhase.MOVE: self.__prompt_move,
            TurnPhase.BUILD: lambda p: self.__prompt_build(p, wid),
        }

        return prompt_methods[turn_phase](player)


    def __prompt_place(self, player, wid):
        """
        Prompt given player for placement.

        :param player: Player, player to prompt
        :param wid: string, worker id 
        :return: PLACE, place specifications
        """
        return player.get_placement(self.board, wid, self.__checker)


    def __prompt_move(self, player):
        """
        Prompt given player for move.

        :param player: Player, player to prompt
        :return: MOVE, move specification
        """
        return player.get_move(self.board, self.__checker)


    def __prompt_build(self, player, wid):
        """
        Prompt given player for build.

        :param player: Player, player to prompt
        :param wid: string, worker id 
        :return: BUILD, build specifications
        """
        return player.get_build(self.board, wid, self.__checker)


    def check(self, player, action):
        """
        Method to check if a given action is valid

        :param action: Action, the action to check
        :param player: Player, the player to check 
        :return: bool, True if action is valid, False otherwise
        """
        action_type = action['type']

        check_methods = {
            "place": lambda a: self.__check_place(player.get_id(), a),
            "move": self.__check_move,
            "build": self.__check_build
        }

        try:
            return check_methods[action_type](action)
        except KeyError:
            return False

    
    def __check_place(self, pid, action):
        """
        Check if given place action is valid.

        :param action: PLACE, place specifications
        :param pid: N, the id of the player to check 
        :return: bool, True if valid, False otherwise
        """
        worker = action['wid']
        xy = action['xy']
        return self.__checker.check_place(pid, worker, *xy)


    def __check_move(self, action):
        """
        Check if given move action is valid.

        :param action: MOVE, move specifications
        :return: bool, True if valid, False otherwise
        """
        args = action['xy1'] + action['xy2']
        return self.__checker.check_move(*args)


    def __check_build(self, action):
        """
        Check if given build action is valid.

        :param action: BUILD, build specifications
        :return: bool, True if valid, False otherwise
        """
        args = action['xy1'] + action['xy2']
        return self.__checker.check_build(*args)

