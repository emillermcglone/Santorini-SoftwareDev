import copy

from Admin.board import GameBoard
from Admin.rule_checker import RuleChecker
from Admin.broken_player import BrokenPlayer
from Admin.game_over import GameOver, GameOverCondition
from Admin.player import GuardedPlayer
from Admin.observer_manager import ObserverManager
from Admin.constants import *
from Common.turn_phase import TurnPhase
from Common.exception import *
from Lib.continuous_iterator import ContinuousIterator

from timeout_decorator import timeout, TimeoutError


class Referee:
    """
    The Referee runs a game of Santorini between two players. It prompts players for their
    turn specifications, and execute turn specifications if valid. In case of timeout
    or invalid action, the opponent is deemed winner automatically. 
    """

    def __init__(self, player_1, player_2, observers=[], time_limit=10, checker_cls=RuleChecker):
        """
        Initialize Referee.

        players take turns making the first move after every game, starting with player_1 

        :param player_1: Player, player 1
        :param player_2: Player, player 2
        :param checker_cls: RuleChecker, class to instantiate rule checker from
                            use standard Santorini rule checker as default
        :param observers: [Observer, ...], list of observers for game
        :raise ValueError: if players are the same
        """
        if player_1.get_id() is player_2.get_id():
            raise ValueError("Players cannot be the same")

        self.__players = [GuardedPlayer(player_1), GuardedPlayer(player_2)]

        self.__time_limit = time_limit
        self.__checker_cls = checker_cls
        self.__init_board_and_checker()

        self.__obs_manager = ObserverManager(observers, self.__board)


    @property
    def players(self):
        """
        Get Player objects from internal guarded players. 

        :return: [Player, ...], original Player objects
        """
        return copy.deepcopy(list(map(lambda p: p.player, self.__players)))
    

    @property
    def board(self):
        """
        Get deep copy of board.

        :return: GameBoard, copy of board
        """
        return copy.deepcopy(self.__board)

    
    @property
    def observers(self):
        """
        Get all observers of this match.

        :return: [Observer, ...], list of observers
        """
        return self.__obs_manager.observers

    
    def add_observer(self, observer):
        """
        Add another observer.

        :param observer: Observer, observer of series of games.
        """
        self.__obs_manager.add_observer(observer)


    def run_games(self, best_of=1):
        """
        Run the game between the two players once or as many as the given 
        number of matches. If best_of is even, Referee adds 1 more match. 

        :param best_of: N, odd number of matches at least 1
        :return: GameOver, the game over state
        """
        if best_of % 2 is 0:
            best_of += 1

        winners = []

        for _ in range(best_of):
            game_over = self.__run_game(self.__board, self.__checker, self.__players)
            if game_over.condition is not GameOverCondition.FairGame:
                return game_over 
            winners.append(game_over.winner)   
        
        overall_winner = max(self.__players, key=lambda p: winners.count(p))
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
        winner = loser = None
        condition = GameOverCondition.FairGame

        try:
            # Init: placement
            self.__run_init_phase(board, checker, players)
            self.__obs_manager.update_state(board)

            # Steady: move and build
            game_over = self.__run_steady_phase(board, checker, players)
            winner = game_over.winner
            loser = game_over.loser

        except BrokenPlayer as e:
            winner, loser, condition = self.__winner_loser_condition_from(e)
            self.__obs_manager.error(loser.get_id(), condition)

        # Game Over: notify players of game over
        self.__game_over_players(winner, loser)
        self.__reset()
        return GameOver(winner, loser, condition)


    def __winner_loser_condition_from(self, broken_player):
        """
        Get winner, loser, and condition of game over from BrokenPlayer exception.

        :param broken_player: BrokenPlayer, broken player exception
        :return: (Player, Player, GameOverCondition) , winner, loesr and game over condition
        """
        loser = broken_player.player
        winner = self.__opponent_of(loser)
        condition = broken_player.condition

        return winner, loser, condition


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
            self.__prompt_act_raise(TurnPhase.PLACE, player, wid)


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
            try:
                move_action = self.__prompt_act_raise(TurnPhase.MOVE, player)
                wid = self.__board.get_worker_id(*move_action['xy2'])
                self.__prompt_act_raise(TurnPhase.BUILD, player, wid)
            except GameOver as e:
                return e


    def __prompt_act_raise(self, turn_phase, player, wid=None):
        """
        Prompt player for action, make the action, and raise game over
        state if game is over after move.

        :param turn_phase: TurnPhase, the phase in the game
        :param player: Player, player to prompt
        :param wid: string, id of worker to place
        :raise BrokenPlayer: if player times out, makes an invalid move, or crashes
        :raise GameOver: if game is over after action
        :return: string, id of worker moved only if turn_phase is TurnPhase.MOVE
        """
        try: 
            # Get action from player and impose time out
            action = timeout(self.__time_limit)(self.__prompt)(turn_phase, player, wid)
            self.__act(turn_phase, player, action)

        # Timeout error
        except TimeoutError:
            raise BrokenPlayer(player, GameOverCondition.Timeout)

        # Illegal action by player
        except IllegalActionException:
            raise BrokenPlayer(player, GameOverCondition.InvalidAction)

        # Player breaks in any way
        except:
            raise BrokenPlayer(player, GameOverCondition.Crash)

        self.__raise_game_over()
        return action


    def __act(self, turn_phase, player, action):
        """
        Act on given action by player.

        :param player: Player, player that acts
        :param action: Action, action made by player
        """
        action_methods = {
            TurnPhase.PLACE: self.__act_place,
            TurnPhase.MOVE: self.__act_move,
            TurnPhase.BUILD: self.__act_build
        }

        try:
            action_methods[turn_phase](player, action)
        except KeyError:
            raise IllegalActionException()


    def __act_place(self, player, action):
        """
        Act on the given place action for player.

        :param player: Player, player that acts
        :param action: PLACE, place action made by player
        """
        # Invalid place action by player
        if not self.__check(TurnPhase.PLACE, player, action):
            raise IllegalPlaceException()

        self.__board.place_worker(player.get_id(), action['wid'], *action['xy'])


    def __act_move(self, player, action):
        """
        Act on the given move action for player.

        :param player: Player, player that acts
        :param action: MOVE, move action made by player
        """
        # Invalid move action by player
        if not self.__check(TurnPhase.MOVE, player, action):
            raise IllegalMoveException()

        self.__board.move_worker(*(action['xy1'] + action['xy2']))


    def __act_build(self, player, action):
        """
        Act on the given build action for player.

        :param player: Player, player that acts
        :param action: BUILD, build action made by player
        """
        # Invalid build action by player
        if not self.__check(TurnPhase.BUILD, player, action):
            raise IllegalBuildException()

        self.__board.build_floor(*action['xy2'])
        self.__obs_manager.update_action(player, self.__board)


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


    def __get_turn_phase(self, phase_str):
        """
        Get TurnPhase from phase string.

        :param phase_str: string, phase in string
        :return: TurnPhase, the turn phase
        """
        phases = {
            "place": TurnPhase.PLACE,
            "move": TurnPhase.MOVE,
            "build": TurnPhase.BUILD,
        }

        return phases[phase_str]


    def __check(self, turn_phase, player, action):
        """
        Method to check if a given action is valid

        :param turn_phase: TurnPhase, the turn phase
        :param action: Action, the action to check
        :param player: Player, the player to check 
        :param wid: string, the worker id
        :return: bool, True if action is valid, False otherwise
        """

        check_methods = {
            TurnPhase.PLACE: lambda a: self.__check_place(player.get_id(), a),
            TurnPhase.MOVE: self.__check_move,
            TurnPhase.BUILD: self.__check_build
        }

        try:
            action_type = self.__get_turn_phase(action['type'])
            return action_type is turn_phase and check_methods[action_type](action)
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

        :param pid: string, player id
        :param action: MOVE, move specifications
        :return: bool, True if valid, False otherwise
        """
        args = action['xy1'] + action['xy2']
        return self.__checker.check_move(*args)


    def __check_build(self, action):
        """
        Check if given build action is valid.

        :param pid: string, player id
        :param wid: string, worker id that moved 
        :param action: BUILD, build specifications
        :return: bool, True if valid, False otherwise
        """
        args = action['xy1'] + action['xy2']
        return self.__checker.check_build(*args)


    def __game_over_players(self, winner, loser):
        """
        Notify winner and loser of game over.

        :param winner: Player, winner of game
        :param loser: Player, loser of game
        """
        self.__game_over_player(winner, WIN_MESSAGE)
        self.__game_over_player(loser, LOSE_MESSAGE)


    def __game_over_player(self, player, message):
        """
        Notify player of game over with message.

        :param player: Player, player to notify
        :param message: string, message to send
        :raise BrokenPlayer: if player times out
        """
        try:
            timeout(self.__time_limit)(player.game_over)(message)
        except TimeoutError:
            pass


    def __get_player_from_id(self, player_id):
        """
        Get player from id.

        :param player_id: id of player
        :return: Player, player
        """
        for p in self.__players:
            if p.get_id() is player_id:
                return p

    
    def __raise_game_over(self):
        """
        Raise GameOver state if game is over.

        :raise GameOver: if game is over
        """
        if self.__is_game_over() is not None:
            winner_id = self.__is_game_over()
            winner = self.__get_player_from_id(winner_id)
            loser = self.__opponent_of(winner)
            self.__obs_manager.game_over(winner)
            raise GameOver(winner, loser, GameOverCondition.FairGame)


    def __is_game_over(self):
        """
        Check if current game is over.

        :return: string | None, id of winner, else None
        """
        player_ids = list(map(lambda p: p.get_id(), self.__players))
        return self.__checker.check_game_over(*player_ids)


    @property
    def __players_iter(self):
        """
        Get continuous iterator of players.

        :return: iterator, continuous iterator of players
        """
        return iter(ContinuousIterator(self.__players))


    def __opponent_of(self, player):
        """
        Get opponent of given player.

        :param player: Player, given player
        :return: Player, opponent of given Player
        """
        for p in self.__players:
            if p.get_id() is not player.get_id():
                return p



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
        self.__players = self.__players[::-1] 

