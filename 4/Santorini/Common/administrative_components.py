""" 
Common data and knowledge among administrative components and players
in a Santorini game.

Common data include physical game pieces, the rules of the game,
and the player interface.

N is a natural number. 
"""

from abc import ABC, abstractmethod

class Cell(ABC):
    """
    Individual cells on a Santorini board with height attributes.
    """

    @abstractmethod
    def __init__(self, height = 0):
        """
        Initialize the height of building, defaults to 0 

        :param height: N, 0 to 4 inclusive
        :raise AttributeError: if height is not from 0 to 4        
        """
        pass

    @property
    @abstractmethod
    def height(self):
        """
        Height of building.
        """
        pass

    @height.setter
    @abstractmethod
    def height(self, new_height):
        """
        Set Cell's height to new_height.

        :param new_height: the new height of Cell
        :raise AttributeError: if height is not from 0 to 4
        """
        pass

class Height(Cell):
    """
    Height of a building.
    """

    def __init__(self, height = 0):
        """
        Initialize Height with height of building.

        :param height: N, height of building, defaults to 0
        :raise AttributeError: if height is not from 0 to 4
        """
        pass

class Worker(Cell):
    """
    Worker of a Santorini board. It has a height attribute representing which 
    floor it is on.
    """

    def __init__(self, id, position, height = 0):
        """
        Initialize Worker with id, position, and height of building the worker is on.

        :param id: N, id of Worker
        :param position: (N, N), the position of Worker
        :param height: N, height of building worker is on, defaults to 0
        :raise AttributeError: if height is not from 0 to 4        
        """
        pass

class Rules(ABC):
    """
    Set of rules for a Santorini game which both Santorini and players can use
    to validate their moves before making them.
    """
    
    @abstractmethod
    def __init__(self, rules):
        """
        Initalize Rules with list of Rule. 
        Rule is a function (board: [[Cell, ...] ...], worker: N, move_direction: Direction, build_direction: Direction) -> bool
  
        :param rules: [Rule, ...], list of rules for move and build 
        """
        pass

    @abstractmethod
    def check(self, board, worker, move_direction, build_direction):
        """
        Check if the move and build are valid.

        :param board: [[Cell, ...] ...], zero-indexed 2D list of Cells
        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        :param build_direction: Direction, direction for build
        """
        pass


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
    def prompt(self, board, worker1_posn, worker2_posn):
        """
        Prompt the player for their move and build turn. 

        :param board: [[Cell, ...], ...], the current board of the game
        :param worker1_posn: (N, N), position of first worker
        :param worker2_posn: (N, N), position of second worker
        :return: (N, Direction, Direction), the worker id, move direction, and build direction
        """
        pass

    @abstractmethod
    def exception(self, error, board, worker1_posn, worker2_posn):
        """
        Prompt the player for their move and build turn, given that their previous move and build invoked an error.

        :param error: Exception | BuildError, invalid move or build 
        :param board: [[Cell, ...], ...], the current board of the game
        :param worker1_posn: (N, N), position of first worker
        :param worker2_posn: (N, N), position of second worker
        :return: (N, Direction, Direction), the worker id, move direction, and build direction
        """
        pass

    @abstractmethod
    def game_over(self, win):
        """
        Notify player that game has ended.

        :param win: bool, True if this Player won the game, False otherwise
        """
        pass
class PlaceOutOfBounds(Exception):
    """
    The coordinates given to place the worker are out of bounds.
    """
    def __init__(self, message):
        self.message = message

class PlaceBlockingWorker(Exception):
    """
    Another worker on coordinates.
    """
    def __init__(self, message):
        self.message = message

class MoveBlockingWorker(Exception):
    """
    Another worker on coordinates.
    """
    def __init__(self, message):
        self.message = message

class MoveHeightUnreachable(Exception):
    """
    Floor is more than one story higher.
    """
    def __init__(self, message):
        self.message = message

class MoveOutOfBounds(Exception):
    """
    Direction leads to out of bounds coordinates.
    """
    def __init__(self, message):
        self.message = message

class MoveStandingOnCoordinates(Exception):
    """
    Worker must move to different position than it's already on.
    """
    def __init__(self, message):
        self.message = message

class MoveHeightFour(Exception):
    """
    Building has a fourth level
    """
    def __init__(self, message):
        self.message = message
    
class BuildBlockingWorker(Exception):
    """
    Cannot build when another worker is on coordinates.
    """
    def __init__(self, message):
        self.message = message

class BuildOutOfBounds(Exception):
    """
    Direction leads to out of bounds coordinates.
    """
    def __init__(self, message):
        self.message = message

class BuildStandingOnCoordinates(Exception):
    """
    Worker must build on a different cell than it's already on.
    """
    def __init__(self, message):
        self.message = message

class BuildHeightFour(Exception):
    """
    Building has a fourth level
    """
    def __init__(self, message):
        self.message = message
