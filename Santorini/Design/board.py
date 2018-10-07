"""
Interface for a physical board with which Santorini components interact with.

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

    @property
    @abstractmethod
    def board(self):
        """
        Provide a representation of the board.
        """
        pass