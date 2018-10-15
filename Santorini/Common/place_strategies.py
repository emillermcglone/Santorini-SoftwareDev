import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math import hypot
from functools import reduce

from Design.strategy import TurnStrategy, PlaceStrategy
from Common.components import *

class StrategyBackup(TurnStrategy):
    """
    Strategy with a list of turn strategies.
    """
    def __init__(self, *args):
        """
        Initialize strategy with list of strategies

        :param args: (TurnStrategy, ...), strategies to be used
        """
        self.strategies = list(args)


    def strategize(self, board, workers, rules):
        """
        Apply each strategy sequentially until a valid turn specification is given.
        """
        for strategy in self.strategies:
            try:
                specification = strategy.strategize(board, workers, rules)
                return specification
            except:
                continue
        raise ValueError("No valid strategy to apply")
        

class PlaceOnFirstDiagonalPoint(StrategyBackup, PlaceStrategy):
    """
    Place the worker on the first point of the diagonal that is still free, 
    starting from (0,0).
    """

    def strategize(self, board, workers, rules):
        coordinates = (0, 0)
    
        while True:
            if rules.check_place(*coordinates):
                return coordinates
            coordinates = Direction.SE(*coordinates)

class FarthestFromOpponent(StrategyBackup, PlaceStrategy):
    """
    Place the worker on a field that is as far away from the 
    other player’s worker(s) using the notion of geometric 
    distance on a Cartesian plane.
    """


    def strategize(self, board, workers, rules):
        workers_on_board = list(map(lambda w: w.id, board.workers))
        opponent_workers = list(filter(lambda w: not w in workers, workers_on_board))
        opponent_worker_positions = list(map(lambda w: board.get_worker_positon(w), opponent_workers))

        width, height = board.dimensions

        farthest_point = None
        for x in range(width):
            for y in range(height):
                if rules.check_place(x, y) and self._total_distance((x, y), opponent_workers) >= self._total_distance(farthest_point, opponent_workers):
                    farthest_point = (x , y)

        if farthest_point is None:
            raise ValueError("Strategy not applicable")
    
        return farthest_point
        
    def _total_distance(from_cell, to_cells):
        if from_cell is None: return 0
        return reduce(lambda x, y: x + self._cartesian_distance(from_cell, y), to_cells, 0)

    def _cartesian_distance(from_cell, to_cell):
        return hypot(to_cell[0] - from_cell[0], to_cell[1] - from_cell[1])

