# This file contains the TurnPhase enum representing the various phases of a turn in the game

from enum import Enum


class TurnPhase(Enum):
    """
    # A TurnPhase is one of:
      - "PLACE", representing the initial piece placement phase
      - "MOVE", representing the move phase of a player's turn
      - "BUILD", representing the build phase of a player's turn
    """
    PLACE = 1
    MOVE = 2
    BUILD = 3
