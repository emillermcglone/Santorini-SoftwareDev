"""
Board is made of a zero-indexed 2D list of Cell for a Santorini game,
and manages the placement of the game's pieces and its buildings. 

Cell is either Height or Worker
Height signifies a building floor: N, 0 to 4 inclusive
Worker has id: N, position: (N, N), and height: N, 0 to 4 inclusive
N is a natural number
Height of 0 signifies the ground floor 

Direction is one of 'N', 'E', 'S', 'W', 'NE', 'NW', 'SE', 'SW'
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
        Provide a deep copy of the board representing state of game.

        :return: [[Cell, ...] ...], the state of the game
        """
        return copy.deepcopy(self._board)

    @abstractmethod
    def place_worker(self, worker, position):
        """ 
        Place worker on start position.

        :param worker: N, id of worker to be placed
        :param position: (N, N), coordinates
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