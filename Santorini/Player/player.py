class IPlayer(ABC):
    """
    Player component for Santorini, and intermediary between administrative
    components and the actor
    """

    @abstractmethod
    def prompt_place(self, board, workers):
        """
        Prompt the player for their place turn.

        :param board: IQueryBoard, the current board of the game
        :param workers: [N, ...], list of worker ids that belong to this player
        :return: (N, N), the x and y coordinates to place a new worker on
        """
        pass


    @abstractmethod
    def prompt_move(self, board, workers):
        """
        Prompt the player for their move turn. 

        :param board: IQueryBoard, the current board of the game
        :param workers: [N, ...], list of worker ids player can move
        :return: (N, Direction), the worker id, move direction
        """
        pass

    @abstractmethod
    def prompt_build(self, board, worker):
        """
        Prompt the player for their build turn. 

        :param board: IQueryBoard, the current board of the game
        :param worker: N, the worker that has to build
        :return: Direction, build direction
        """
        pass

    @abstractmethod
    def game_over(self, win):
        """
        Notify player that game has ended either by victory on either side or by
        player shutdown due to invalid move/build or connection lost.

        :param win: bool, True if this Player won the game, False otherwise
        """
        pass