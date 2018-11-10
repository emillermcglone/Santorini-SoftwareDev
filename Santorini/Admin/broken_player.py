"""
Error for when a player breaks in the context of cheating or unresponsiveness.
This is meant to be only used internally with the referee. 
"""


class BrokenPlayer(Exception):
    """
    Error for when a player breaks in the context  of cheating or unresponsiveness.
    """

    def __init__(self, player, condition):
        """
        :param player: Player, player who breaks
        :param condition: GameOverCondition, condition for breaking
        """
        self.player = player
        self.condition = condition