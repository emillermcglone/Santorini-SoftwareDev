"""
Observer is used to plug into the referee and observes all phases of a game, initialization,
steady phase, and shutdown. 
"""

class Observer:
    """
    Observer gets notified of the state of games, actions taken by players, and other events 
    such as player giving up or 
    """

    def update_state_of_game(self, board):
        """
        Update the observer with the current state of the game. This
        can be used throughout initialization, steady phase and shutdown. 

        :param board: Board, current board state
        """
        pass


    def update_action(self, wid, action):
        """
        Update the observer with the next action taken by given worker.

        :param wid: string, id of worker
        :param action: Action, action taken by worker
        """
        pass

    
    def error(self, pid, message):
        """
        Update observer on player error.

        :param pid: string, id of player
        :param message: string, error message
        """
        pass

    
    def give_up(self, pid):
        """
        Player gives up in cases when they can't take an action

        :param pid: string, id of player that gives up
        """
        pass

    
    def game_over(self, pid, wid, move_action):
        """
        Update the observer with the player who won the game and winning move.

        :param pid: string, id of winning player
        :param wid: string, id of winning worker
        :param wid: Action, winning move action
        """
        pass