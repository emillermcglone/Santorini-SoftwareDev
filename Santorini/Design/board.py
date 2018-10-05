"""
Interface design for board with which Santorini games move/place workers
and build buildings.

ICell is an individual cell with height on the board.

N is a natural number
"""

from abc import ABC, abstractmethod

class IBoard(ABC):
    """
    IBoard is made of a zero-indexed 2D list of ICell for a Santorini game,
    and manages the placement of the game's pieces and its buildings. 
    No rules are baked into the board. The board is in charge of the game's pieces 
    and provide basic inquiries about its pieces.
    """

    @abstractmethod
    def __init__(self, board=None, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default.

        :param board: [[ICell, ...], ...], a board to initialize from 
        :param width: N, number of cells horizontally
        :param height: N, number of cells vertically
        """
        pass

    @abstractmethod
    def is_game_over(self, win_condition):
        """
        Check if game has been won.

        :param win_condition: (board: [[ICell, ...] ...]) -> N | -1, returns id of winning worker, -1 if game continues
        :return: N | -1, id of winning worker or -1 if game continues
        """
        pass

    @property
    @abstractmethod
    def board(self):
        """
        Provide a deep copy of the board representing state of game.

        :return: [[ICell, ...] ...], the state of the game
        """
        pass

    @abstractmethod
    def cell(self, x, y):
        """
        Get a copy of the cell on the given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: ICell, the cell on given coordinates
        :raise ValueError: if given position is out of bounds
        """
        pass

    @abstractmethod
    def neighbor(self, worker, direction):
        """
        Is there a cell in the given direction?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: bool, True if it is an empty cell, False otherwise
        """
        pass


    @abstractmethod
    def occupied(self, worker, direction):
        """
        Is the neighboring cell occupied by worker?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: bool, True if worker occupies neighbor, False otherwise
        """
        pass


    @abstractmethod
    def neighbor_height(self, worker, direction):
        """
        What is the height of neigboring cell?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: N, the height of neighboring building
        :raise ValueError: if there's no neighboring cell
        """
        pass

    
    @abstractmethod
    def get_worker_position(self, worker):
        """
        Get the position of given worker.

        :param worker: N, id of worker
        :return: (N, N), position of worker
        :raise ValueError: if worker is not found
        """
        pass


    @abstractmethod
    def place_worker(self, worker, x, y):
        """ 
        Place worker on position.

        :param worker: N, id of worker to be placed
        :param x: N, x coordinate
        :param y: N, y coordinate
        :raise ValueError: if another worker is on position
        """
        pass


    @abstractmethod
    def move(self, worker, move_direction):
        """ 
        Move worker to given direction.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        pass


    @abstractmethod
    def build(self, worker, build_direction):
        """
        Build a floor in the given direction.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        pass