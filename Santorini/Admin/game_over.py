from enum import Enum

class GameOver:
    """ Game over state """

    def __init__(self, winner, loser, condition):
        """
        Hold winner, loser and condition of victory for game. 

        :param winner: Player, winner
        :param loser: Player, loser
        :param condition: GameOverCondition, condition for game over
        :raise ValueError: if winner and loser are same player
        """
        if winner == loser:
            raise ValueError("Winner and loser are the same player")

        self.winner = winner
        self.loser = loser
        self.condition = condition


class GameOverCondition(Enum):
    Timeout = "Loser timed out on action request"
    InvalidAction = "Loser specified invalid action"
    FairGame = "Winner won by game rules"