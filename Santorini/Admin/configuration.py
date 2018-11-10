"""
IConfiguration configures a tournament's players and observers. It is used 
by and passed to the tournament to extract the required information. 
"""

from abc import ABC, abstractmethod

class IConfiguration(ABC):
    """
    Configuration that provides the tournament manager with the list of
    players and observers involved.
    """

    @abstractmethod
    def players(self):
        """
        Get players from configuration.

        :return: [Player, ...], list of players for this configuration
        """
        pass


    @abstractmethod
    def observers(self):
        """
        Get observers from configuration.

        :return: [Observer, ...], list of observers for this configuration
        """
        pass