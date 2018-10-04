""" 
Concrete classes for common components.
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from enum import Enum

from Common.components import ICell, IRules, Direction

class Cell(ICell):
    """
    Individual cell element with height on a Santorini board.
    """

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

    def __str__(self):
        return "{0} {1}".format(type(self).__name__, self.height)
        

class Height(Cell):
    """
    Height of a building.
    """

class Worker(Cell):
    """
    Worker of a Santorini board whose height represents which floor
    it is on.
    """

    def __init__(self, worker_id, height = 0):
        """
        Initialize with id, position, and height of building the worker is on.

        :param worker_id: N, id of Worker
        :param position: (N, N), the position of Worker
        :param height: N, height of building worker is on, defaults to 0
        :raise ValueError: if height is not from 0 to 4        
        """
        super().__init__(height)
        self.id = worker_id


class Rules(IRules):
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