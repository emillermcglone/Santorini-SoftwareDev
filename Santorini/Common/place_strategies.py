import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math import hypot
from functools import reduce

from Design.strategy import PlaceStrategy
from Common.components import *


"""
A PlaceStrategy is a (IQueryBoard, [N, ...], IRules) -> (N, N)
which takes in the query board, list of player's workers, and the rules of the game.

It returns the coordinates to place a new worker on and
raises a ValueError if placing is impossible according to strategy.
"""

def place_first_diagonal_point(board, workers, rules):
    """
    Place the worker on the first point of the diagonal that is still free, 
    starting from (0,0).
    """
    coordinates = (0, 0)
    
    while True:
        if rules.check_place(*coordinates):
            return coordinates
        coordinates = Direction.SE(*coordinates)


def farthest_away_from_opponent(board, workers, rules):
    """
    Place the worker on a field that is as far away from the 
    other player’s worker(s) using the notion of geometric 
    distance on a Cartesian plane.
    """
    
    workers_on_board = list(map(lambda w: w.id, board.workers))
    opponent_workers = list(filter(lambda w: not w in workers, workers_on_board))
    opponent_worker_positions = list(map(lambda w: board.get_worker_positon(w), opponent_workers))

    width, height = board.dimensions

    farthest_point = None
    for x in range(width):
        for y in range(height):
            if rules.check_place(x, y) and total_distance((x, y), opponent_workers) >= total_distance(farthest_point, opponent_workers):
                farthest_point = (x , y)

    if farthest_point is None:
        raise ValueError("Strategy not applicable")
    
    return farthest_point

def total_distance(from_cell, to_cells):
    if from_cell is None: return 0
    return reduce(lambda x, y: x + cartesian_distance(from_cell, y), to_cells, 0)

def cartesian_distance(from_cell, to_cell):
    return hypot(to_cell[0] - from_cell[0], to_cell[1] - from_cell[1])
