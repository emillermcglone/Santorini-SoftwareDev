"""
Admin Player is used throughout games. 
"""

from Common.player import Player

class GuardedPlayer(Player):
    """
    Guarded player delegates all functionalities to given external player, but keeps its id 
    constant throughout a game for Admin's convenience. 
    """

    def __init__(self, player):
        """
        Initialize guarded player's id with that of the external player. 

        :param player: Player, external player
        """
        self.player = player
        self.id = player.get_id()
        

    def get_id(self):
        """
        Get the id of this guarded player

        :return: string, id of player
        """
        return self.id

    
    def set_id(self, new_id):
        """
        Set the this guarded player's and the external player's ids.

        :param new_id: string, the new id
        """
        self.id = new_id
        self.player.set_id(new_id)


    def get_placement(self, *args, **kwargs):
        return self.player.get_placement(*args, **kwargs)


    def get_move(self, *args, **kwargs):
        return self.player.get_move(*args, **kwargs)


    def get_build(self, *args, **kwargs):
        return self.player.get_build(*args, **kwargs)


    def game_over(self, *args, **kwargs):
        return self.player.game_over(*args, **kwargs)

