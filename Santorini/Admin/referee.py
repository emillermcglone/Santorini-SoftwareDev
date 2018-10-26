import sys
sys.path.append('../')

from Design.referee import Referee
from Common.board import GameBoard
from Common.turn_phase import TurnPhase
from Common.rule_checker import RuleChecker

from timeout_decorator import timeout, TimeoutError

import copy

class TimeoutOrInvalidActionWinner(Exception):
    """ Exceptions to throw when a Player has timed out during their turn. """

    def __init__(self, winner):
        """
        Initialize exception.

        :param winner: Player, winner of the game
        """
        self.winner = winner


class ContinuousIterator:
    """
    Iterable class that loops over list of players continuously. 
    """

    def __init__(self, items):
        """
        Initialize iterable with list of items to loop over. 

        :param items: [Any, ...], list of items to loop over
        """
        self.items = items
        self.index = 0
        self.end = len(items)


    def __iter__(self):
        return self


    def __next__(self):
        """ Iterate continuously """
        if self.end is 0:
            raise StopIteration

        if self.index is self.end:
            self.index = 0

        item = self.items[self.index]
        self.index += 1
        return item


class SantoriniReferee(Referee):
    """
    The Referee runs a game of Santorini between two players. It prompts players for their
    turn specifications, and execute turn specifications if valid. In case of timeout
    or invalid action, the opponent is deemed winner automatically. 
    """


    def __init__(self, player_1, player_2, checker_cls=RuleChecker, board=None):
        """
        Initialize Referee.

        players take turns making the first move after every game, starting with player_1 

        :param player_1: Player, player 1
        :param player_2: Player, player 2
        :param checker_cls: RuleChecker, class to instantiate rule checker from
                            use standard Santorini rule checker as default
        :param board: GameBoard, board to instantiate from if given
        """
        self.__original_board = board
        self.__checker_cls = checker_cls
        self.players = [player_2, player_1]
        self.__reset()


    def __reset(self):
        """
        Reset board with copy of original board and checker with new board instance,
        and reverse player order. 
        """
        self.__board = copy.deepcopy(self.__original_board) or GameBoard()
        self.__checker = self.__checker_cls(self.__board)
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
        :return: string, the id of winner
        """
        if best_of % 2 is 0:
            best_of += 1

        winners = [self.__run_game(self.__board, self.__checker, self.players) for _ in range(best_of)]

        #
        return max(self.players, key=lambda p: winners.count(p)).get_id()

    
    def __run_game(self, board, checker, players):
        """
        Run a game of Santorini between given players and reset the
        Referee after running game.

        :param board: GameBoard, board to play with
        :param checker: RuleChecker, rule checker for game
        :param players: [Player, Player], list of players 
        :return: Player, winner of game
        """

        try:
            # Init: placement
            self.__run_init_phase(board, checker, players)

            # Steady: move and build
            winner = self.__run_steady_phase(board, checker, players)

        except TimeoutOrInvalidActionWinner as e:
            winner = e.winner

        finally:
            opponent = self.__opponent_of(winner)

        try:
            # Shutdown: game over update and reset
            self.__shutdown_players(winner, opponent)

        except TimeoutError:
            # Is there a better way to deal with Timeout rather 
            # than giving up on notifying players?
            pass

        finally:
            self.__reset()
            return winner


    def __shutdown_players(winner, loser):
        """
        Notify winner and loser of game over.

        :param winner: Player, winner of game
        :param loser: Player, loser of game
        """
        winner.game_over("WIN")
        opponent.game_over("LOSE")


    def __run_init_phase(self, board, checker, players):
        """
        Run the initialization phase of a Santorini game, placing four workers
        on the board, two for each player. 

        :param board: GameBoard, the board to place workers on
        :param checker: RuleChecker, the rule checker for current game
        :param players: [Player, ...], list of players involved in game.
        :raise TimeoutOrInvalidActionWinner: if a player times out or makes an invalid action
        """

        # TODO: Replace constant with RuleChecker constant
        for player, wid in zip(self.__players_iter, range(4)):
            self.__prompt_and_act(TurnPhase.PLACE, player, str(wid))


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
                return self.__is_game_over()

            # TODO: Fix getting worker id after move
            wid = self.__prompt_and_act(TurnPhase.MOVE, player)
            self.__prompt_and_act(TurnPhase.BUILD, player, wid)

    

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
                raise TimeoutOrInvalidActionWinner(self.__opponent_of(player))
            self.__act(player, action)

            # if action is move, return id of worker moved
            if turn_phase is TurnPhase.MOVE:
                return self.__board.get_worker_id(*action['xy2'])

        except TimeoutError:
            raise TimeoutOrInvalidActionWinner(self.__opponent_of(player))


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
            self.__board.build_floor(action['xy2'])


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
            if p.get_id is not player.get_id:
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


    # Not sure if this is necessary but it was given in the interface
    def check(self, player, action):
        """
        Method to check if a given action is valid

        :param action: Action, the action to check
        :param player: Player, the player to check 
        :return: bool, True if action is valid, False otherwise
        """
        action_type = action['type']

        # Are dictionary and method currying too complicated?
        # Are if else statements simpler? They're ugly
        check_methods = {
            "place": lambda a: self.__checker.check_place(player.get_id(), a),
            "move": self.__checker.check_move,
            "build": self.__checker.check_build
        }
        try:
            valid = check_methods[action_type](action)
            return valid
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

