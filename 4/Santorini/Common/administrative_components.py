""" 
Common data and knowledge among administrative components and players
in a Santorini game.

Common data include physical game pieces, the rules of the game,
and the player interface.

N is a natural number 
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
        self._height = height

    @property
    def height(self):
        """
        Height of building.
        """
        return self._height

    @height.setter
    def height(self, new_height):
        """
        Set Cell's height to new_height.

        :param new_height: the new height of Cell
        :raise AttributeError: if height is not from 0 to 4
        """
        if new_height < 0 and new_height > 4:
            raise AttributeError
        self._height = new_height

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
        return super().__init__(height)

class Worker(Cell):
    """
    Worker of a Santorini board. It has a height attribute representing which 
    floor it is on.
    """

    def __init__(self, id, position, height = 0):
        """
        Initialize Worker with id, position, and height of building the worker is on.

        :param id: N, id of Worker
        :param position: (x, y), the position of Worker
        :param height: N, height of building worker is on, defaults to 0
        :raise AttributeError: if height is not from 0 to 4        
        """
        super().__init__(height)
        self.id = id
        self.position = position

class Rules:
    """
    Set of rules for a Santorini game which both Santorini and players can use
    to validate their moves before making them.
    """

    def __init__(self, rules):
        """
        Initalize Rules with list of Rule. 
        Rule is a function (board: [[Cell, ...] ...], worker: N, move_direction: Direction, build_direction: Direction) -> bool
  
        :param rules: [Rule, ...], list of rules for move and build 
        """
        self.rules = rules

    def check(self, board, worker, move_direction, build_direction):
        """
        Check if the move and build are valid.

        :param board: [[Cell, ...] ...], zero-indexed 2D list of Cells
        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        :param build_direction: Direction, direction for build
        """
        return all(list(map(lambda rule: rule(board, worker, move_direction, build_direction), self.rules)))