"""
The tournament manager reads a configuration file and configures the tournament
according to the instructions in this file.

The configuration is a single JSON object of the following shape:

    { "players"   : [[Kind, Name, PathString], ..., [Kind, Name, PathString]],
      "observers" : [[Name, PathString], ..., [Name, PathString]]}

    that is, a hash table with two keys—"players" and "observers"—each mapped to an
    array of player and observer specification, respectively. 

The specifications have the following meaning:

    Kind is one of:
        - "good", meaning a player that is intended to be well-behaved;
        - "breaker", referring to a player that terminates in a timely manner but misbehaves;
        - "infinite", denoting a player that goes into an infinite loop.
    
    Name is a JSON String

    PathString is a Linux Path to a dynamically loadable component that implements
    the respective player or observer.

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