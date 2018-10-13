from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    The Santorini strategy for place, move, and build. 
    """
    def __init__(self, board, workers, rules):
        """
        Initialize strategy.

        :param board: IQueryBoard, the state of the game
        :param workers: [N, ...], the list of worker ids to interact with
        :param rules: IRules, the rule checker for the given game
        """
        self.board = board
        self.workers = workers
        self.rules = rules


    def place(self):
        """
        The strategy to plan for the next worker place action for a player. 

        :return: (N, N), the x and y coordinates of the cell to place the worker on
        """
        pass

    def move(self):
        """
        The strategy to plan for the next move action for a player.

        :return: (N, Direction), the id of the worker to be moved and the direction to move in
        """
        pass

    def build(self, worker):
        """
        The strategy to plan for the next build action for a player.

        :param worker: N, the id of worker to build with
        :return: Direction, the direction to build in
        """
        pass


class PlaceStrategy(ABC):
    """
    Santorini strategy to plan for next worker place action for a player.
    """

    @abstractmethod
    def apply(self, board, workers, rules):
        """
        Apply the strategy to produce specifications for the next move. 

        :param board: IQueryBoard, the current board of the game
        :param workers: [N, ...], list of worker ids of player to be placed
        :param rules: Rules, the rule checker with standard Santorini rules
        :return: (N, N), the x and y coordinates to place a new worker
        """
        pass 
          

class MoveStrategy(ABC):
    """
    Santorini strategy to plan for next action for a player.
    """

    @abstractmethod
    def apply(self, board, workers, rules): 
        """
        Apply the strategy to produce specifications for the next move. 

        :param board: IQueryBoard, the current board of the game
        :param workers: [N, ...], list of worker ids of the player 
        :param rules: Rules, the rule checker with standard Santorini rules
        :return: (N, Direction), the worker id, move direction
        """
        pass


class BuildStrategy(ABC):
    """
    Build strategy in a Santorini game.
    """

    @abstractmethod
    def apply(self, board, worker, rules): 
        """
        Apply the strategy to produce specifications for next build.

        :param board: IQueryBoard, the current board of the game
        :param worker: N, id of worker to build with 
        :param rules: Rules, the rule checker with standard Santorini rules
        :return: Direction, build direction
        """
        pass