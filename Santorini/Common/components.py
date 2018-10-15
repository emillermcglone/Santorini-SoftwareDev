""" 
Common data and knowledge among administrative components and players
in a Santorini game.

Common data include physical game pieces, the rules of the game,
and the player interface.

N is a natural number. 
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from enum import Enum

class ICell(ABC):
    """
    Individual cell element with height on a Santorini board.
    """

    @property
    @abstractmethod
    def height(self):
        """
        Height of cell.
        """
        pass

    @height.setter
    @abstractmethod
    def height(self, new_height):
        """
        Set cell's height to new height.

        :param new_height: the new height
        :raise ValueError: if given height is less than 0
        """
        pass

class IRules(ABC):
    """
    Set of rules for a Santorini game which both the administrative components
    and players can use to validate their moves before making them.
    """

    @property
    @abstractmethod
    def max_height(self):
        """ N, maximum height of each building """
        pass

    @property
    @abstractmethod
    def height_to_win(self):
        """ N, height of worker to win the game """
        pass

    @property
    @abstractmethod
    def max_height_difference(self):
        """ N, maximum height difference to climb onto buildings """
        pass

    @property
    @abstractmethod
    def max_workers_per_player(self):
        """ N, maximum workers per player """
        pass

    @property
    @abstractmethod
    def max_workers(self):
        """ N, maximum workers in a game """
        pass

    @abstractmethod
    def check_place(self, x, y):
        """
        Check if place request is valid.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: bool, True if valid, False otherwise
        """
        pass


    @abstractmethod
    def check_move(self, worker, move_direction):
        """
        Check if the move is valid.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        :return, bool, True if valid, False otherwise
        """
        pass


    @abstractmethod
    def check_build(self, worker, build_direction):
        """
        Check if the build is valid.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        :return, bool, True if valid, False otherwise
        """
        pass

    @abstractmethod
    def check_move_and_build(self, worker, move_direction, build_direction):
        """
        Check if build after move is valid.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        :param build_direction: Direction, direction for build after move
        :return, bool, True if valid, False otherwise
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        Check if game has ended.

        :return: N, id of player who won, -1 if game has not ended.
        """
        pass



class Direction(Enum):
    """
    Direction for moving or building in a zero-indexed 2D list of Cell where
    origin is on the top left corner. Going North means y - 1 and West means x - 1.
    Each Enum maps to a function of type (x, y: (N, N)) -> (N, N) that gives the next
    coordinates in its direction.
    """
    N = lambda x, y: (x, y - 1)
    S = lambda x, y: (x, y + 1)
    W = lambda x, y: (x - 1, y)
    E = lambda x, y: (x + 1, y)
    NW = lambda x, y: (x - 1, y - 1)
    NE = lambda x, y: (x + 1, y - 1)
    SW = lambda x, y: (x - 1, y + 1)
    SE = lambda x, y: (x + 1, y + 1)

    @staticmethod
    def compose(direction_1, direction_2):
        """
        Composes two direction functions.

        :param direction_1: Direction, first direction
        :param direction_2: Direction, second direction
        :return: (int, int) -> (int, int), composed direction function
        """
        def go(x, y):
            i, j = direction_1(x, y)
            return direction_2(i, j)

        return go