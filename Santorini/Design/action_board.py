"""
IActionBoard is to be used by the referee throughout the phases of the game. It is responsible 
for executing the changes to the state of the game.
"""

import copy, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from Design.board import IBoard

class IActionBoard(IBoard):
    """
    An action board handles placing and moving workers, and building floors on top of buildings. 
    No rules are baked into this board. This board is in charge of the game's pieces.
    """

    @abstractmethod
    def place(self, worker, x, y):
        """ 
        Place worker on position.

        :param worker: N, id of worker to be placed
        :param x: N, x coordinate
        :param y: N, y coordinate
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