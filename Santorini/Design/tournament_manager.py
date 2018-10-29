"""
Interface for a tournament manager. Runs a round robin tournament with a fixed but arbitrary number 
of players. Accounts for how to start a tournament, what to do with broken players,
and how to report the results, etc. 

     
Starting tournament:
    - All players play single match against every other.
    - Matches and results are tracked internally 


Broken Players:
    - Remove players from tournament
    - Void all past and future games with the broken players
    - Keep track of broken players


Reporting results:
    - Outcome of every match of each player
    - Broken players discovered along the way
    - Winner(s) of tournament
    - Report appropriately if all players are broken


Edge cases:
    - 2 player tie: Run a single match between them
    - 3 or more player tie: Compare win/lose results of each player against the other tied players
    - 3 or more player tie with wins/loses within same group: declare all as winners


TournamentResult is a:
    {
        'victories': {
            <Player>: [<Player>, ...]
            ...
        },

        'brokenPlayers': [<Player>, ...],

        'winners': <Player> | [<Player>, ...]
    }

where 'victories' contains each Player's victories against others,
'brokenPlayers' is the list of broken players that gave invalid actions or were unresponsive,
and 'winners' is either a single player or list of players who won the tournament.

If all players are discovered to be broken, 'victories' and 'winners' are "null" and brokenPlayers
contain all given players.
"""

from abc import ABC, abstractmethod


class ITournamentManager(ABC):
    """
    Santorini tournament manager that runs games in a round robin fashion among 
    a fixed but arbitrary number of players. 
    """

    def __init__(self, players):
        """
        Initialize a tournament manager with players.

        The manager will remove any duplicate players based on id.

        :param players: [Player, ...], players in the tournament
        :raise ValueError: if set of players comes down to empty or a single player
        """
        pass


    def run_tournament(self):
        """
        Run a round robin tournament with the players.

        :return: TournamentResult, result of tournament
        """
        pass
