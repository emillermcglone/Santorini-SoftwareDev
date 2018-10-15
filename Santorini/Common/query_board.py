"""
IQueryBoard provides components such as Player, Rules, and Strategy an interface to make
inquiries about game pieces. It does not mutate the state of the game.

The referee passes this board representation to components that need it to fulfill
their purpose. 
"""

import copy, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abc import ABC, abstractmethod
from Design.board import IBoard

class IQueryBoard(IBoard):
    """
    A query board provides an interface for components to inquire basic information
    on game pieces. 
    """

    @property
    def dimensions(self):
        """
        Dimensions of board.

        :return: (N, N), width and height of board
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
    def height(self, x, y):
        """
        Get the height of the cell on the given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: N, the height of the cell
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
        :raise ValueError: if neighboring cell does not exist
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


    @property
    @abstractmethod
    def workers(self):
        """
        Deep copy of all workers on board.
        
        :return: [Worker, ...], deep copy of all workers
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
       