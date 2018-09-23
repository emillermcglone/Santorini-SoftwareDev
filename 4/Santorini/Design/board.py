from abc import ABC, abstractmethod

"""
Board is made of a zero-indexed 2D list of Cells for a Santorini game. 

Cell is one of (Floor, Level) and (Worker, Level)
Floor is an empty class
Worker has id: int, and position: (x, y)
Level ranges from 0 to 4 inclusive

Rule is a (board: [[Cell, ...] ...], worker: int, move_direction: Direction, build_direction: Direction) -> bool
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


class Board(ABC):

    def __init__(self, win_callback, win_condition, rules, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default, and
        list of game rules.

        @param win_callback: (worker: Worker) -> void, callback function to call when win_condition is met
        @param win_condition: condition for a win
        @param rules: list of Rule validating each move and build
        @param width: number of cells horizontally
        @param height: number of cells vertically
        """
        pass

    @abstractmethod
    def place_worker(self, worker, position):
        """ 
        Place worker on start position

        @param worker: id of worker to be placed
        @param position: (x, y) coordinates
        @raise OutOfBounds: given position is out of the board
        @raise BlockingWorker: another worker is on given position 
        """

        pass

    @abstractmethod
    def move_and_build(self, worker, move_direction, build_direction):
        """ 
        Move worker and build in the given directions.

        @param worker: id of worker
        @move_direction: Direction for move
        @build_direction: Direction for build
        @raise MoveError: invalid move
        @raise BuildError: invalid build
        """
        pass
