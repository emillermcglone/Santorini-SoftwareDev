from abc import ABC, abstractmethod

"""
Board is made of a zero-indexed 2D list of Cells for a Santorini game,
and manages the placement of the game's pieces. 

Cell is one of (Floor, Level) and (Worker, Level)
Floor is an empty class
Worker has id: N, and position: (x, y)
N is a natural number
Level ranges from 0 to 4 inclusive

Rule is a function (board: [[Cell, ...] ...], worker: int, move_direction: Direction, build_direction: Direction) -> bool
that returns True if move is permitted and False otherwise

Direction is one of 'N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW'

MoveError is one of:
    BlockingWorker: another worker on coordinates
    FloorUnreachable: floor is more than one story higher
    OutOfBounds: direction leads to off the board
    StandingOnCoordinates: can't move on where worker is standing
    FloorFour: can't move to the fourth level of a building

BuildError is one of:
    BlockingWorker: another worker on coordinates
    OutOfBounds: direction leads to off the board
    StandingOnCoordinates: can't build where a worker is
    FloorFour: can't build above the fourth floor
"""


class Floor:
    pass


class Board(ABC):
    @abstractmethod
    def __init__(self, win_callback, win_condition, rules, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default, and
        list of game rules.

        @param win_callback: (worker: Worker) -> void, callback function to call when win_condition is met
        @param win_condition: (board: [[Cell, ...] ...])
        @param rules: [Rule, ], list of rules validating each move and build
        @param width: N, number of cells horizontally
        @param height: N, number of cells vertically
        """
        self.win_callback = win_callback
        self.win_condition = win_condition
        self.rules = rules
        self.__board = [[(Floor(), 0)] * width] * height

    @abstractmethod
    def get_state_of_game(self):
        """
        Provide a deep copy of the board representing state of game.

        @return: [[Cell, ...] ...], the state of the game
        """
        pass

    @abstractmethod
    def place_worker(self, worker, position):
        """ 
        Place worker on start position.

        @param worker: N, id of worker to be placed
        @param position: (N, N), coordinates
        @raise OutOfBounds: given position is out of the board
        @raise BlockingWorker: another worker is on given position 
        """
        pass

    def move_and_build(self, worker, move_direction, build_direction):
        """ 
        Move worker, build in the given directions, and evoke
        win callback if game has been won.

        @param worker: N, id of worker
        @move_direction: Direction, direction for move
        @build_direction: Direction, direction for build
        @raise MoveError: invalid move
        @raise BuildError: invalid build
        """
        id = self.__move_and_build__(worker, move_direction, build_direction)
        if id >= 0:
            self.win_callback(id)

    @abstractmethod
    def __move_and_build(self, worker, move_direction, build_direction):
        """ 
        Move worker and build in the given directions. Check if
        game has been won with the move.

        @param worker: N, id of worker
        @move_direction: Direction, direction for move
        @build_direction: Direction, direction for build
        @raise MoveError: invalid move
        @raise BuildError: invalid build
        @return: -1 if game continues, N representing winner's id otherwise
        """
        pass
