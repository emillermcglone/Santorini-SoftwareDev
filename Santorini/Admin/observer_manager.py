import copy

class ObserverManager:
    """
    Manage the observers for a referee by updating them.
    """

    def __init__(self, observers, board, players):
        """
        Initialize manager's observers, board state, and players

        :param observers: [Observer, ...], list of observers 
        :param board: GameBoard, copy of board
        :param players: [Player, ...], list of players 
        """
        self.observers = observers
        self.__board = board
        self.__players = players


    @property
    def board(self):
        return copy.deepcopy(self.__board)


    def update_state(self):
        """
        Update observers about state of game.
        """
        self.__obs(lambda obs: obs.update_state_of_game(self.board))


    def update_action(self, wid, move_action, build_action):
        """
        Update observers about recent action.

        :param wid: string, worker id
        :param move_action: Action, move specification
        :param build_action: Action, build specification
        """
        def go(observer):
            observer.update_action(wid, move_action, build_action)
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


    def game_over(self, pid, wid, move_action):
        """
        Update observers about game over.

        :param pid: string, winner id
        :param wid: string, winning move worker id
        :param move_action: Action, winning move action
        """
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


