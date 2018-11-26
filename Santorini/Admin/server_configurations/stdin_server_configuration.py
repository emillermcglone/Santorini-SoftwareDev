import fileinput, json, sys
import math

def stdin():
    """
    Read all lines from fileinput.

    :return: string, input from fileinput
    """
    lines = ""
    for line in fileinput.input():
        lines += line
    return lines

class ServerConfiguration:
    """
    Server configuration that reads from given a readable.
    If no valid configuration is found, program exits. 
    """

    def __init__(self, readable=stdin):
        """
        Initialize STDINServerConfiguration.
        """
        self.configuration = None
        self.readable = readable


    def min_players(self):
        """
        Minimum number of players accepted.

        :return: N, minimum number of players accepted
        """
        return self.__extract_from_configuration('min players', self.__natural)

    
    def port(self):
        """
        Port to start server on.

        :return: N, port to start server on
        """
        return self.__extract_from_configuration('port', self.__valid_port)


    def waiting_for(self):
        """
        Wait time for remote players to connect to server.

        :return: N > 0, positive number of seconds to wait for remote players
        """
        return self.__extract_from_configuration('waiting for', lambda v: self.__natural(v) and v > 0)


    def repeat(self):
        """
        Should the server repeat an indefinite number of tournaments or run a single one?

        :return: bool, True if repeat, False otherwise
        """
        value = self.__extract_from_configuration('repeat', lambda v: v is 0 or v is 1)
        return value is 1


    def __set_configuration(self):
        """
        Set the configuration to stdin JSON values if
        the configuration has not been set. 
        """
        if self.configuration is None:
            self.configuration = json.loads(self.readable())
        


    def __extract_from_configuration(self, key, qualifier):
        """
        Extract value from configuration from given key. 
        If no valid configuration is found, use fallback function

        :param key: string, key in configuration
        :param qualifier: (Any) -> bool, qualifier to determine if value is valid
        :return: Any, value from configuration
        """
        value = None

        try:
            self.__set_configuration()
            value = self.configuration[key]

            if not qualifier(value):
                raise Exception()

        except:
            print("No valid configuration found.")
            sys.exit()

        return value


    def __valid_port(self, value):
        """
        Is given port number valid?

        :param value: Any, value to check
        :return bool, True if valid port number, False otherwise
        """
        return self.__natural(value) and value >= 50000 and value <= 60000


    def __natural(self, value):
        """ 
        Is given value a natural number?

        :param value: Any, value to check
        :return: bool, True if natural number, False otherwise
        """
        return not isinstance(value, bool) and isinstance(value, int) and value >= 0

