import json, fileinput, sys
sys.path.append(sys.path[0] + "/../../")

from Lib.util import import_cls, stdin
from Admin.configurations.stdin_configuration import STDINConfiguration


class STDINRemoteConfiguration(STDINConfiguration):
    """
    Configuration that extracts players and observers from stdin JSON values. 
    """
    
    def __init__(self, readable=stdin):
        """
        Initialize the configuration
        """
        self.configuration = None
        self.readable = readable


    def observers(self):
        """
        Create a list of observers from the given configuration path for each observer

        :return: [Observer, ...], list of obserbers
        """
        json_observers = self.__extract_from_configuration('observers', self.__observers_conf_qualifier)

        try:
            observers = []

            for observer in json_observers: 
                observer_cls = import_cls(observer[1]).Observer
                observers.append(observer_cls())

            return observers
        except:
            self.__exit()

    
    def __observers_conf_qualifier(self, value):
        """
        Check if given value is a valid observers configuration.

        :param value: Any, value to check
        :return: bool, True if valid, False otherwise
        """
        def is_name_pathstring(value):
            return isinstance(value, list) and len(value) == 2 \
                    and all(map(lambda e: isinstance(e, str), value))

        return isinstance(value, list) and all(map(is_name_pathstring, value))


    def players(self):
        """
        Create a list of player from the given configuration path for each player

        :return: [Player, ...], list of obserbers
        """
        json_players = self.__extract_from_configuration('players', self.__players_conf_qualifier)

        try:
            players = []

            for player in json_players:
                player_id = player[1]
                player_cls = import_cls(player[2]).Player
                players.append(player_cls(player_id))

            return players
        except:
            self.__exit()

    
    def __players_conf_qualifier(self, value):
        """
        Check if given value is a valid players configuration.

        :param value: Any, value to check
        :return: bool, True if valid, False otherwise
        """
        def is_kind_name_pathstring(value):
            return isinstance(value, list) and len(value) == 3 \
                    and all(map(lambda e: isinstance(e, str), value))

        return isinstance(value, list) and all(map(is_kind_name_pathstring, value))


    def ip(self):
        """
        Get the IP address from STDIN.

        :return: string, IP address
        """
        return self.__extract_from_configuration('ip', lambda v: isinstance(v, str))
            

    def port(self):
        """
        Get the port number from STDIN.

        :return: N, port number
        """
        return self.__extract_from_configuration('port', self.__valid_port)


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
        try:
            self.__set_configuration()
            value = self.configuration[key]

            if qualifier(value):
                return value

        except:
            self.__exit()
        self.__exit()


    def __exit(self):
        """
        Notify of invalid configuration and exit program.
        """
        print("No valid configuration found.")
        sys.exit()



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

