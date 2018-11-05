from Player.test_strategy_place2 import Strategy as PlaceFurthestStrategy
from Player.test_strategy_place1 import Strategy as PlaceDiagonalStrategy
from Player.test_strategy_alive import Strategy as StayAliveStrategy
from Lib.util import gen_moves, gen_builds

from Design.player import Player as IPlayer

class InfiniteLoopPlayer(IPlayer):
    """
    Class representing a Player that will go on an infinite loop on its third move.
    """

    def __init__(self, player_id):
        """
        Initialize the Player object

        :param player_id: Unique ID for the Player
        """
        self.__player_id = player_id
        self.__count = 0

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.get_id() is other.get_id()


    def get_id(self):
        """
        Getter for the Player's ID

        :return: String Player ID
        """
        return self.__player_id


    def get_placement(self, board, wid, rule_checker):
        """
        Asks the player to place a worker on the board

        :param board: GameBoard, copy of the current state of the game
        :param wid: The ID of the worker the player is to place

        :return: JSON that represents a place_worker action
        """
        place_diagonal_strategy = PlaceDiagonalStrategy(self.__player_id, rule_checker, board)
        
        to_xy = place_diagonal_strategy.decide_place(wid)
        return { 'type': 'place', 'wid': wid, 'xy': list(to_xy) }


    def get_move(self, board, rule_checker):
        """
        Asks the player to make a move.

        On the third move, go on an infinite loop. Otherwise, make a random move

        :param board: GameBoard, copy of the current state of the game
        :return: JSON that represents a move action
        """
        if self.__count is 2:
            while True:
                pass

        self.__count += 1

        moves = gen_moves(self.__player_id, board, rule_checker)
        for i in moves:
            return i
        

    def get_build(self, board, wid, rule_checker):
        """
        Asks the player to build a floor

        :param board: GameBoard, copy of the current state of the game
        :param wid: Worker ID of the worker that the player needs to build with

        :return: Json that represents a build action
        """
        worker_position = board.find_worker(self.__player_id, wid)
        builds = gen_builds(self.__player_id, worker_position, board, rule_checker)
        for i in builds:
            return i
        

    def game_over(self, status):
        """
        Alerts the player that the game is over with status

        :param status: one of "WIN" | "LOSE" depending on the outcome of the board
        """
        pass
