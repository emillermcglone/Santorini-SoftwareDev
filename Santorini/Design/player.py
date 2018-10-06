class IPlayer(ABC):
    """
    Player component for Santorini, and intermediary between administrative
    components and the player AI.
    """

    @abstractmethod
    def __init__(self, id, worker1_id, worker2_id):
        """"
        Initialize the Player with id, worker1_id, and worker2_id.

        :param id: N, id of Player
        :param worker1_id: N, the id of the Player's first worker 
        :param worker2_id: N, the id of the Player's second worker
        """
        pass

    @abstractmethod
    def prompt_place(self, board):
        """
        Provide coordinates to place one of the workers on the given board.

        :param board: [[Cell, ...], ...], the current board of the game
        :return: (N, (N, N)), the worker id, and the x and y coordinates
        """
        pass

    @abstractmethod
    def prompt_move(self, board, worker1, worker2):
        """
        Prompt the player for their move turn. 

        :param board: [[Cell, ...], ...], the current board of the game
        :param worker1: Worker, the first worker
        :param worker2: Worker, the second worker
        :return: (N, Direction), the worker id, move direction
        """
        pass

    @abstractmethod
    def prompt_build(self, board, worker):
        """
        Prompt the player for their build turn. 

        :param board: [[Cell, ...], ...], the current board of the game
        :param worker: Worker, the worker that was moved in that turn
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