from Admin.configuration import IConfiguration

class StandardConfiguration(IConfiguration):
    """ TournamentManager configuration initialized with players and observers. """

    def __init__(self, players, observers):
        """
        Initialize configuration with players and observers.

        :param players: [Player, ...], players for the TournamentManager
        :param observers: [Observer, ...], observers for the TournamentManager
        """
        self.__players = players
        self.__observers = observers

    def players(self):
        return self.__players

    def observers(self):
        return self.__observers