from Admin.configuration import IConfiguration

from Player.players.random_player import Player as RandomPlayer
from Player.players.infinite_loop_player import InfiniteLoopPlayer
from Player.players.misbehaving_player import MisbehavingPlayer

class Configuration(IConfiguration):
    def __init__(self, players, observers):
        self.__players = players
        self.__observers = observers

    def players(self):
        return self.__players

    def observers(self):
        return self.__observers