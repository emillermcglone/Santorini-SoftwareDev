# This file contains custom exceptions for the game
class IllegalActionException(Exception):
    """ Raised when attempting an illegal action. """

class IllegalPlaceException(IllegalActionException):
    """Raised when attempting to place a worker illegally."""


class IllegalMoveException(IllegalActionException):
    """Raised when attempting to move a worker illegally."""


class IllegalBuildException(IllegalActionException):
    """Raised when attempting to build onto a building illegally."""

