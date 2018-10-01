""" 
Common data and knowledge among administrative components and players
in a Santorini game.

Common data include physical game pieces, the rules of the game,
and the player interface.

N is a natural number. 
"""

from abc import ABC, abstractmethod
from enum import Enum

class Cell(ABC):
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
        self.height = height

    @property
    def height(self):
        """
        Height of cell.
        """
        return self._height

    @height.setter
    def height(self, new_height):
        """
        Set cell's height to new_height.

        :param new_height: the new height
        :raise ValueError: if height is not from 0 to 4
        """
        if new_height < 0 or new_height > 4:
            raise ValueError("New height must be between 0 and 4 inclusive")
        self._height = new_height

class Height(Cell):
    """
    Height of a building.
    """

    def __init__(self, height = 0):
        """
        Initialize with height of building.

        :param height: N, height of building, defaults to 0
        :raise ValueError: if height is not from 0 to 4
        """
        super().__init__(height)
        

class Worker(Cell):
    """
    Worker of a Santorini board whose height represents which floor
    it is on.
    """

    def __init__(self, worker_id, position = None, height = 0):
        """
        Initialize with id, position, and height of building the worker is on.

        :param worker_id: N, id of Worker
        :param position: (N, N), the position of Worker
        :param height: N, height of building worker is on, defaults to 0
        :raise ValueError: if height is not from 0 to 4        
        """
        super().__init__(height)
        self.id = worker_id
        self.position = position


class Rules():
    """
    Set of rules for a Santorini game which both the administrative components
    and players can use to validate their moves before making them.
    """
    
    def __init__(self, move_rules, build_rules):
        """
        Initalize with list of Rule for both moving and building. 
        Rule is a function (board: [[Cell, ...] ...], worker: N, direction: Direction) -> bool
  
        :param move_rules: [Rule, ...], list of rules for move
        :param build_rules: [Rule, ...], list of rules for build
        """
        self.move_rules = move_rules
        self.build_rules = build_rules

    def check_move(self, board, worker, move_direction):
        """
        Check if the move is valid.

        :param board: [[Cell, ...] ...], zero-indexed 2D list of Cells
        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        return all(map(lambda f: f(board, worker, move_direction), self.move_rules))

    def check_build(self, board, worker, build_direction):
        """
        Check if the build is valid.

        :param board: [[Cell, ...] ...], zero-indexed 2D list of Cells
        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        return all(map(lambda f: f(board, worker, build_direction), self.build_rules))

class Player(ABC):
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
    def place_worker(self, board):
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

    def compose(direction1, direction2):
        def go(x, y):
            i, j = direction1(x, y)
            return direction2(i, j)

        return go