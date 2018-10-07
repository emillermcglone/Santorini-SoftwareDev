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

    @property
    @abstractmethod
    def board(self):
        """
        Provide a representation of the board.
        """
        pass