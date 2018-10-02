from abc import ABC, abstractmethod

class Board(ABC):
    """
    Board is made of a zero-indexed 2D list of Cell for a Santorini game,
    and manages the placement of the game's pieces and its buildings. 

    Cell is either Height or Worker
    Height signifies a building floor: N, 0 to 4 inclusive
    Worker has id: N, position: (N, N), and height: N, 0 to 4 inclusive
    N is a natural number
    Height of 0 signifies the ground floor 

    Direction is an Enum, one of N, E, S, W, NE, NW, SE, SW
    """

    @abstractmethod
    def __init__(self, rules, board=None, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default, and
        list of game rules.

        :param rules: Rules, the rule checking interface
        :param board: [[Cell, ...], ...], a board to initialize from 
        :param width: N, number of cells horizontally
        :param height: N, number of cells vertically
        """
        pass

    @abstractmethod
    def is_game_over(self, win_condition):
        """
        Check if game has been won.

        :param win_condition: (board: [[Cell, ...] ...]) -> N | -1, returns id of winning worker, -1 if game continues
        :return: N | -1, id of winning worker or -1 if game continues
        """
        pass

    @property
    @abstractmethod
    def board(self):
        """
        Provide a deep copy of the board representing state of game.

        :return: [[Cell, ...] ...], the state of the game
        """
        pass

    @property
    @abstractmethod
    def rules(self):
        """ 
        Provide a deep copy of the rules interface.

        :return: Rules, the rules of the game
        """
        pass

    @abstractmethod
    def cell(self, x, y):
        """
        Get a copy of the cell on the given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: Cell, the cell on given coordinates
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
    def height(self, worker, direction):
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
        Move worker to given direction if rules are satisfied.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        pass


    @abstractmethod
    def build(self, worker, build_direction):
        """
        Build a floor in the given direction if rules are satisfied.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        pass