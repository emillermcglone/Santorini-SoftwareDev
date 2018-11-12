"""
Data representation used by referee for game over states based 
on different game over conditions.
"""

from enum import Enum

class GameOver(Exception):
    """ Game over state holding winning and losing players and condition of game over """

    def __init__(self, winner, loser, condition):
        """
        Hold winner, loser and condition of victory for game. 

        :param winner: GuardedPlayer, winner
        :param loser: GuardedPlayer, loser
        :param condition: GameOverCondition, condition for game over
        :raise ValueError: if winner and loser are same player
        """
        if winner == loser:
            raise ValueError("Winner and loser are the same player")

        self.winner = winner
        self.loser = loser
        self.condition = condition


class GameOverCondition(Enum):
    """ Condition for game over. """

    LoserBrokeInTournament = "Loser broke post match in the tournament, regardless of previous victory or defeat"
    Crash = "Loser crashed at runtime"
    Timeout = "Loser timed out on action request"
    InvalidAction = "Loser specified invalid action"
    FairGame = "Winner won by game rules"