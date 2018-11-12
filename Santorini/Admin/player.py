"""
GuardedPlayer is used throughout games as an internal representation of the
external Player for safe use by the admin and some convenient query methods
for the ObserverManager.
"""

from Common.player import Player

class GuardedPlayer(Player):
    """
    Guarded player delegates all functionalities to given external player, but keeps its id 
    constant throughout a game for Admin's convenience and tracks all of the player's
    actions for records
    """

    def __init__(self, player):
        """
        Initialize guarded player's id with that of the external player. 

        :param player: Player, external player
        """
        self.player = player
        self.id = player.get_id()
        self.reset()


    def reset(self):
        self.__place_history = []
        self.__move_history = []
        self.__build_history = []


    def last_place(self):
        """
        Get the last place action by this player from place history.

        :return: PLACE, the last place action
        """
        return self.__place_history[-1]


    def last_move(self):
        """
        Get the last move action by this player from move history.

        :return: MOVE, the last move action
        """
        return self.__move_history[-1]

        
    def last_build(self):
        """
        Get the last build action by this player from the build history.
        
        :return: BUILD, the last build action
        """
        return self.__build_history[-1]
        

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