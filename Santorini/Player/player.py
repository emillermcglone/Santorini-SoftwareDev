class IPlayer(ABC):
    """
    Player component for Santorini, and intermediary between administrative
    components and the actor

    Log is a [Action, N, Direction], representing type of action, worker id, and direction of action
    Action is either "move" or "build"
    """
    
    @abstractmethod
    def __init__(self, place_strategy, move_strategy, build_strategy):
        """
        Initialize player with strategies for place, move, and build. 
        """
        pass
        

    @abstractmethod
    def prompt_place(self, board, workers):
        """
        Prompt the player for their place tu of worker ids player can move
        :param player_history: [Log, ...], logs of this player's actions
        :param opponent_history: [Log, ...], logs of opponent's actions
        :return: (N, Direction), the worker id, move direction
        """
        pass


    @abstractmethod
    def prompt_build(self, board, worker, player_history, opponent_history):
        """
        Prompt the player for their build turn. 

        :param board: IQueryBoard, the current board of the game
        :param worker: N, the worker that has to build
        :param player_history: [Log, ...], logs of this player's actions
        :param opponent_history: [Log, ...], logs of opponent's actions
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