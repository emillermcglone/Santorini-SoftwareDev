class IPlayer(ABC):
    """
    Player component for Santorini, and intermediary between administrative
    components and the actor
    """ 

    def __init__(self, board):
        """
        Initialize the player. 

        :param board: IQueryBoard, the state of the game
        """
        self.board = board

    @abstractmethod
    def prompt_place(self, workers):
        """
        Prompt the player for their place turn.

        :param workers: [N, ...], list of worker ids that belong to this player so far
        :return: (N, N), the x and y coordinates to place a new worker
        """
        pass

    @abstractmethod
    def prompt_move(self, workers):
        """
        Prompt the player for their move turn. 
        :param workers: [N, ...], list of worker ids player can move
        :return: (N, Direction), the worker id, move direction
        """
        pass


    @abstractmethod
    def prompt_build(self, worker):
        """
        Prompt the player for their build turn. 

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