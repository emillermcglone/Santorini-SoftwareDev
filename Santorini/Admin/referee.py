from Design.referee import Referee
from Common.board import GameBoard
from Common.turn_phase import TurnPhase

from timeout_decorator import timeout, TimeoutError

import copy

class TimeoutWinner(Exception):
    """
    Exceptions to throw when a Player has timed out during their turn.
    """
    def __init__(self, winner):
        """
        Initialize exception.

        :param winner: Player, winner of the game
        """
        self.winner = winner


class SantoriniReferee(Referee):
    def __init__(self, player_1, player_2, checker_cls, board=None):
        """
        initilization setup to hold state

        :param player_1: string, player 1 id
        :param player_2: string, player 2 id

        checker_cls: A Santorini RuleChecker class that is used for logic
        board: A Santorini GameBoard that is used for state lookup
        players: List-of Player IDs
        current_player: player ID of the current player
        current_worker: assigned after a move is done
        cmd_handler: used to dispatch to appropriate function based on incoming action
        """
        self.__original_board = board
        self.__reset()
    
    @property
    def board(self):
        """
        Get deep copy of board.

        :return: GameBoard, copy of board
        """
        return copy.deepcopy(self.__board)


    def run_games(self, best_of=1):
        """
        Run the game between the two players once or as many as the given 
        number of matches. 

        :param best_of: N, odd number of matches at least 1
        :return: string, the id of winner
        """
        if best_of % 2 is 0:
            best_of -= 1

        winners = []
        for i in range(best_of):
            winners.append(self.__run_game(self.__board, self.__checker, self.players))
            self.__reset()

        return max(self.players, key=lambda p: winners.count(p))


    def __reset(self):
        """
        Reset the state of referee to run more games.
        """
        self.__board = board if self.__original_board is not None else GameBoard()
        self.__checker = checker_cls(self.board)
        self.players = [Player(player_1, self.__checker), Player(player_2, self.__checker)]

    
    def __run_game(self, board, checker, players):
        """
        Run a game of Santorini between given players.

        :param board: GameBoard, board to play with
        :param checker: RuleChecker, rule checker for game
        :param players: [Player, Player], list of players 
        :return: Player, winner of game
        """
        # Placement phase
        try:
            self.__run_init_phase(board, checker, players)
        except TimeoutWinner as e:
            return e.winner

        # Steady phase
        winner = self.__run_steady_phase(board, checker, players)
        winner.game_over("WIN")
        self.__get_opponent_of(winner).game_over("LOSE")
        return winner


    def __run_init_phase(self, board, checker, players):
        """
        Run the initialization phase of a Santorini game.

        :param board: GameBoard, the board the place workers on
        :param checker: RuleChecker, the rule checker for current game
        :param players: [Player, ...], list of players involved in game.
        :raise TimeoutWinner: if a Player has timed out
        """
        worker_id = 0

        while worker_id < 4:
            player = players[worker_id % 2]

            try:
                action = self.__prompt_place(player, worker_id)
            except TimeoutError:
                raise TimeoutWinner(self.__get_opponent_of(player))

            if self.__check_place(action):
                self.__board.place_worker(player.get_id(), worker_id, *action['xy'])


    def __run_steady_phase(self, board, checker, players):
        """
        Run the steady phase of the game by prompting each player for their
        move and build turns.

        :param board: GameBoard, the board to use
        :param checker: RuleChecker, the rule checker for current game
        :param players: [Player, ...], list of players involved in game.
        :return: Player, winner of game
        """
        rounds = 0
        while not self.__is_game_over():
            player = self.players[rounds % 2]

            try:
                move_action = self.__prompt_move(player, worker_id)
                if not self.__check_move(move_action):
                    return self.__get_opponent_of(player)

                self.__board.move_worker(*(move_action['xy1'] + move_action['xy2']))
                worker_id = self.__board.get_worker_id(*move_action['xy1'])

                build_action = self.__prompt_build(player, worker_id)
                if not self.__check_build(build_action):
                    return self.__get_opponent_of(player)

                self.__board.build_floor(*build_action['xy2'])
                rounds += 1
            except TimeoutError:
                raise TimeoutWinner(self.__get_opponent_of(player))
        

    def __is_game_over(self):
        """
        Check if current game is over.

        :return: bool, True if over, False otherwise
        """
        return self.__checker.check_game_over(*self.players)


    def __get_opponent_of(self, player):
        """
        Get opponent of given player.

        :param player: Player, given player
        :return: Player, opponent of given Player
        """

        for p in self.players:
            if p.get_id is not player.get_id:
                return p

    @timeout(10)
    def __prompt_place(self, player, wid):
        """
        Prompt given player for placement.

        :param player: Player, player to prompt
        :param wid: string, worker id 
        :return: PLACE, place specifications
        """
        return player.get_placement(self.board, wid)

    @timeout(10)
    def __prompt_move(self, player, wid):
        """
        Prompt given player for move.

        :param player: Player, player to prompt
        :param wid: string, worker id 
        :return: MOVE, move specification
        """
        return player.get_move(self.board)

    @timeout(10)
    def __prompt_build(self, player, wid):
        """
        Prompt given player for build.

        :param player: Player, player to prompt
        :param wid: string, worker id 
        :return: BUILD, build specifications
        """
        return player.get_build(self.board, wid)

    def check(self, action):
        """
        Method to check if a given action is valid

        :param action:  JSON representing an action
        :return: Boolean representing whether the action was valid or not
        """
        action_type = action['type']

        check_methods = {
            "place": self.__checker.check_place,
            "move": self.__checker.check_move,
            "build": self.__checker.check_build
        }

        return check_methods[action_type](action)
    
    def __check_place(self, action):
        """
        Check if given place action is valid.

        :param action: PLACE, place specifications
        :return: bool, True if valid, False otherwise
        """
        worker = action['wid']
        xy = tuple(action['xy'])
        return self.__checker.check_place(self.__current_player, worker, *xy)

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

