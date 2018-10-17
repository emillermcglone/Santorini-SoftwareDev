# This file contains custom exceptions for the game


class IllegalPlaceException(Exception):
    """Raised when attempting to place a worker illegally."""
    pass


class IllegalMoveException(Exception):
    """Raised when attempting to move a worker illegally."""


class IllegalBuildException(Exception):
    """Raised when attempting to build onto a building illegally."""
