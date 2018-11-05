

class ITournamentManager:
    """
    Santorini tournament manager that runs games in a round robin fashion among 
    a fixed but arbitrary number of players. 

    Policy on Names If the tournament manager discovers that several players with the same name are to participate in a tournament, it picks a unique name for all but one of the players and informs these players of the chosen names.

    Policy on Broken Players When a tournament manager is informed that a player misbehaved, it acts as follows:

    - The player is removed from all future encounters; there are no second chances.

    - All past meet-ups involving the player are counted as won by the opponent.

    - If a player breaks after winning past games due to its opponents' breakage, the game is eliminated from the tournament evaluation.

    The End When the tournament is over, the tournament manager delivers two pieces of information:

    - The first is a list of names of players that misbehaved in any way. They are listed in the order of failure.

    - The second lists all completed games where each piece of game information lists the winner’s and the loser’s name. The games are listed in the order of "first plays against rest, second plays against rest, etc."
    """

    def __init__(self, configuration=None):
        """
        Initialize a tournament manager with configuration.

        :param configuration: Configuration, game configuration containing players
        """
        self.players = configuration.players


    def run_tournament(self):
        """
        Run a round robin tournament with the players.

        :return: TournamentResult, result of tournament
        """
        pass
