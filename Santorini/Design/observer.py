"""
Observer is used to plug into the referee and observes all phases of a game, initialization,
steady phase, and shutdown. 

A Board is [[Cell, ...], ...].

A Cell is one of: a Height or a BuildingWorker Worker.

A Height is one of: 0, 1, 2, 3, 4. It indicates (the height of) a building.

A BuildingWorker is a String that starts with a single digit followed by a Worker. The first digit represents the Height of the building.

A Worker is a string of lowercase letters that ends in either 1 or 2. The last digit indicates whether it is the first or the second worker of a player. The lowercase letters are the name of the player that owns the worker.

Action is one of:
PLACE:
    {'type': 'place', 'wid' <Worker_ID>, 'xy': [<Number>, <Number>]}

MOVE:
    {'type': 'move', 'xy1': [<Number>, <Number>], 'xy2': [<Number>, <Number>]}

BUILD:
    {'type': 'build', 'xy1': [<Number>, <Number>], 'xy2': [<Number>, <Number>]}
"""

class IObserver:

    def update_state_of_game(self, board):
        """
        Update the observer with the current state of the game. This
        can be used throughout initialization, steady phase and shutdown. 

        :param board: Board, specification of current state
        """
        pass


    def update_action(self, wid, action):
        """
        Update the observer with the next action taken by given player.

        :param pid: string, id of player
        :param action: Action, action taken by player
        """
        pass

    
    def give_up(self, pid):
        """
        Player gives up.

        :param pid: string, id of player that gives up
        """
        pass

    
    def game_over(self, pid, wid, move_action):
        """
        Update the observer with the player who won the game and the last state
        of the game.

        :param winner: string, id of winning player
        :param condition: GameOverCondition, condition of game over
        """
        pass