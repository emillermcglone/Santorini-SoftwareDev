from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Santorini strategy to plan for next action for a player.

    Requires:
    - Worker ids
    - What kind of turn
    - State of game 
    - Rules
    - History of opponent and actor's moves
    """

    @abstractmethod
    def apply(self, board, workers, rules, history):
        pass
