import json, fileinput, sys
sys.path.append(sys.path[0] + "/../../")

from Lib.util import import_cls

class STDINConfiguration:
    
    def __init__(self):
        """
        initialize the configuration
        """
        self.configuration = None

    def __set_configuration(self):
        """
        sets the configuration to JSON
        """
        if self.configuration is None:
            lines = ""
            for line in fileinput.input():
                lines += line
        
            self.configuration = json.loads(lines)


    def observers(self):
        """
        Create a list of observers from the given configuration path for each observer

        :return: [Observer, ...], list of obserbers
        """
        self.__set_configuration()
        json_observers = self.configuration['observers']

        observers = []

        for observer in json_observers: 
            observer_cls = import_cls(observer[1])
            observers.append(observer_cls())

        return observers


    def players(self):
        """
        Create a list of player from the given configuration path for each player

        :return: [Observer, ...], list of obserbers
        """
        self.__set_configuration()
        json_players = self.configuration['players']

        players = []
        
        for player in json_players:
            player_id = player[1]
            player_cls = import_cls(player[2])
            players.append(player_cls(player_id))

        return players