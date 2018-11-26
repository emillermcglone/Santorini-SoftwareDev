import fileinput, json
import math

from Admin.server_configuration import IServerConfiguration

class STDINServerConfiguration(IServerConfiguration):
    """
    Server configuration that reads from STDIN.
    """

    def __init__(self):
        """
        Initialize STDINServerConfiguration.
        """
        self.configuration = None


    def __set_configuration(self):
        """
        Set the configuration to stdin JSON values if
        the configuration has not been set. 
        """
        if self.configuration is None:
            lines = ""
            for line in fileinput.input():
                lines += line
                
            self.configuration = json.loads(lines)


    def __extract_from_configuration(self, key, fallback):
        """
        Extract value from configuration from given key. 
        If no valid configuration is found, use fallback function

        :param key: string, key in configuration
        :param fallback: () -> Any, fallback function
        :return: Any, value from configuration
        """
        try:
            self.__set_configuration()
            return self.configuration[key]
        except:
            print("No valid configuration found. Try again")
            self.configuration = None
            return fallback()
    

    def min_players(self):
        """
        Minimum number of players accepted.

        :return: N, minimum number of players accepted
        """
        value = self.__extract_from_configuration('min players', self.min_players)
        if not isinstance(value, int) or value < 0:
            print("No valid configuration found. Try again")
            self.configuration = None
            return self.min_players()


    
    def port(self):
        """
        Port to start server on.

        :return: N, port to start server on
        """
        value = self.__extract_from_configuration('port', self.port)
        if not isinstance(value, int) or value < 0:
            print("No valid configuration found. Try again")
            self.configuration = None
            return self.port()


    def waiting_for(self):
        """
        Wait time for remote players to connect to server.

        :return: N > 0, positive number of seconds to wait for remote players
        """
        value = self.__extract_from_configuration('waiting for', self.waiting_for)
        if not isinstance(value, int) or value <= 0:
            print("No valid configuration found. Try again")
            self.configuration = None
            return self.waiting_for()


    def repeat(self):
        """
        Should the server repeat an indefinite number of tournaments or run a single one?

        :return: bool, True if repeat, False otherwise
        """
        value = self.__extract_from_configuration('repeat', self.repeat)
        if value is not 0 and value is not 1:
            print("No valid configuration found. Try again")
            self.configuration = None
            return self.repeat()

        return value is 1