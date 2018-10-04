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
    
    @abstractmethod
    def __init__(self, height = 0):
        """
        Initialize cell with height, defaults to 0.

        :param height: 0 to 4 inclusive
        :raise ValueError: height is not between 0 and 4 inclusive        
        """
        pass

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
        Set cell's height to new_height.

        :param new_height: the new height
        :raise ValueError: if height is not from 0 to 4
        """
        pass

class IRules(ABC):
    """
    Set of rules for a Santorini game which both the administrative components
    and players can use to validate their moves before making them.
    """
    @abstractmethod
    def __init__(self, move_rules, build_rules):
        """
        Initalize with list of Rule for both moving and building. 
        Rule is a function (board: [[Cell, ...] ...], worker: N, direction: Direction) -> bool
  
        :param move_rules: [Rule, ...], list of rules for move
        :param build_rules: [Rule, ...], list of rules for build
        """
        pass

    @abstractmethod
    def check_move(self, board, worker, move_direction):
        """
        Check if the move is valid.

        :param board: [[Cell, ...] ...], zero-indexed 2D list of Cells
        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        pass


    @abstractmethod
    def check_build(self, board, worker, build_direction):
        """
        Check if the build is valid.

        :param board: [[Cell, ...] ...], zero-indexed 2D list of Cells
        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        pass


class IPlayer(ABC):
    """
    Player component for Santorini, and intermediary between administrative
    components and the player AI.
    """

    @abstractmethod
    def __init__(self, id, worker1_id, worker2_id):
        """"
        Initialize the Player with id, worker1_id, and worker2_id.

        :param id: N, id of Player
        :param worker1_id: N, the id of the Player's first worker 
        :param worker2_id: N, the id of the Player's second worker
        """
        pass

    @abstractmethod
    def prompt_place_worker(self, board):
        """
        Provide coordinates to place one of the workers on the given board.

        :param board: [[Cell, ...], ...], the current board of the game
        :return: (N, (N, N)), the worker id, and the x and y coordinates
        """
        pass

    @abstractmethod
    def prompt_move(self, board, worker1, worker2):
        """
        Prompt the player for their move turn. 

        :param board: [[Cell, ...], ...], the current board of the game
        :param worker1: Worker, the first worker
        :param worker2: Worker, the second worker
        :return: (N, Direction), the worker id, move direction
        """
        pass

    @abstractmethod
    def prompt_build(self, board, worker):
        """
        Prompt the player for their build turn. 

        :param board: [[Cell, ...], ...], the current board of the game
        :param worker: Worker, the worker that was moved in that turn
        :return: Direction, build direction
        """
        pass

    @abstractmethod
    def game_over(self, win):
        """
        Notify player that game has ended either by victory on either side or by
        player shutdown due to invalid move/build or connection lost.

        :param win: bool, True if this Player won the game, False otherwise
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