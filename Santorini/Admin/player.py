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
        self.__place_history = []
        self.__move_history = []
        self.__build_history = []
        

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


    def get_placement(self, board, wid, rule_checker):
        place = self.player.get_placement(board, wid, rule_checker)
        self.__place_history.append(place)
        return place


    def get_move(self, board, rule_checker):
        move = self.player.get_move(board, rule_checker)
        wid = board.get_worker_id(*move['xy1'])
        self.__move_history.append((wid, move))
        return move


    def get_build(self, board, wid, rule_checker):
        build = self.player.get_build(board, wid, rule_checker)
        given_wid = board.get_worker_id(*build['xy1'])
        self.__build_history.append((given_wid, build))
        return build


    def game_over(self, status):
        return self.player.game_over(status)