"""
Board is made of a zero-indexed 2D list of Cells for a Santorini game,
and manages the placement of the game's pieces. 

Cell is one of Height or Worker
Height signifies a building floor: N, 0 to 4 inclusive
Worker has id: N, position: (N, N), and height: N, 0 to 4 inclusive
N is a natural number
Height of 0 signifies the ground floor 

Rule is a function (board: [[Cell, ...] ...], worker: int, move_direction: Direction, build_direction: Direction) -> bool
that returns True if move is permitted and False otherwise

Direction is one of 'N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW'

MoveError is one of:
    BlockingWorker: another worker on coordinates
    HeightUnreachable: floor is more than one story higher
    OutOfBounds: direction leads to off the board
    StandingOnCoordinates: can't move on where worker is standing
    HeightFour: can't move to the fourth level of a building

BuildError is one of:
    BlockingWorker: another worker on coordinates
    OutOfBounds: direction leads to off the board
    StandingOnCoordinates: can't build where a worker is
    HeightFour: can't build above the fourth floor
"""

import copy

from Common.administrative_components import *
from abc import ABC, abstractmethod

class Board(ABC):
    def __init__(self, rules, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default, and
        list of game rules.

        :param rules: Rules, the rule checking interface
        :param width: N, number of cells horizontally
        :param height: N, number of cells vertically
        """
        self.rules = rules
        self.workers = {}
        self._board = [[Height(0)] * width] * height

    def is_game_over(self, win_condition):
        """
        Check if game has been won.

        :param win_condition: (board: [[Cell, ...] ...]) -> N | -1, returns id of winning worker, -1 if game continues
        :return: N | -1, id of winning worker or -1 if game continues
        """
        return win_condition(self.board)

    @property
    def board(self):
        """
        Provide a copy of the board representing state of game.

        :return: [[Cell, ...] ...], the state of the game
        """
        return copy.deepcopy(self._board)

    @abstractmethod
    def place_worker(self, worker, position):
        """ 
        Place worker on start position.

        :param worker: N, id of worker to be placed
        :param position: (N, N), coordinates
        :raise PlaceOutOfBounds: given position is out of the board
        :raise PlaceBlockingWorker: another worker is on given position 
        """
        try: 
            cell = self.board[position[0], position[1]]
            if isinstance(cell, Worker):
                raise PlaceBlockingWorker("Another worker on given position")
        except IndexError:
            raise PlaceOutOfBounds("Coordinates are outside of the board.")

        self.board[position[0], position[1]] = Worker(worker, position)
        self.workers[worker] = position

    @abstractmethod
    def move_and_build(self, worker, move_direction, build_direction):
        """ 
        Move worker and build in the given directions if rules 
        are satisfied.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        :param build_direction: Direction, direction for build
        :raise MoveError: invalid move
        :raise BuildError: invalid build
        """
        if self.rules.check(self.board, worker, move_direction, build_direction):
            
            

