from abc import ABC, abstractmethod

class PlaceStrategy(ABC):
    """
    Santorini strategy to plan for next worker place action for a player.
    """

    @abstractmethod
    def apply(self, board, workers, rules):
        """
        Apply the stratgy to produce specifications for the next move. 

        :param board: IQueryBoard, the current board of the game
        :param workers: [N, ...], list of worker ids of player to be placed
        :param rules: Rules, the rule checker with standard Santorini rules
        """
        pass 
          

class MoveStrategy(ABC):
    """
    Santorini strategy to plan for next action for a player.

    Log is a [Action, N, Direction], representing type of action, worker id, and direction of action
    Action is either "move" or "build"
    """

    @abstractmethod
    def apply(self, board, workers, rules, player_history, opponent_history): 
        """
        Apply the stratgy to produce specifications for the next move. 

        :param board: IQueryBoard, the current board of the game
        :param workers: [N, ...], list of worker ids of the player 
        :param rules: Rules, the rule checker with standard Santorini rules
        :param player_history: [Log, ...], logs of this player's actions
        :param opponent_history: [Log, ...], logs of opponent's actions
        """
        pass


class BuildStrategy(ABC):
    """
    Build strategy in a Santorini game.
    """

    @abstractmethod
    def apply(self, board, worker, rules, player_history, opponent_history): 
        """
        Apply the strategy to produce specifications for next build.

        :param board: IQueryBoard, the current board of the game
        :param worker: N, id of worker to build with 
        :param rules: Rules, the rule checker with standard Santorini rules
        :param player_history: [Log, ...], logs of this player's actions
        :param opponent_history: [Log, ...], logs of opponent's actions
        """
        pass