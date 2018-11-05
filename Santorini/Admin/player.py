"""
Admin Player is used throughout games. 
"""

from Common.player import Player as IPlayer

class Player(IPlayer):
    def __init__(self, player):
        self.player = player
        self.id = player.get_id()

    def get_id(self):
        return self.id

    def get_placement(self, *args, **kwargs):
        return self.player.get_placement(*args, **kwargs)

    def get_move(self, *args, **kwargs):
        return self.player.get_move(*args, **kwargs)

    def get_build(self, *args, **kwargs):
        return self.player.get_build(*args, **kwargs)

    def game_over(self, *args, **kwargs):
        return self.player.game_over(*args, **kwargs)

