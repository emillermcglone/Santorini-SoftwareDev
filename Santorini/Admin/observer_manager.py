import copy

class ObserverManager:
    """
    Manage the observers for a referee by updating them.
    """

    def __init__(self, observers, board):
        """
        Initialize manager's observers, board state, and players

        :param observers: [Observer, ...], list of observers 
        :param board: GameBoard, copy of board
        """
        self.observers = observers
        self.__board = board


    @property
    def board(self):
        return copy.deepcopy(self.__board)


    def add_observer(self, observer):
        """
        Add another observer.

        :param observer: Observer, observer of series of games.
        """
        self.observers.append(observer)


    def update_state(self):
        """
        Update observers about state of game.
        """
        self.__obs(lambda obs: obs.update_state_of_game(self.board))


    def update_action(self, player):
        """
        Update observers about recent action.

        :param player: GuardedPlayer, the player with the recent action
        """
        last_move = player.last_move()
        last_build = player.last_build()
        wid = last_move[0]

        def go(observer):
            observer.update_action(wid, last_move[1], last_build[1])
            observer.update_state_of_game(self.__board)

        self.__obs(go)


    def give_up(self, pid):
        """
        Update observers about player who gives up.

        :param pid: string, id of player
        """
        self.__obs(lambda obs: obs.give_up(pid))


    def error(self, pid, message):
        """
        Update observers about player error.

        :param pid: string, player id
        :param message: string, error message
        """
        self.__obs(lambda obs: obs.error(pid, message))


    def game_over(self, winner):
        """
        Update observers about game over.

        :param winner: GuardedPlayer, winner of game
        """
        pid = winner.get_id()
        last_move = winner.last_move()
        wid = last_move[0]
        move_action = last_move[1]
        self.__obs(lambda obs: obs.game_over(pid, wid, move_action))


    def __obs(self, func):
        """
        Update every observer and remove broken observers

        :param func: (Observer) -> void, function used to update observer
        """
        stable_observers = []
        for observer in self.observers:
            try:
                func(observer)
                stable_observers.append(observer)
            except:
                pass
        self.observers = stable_observers


