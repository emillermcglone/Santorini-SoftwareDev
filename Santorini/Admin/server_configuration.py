
# Used to configure servers, providing the necessary attributes for the 
# server to run: minimum players, port number, time to wait for, and repeat or not
from abc import ABC, abstractmethod

class IServerConfiguration(ABC):
    """
    Server configuration specifying minimum number of players, port number,
    wait time for remote components to connect, and whether server should
    run an indefinite number of tournaments or not. 
    """

    @abstractmethod
    def min_players(self):
        """
        Minimum number of players accepted.

        :return: N, minimum number of players accepted
        """
        pass

    
    @abstractmethod
    def port(self):
        """
        Port to start server on.

        :return: N, port to start server on
        """
        pass

    @abstractmethod
    def waiting_for(self):
        """
        Wait time for remote players to connect to server.

        :return: N > 0, positive number of seconds to wait for remote players
        """
        pass

    @abstractmethod
    def repeat(self):
        """
        Should the server repeat an indefinite number of tournaments or run a single one?

        :return: bool, True if repeat, False otherwise
        """
        pass