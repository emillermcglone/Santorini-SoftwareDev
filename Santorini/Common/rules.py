import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import IRules
from abc import ABC, abstractmethod
from Admin.components import Worker
from Admin.query_board import QueryBoard

class SantoriniRules(IRules):
    """
    Rule checker with standard santorini rules. 
    """

    def __init__(self, query_board):
        """
        Initializes rules with a query board with which this checker
        checks the validity of player moves.

        :param query_board: IQueryBoard, the query board / state of game
        """
        self._board = query_board


    def check_place(self, x, y):
        """
        True if:
        - destination height is 0
        - destination has not been taken by another worker
        - number of workers does not exceed four.
        - x and y are valid coordinates on the board
        """

        try:
            cell = self._board.cell(x, y)
            number_of_workers = len(self._board.workers)
        except ValueError:
            return False

        return cell.height == 0 and not isinstance(cell, Worker) and number_of_workers < 4


    def check_move(self, worker, move_direction):
        """
        True if:
        - destination cell is not occupied
        - destination cell is at most a floor higher
        - destination cell's height is not four
        - destination cell exists
        """
        try:
            x, y = self._board.get_worker_position(worker)
            height = self._board.height(x, y)

            occupied = self._board.occupied(worker, move_direction)
            neighbor_height = self._board.neighbor_height(worker, move_direction)

            height_difference = neighbor_height - height
        except ValueError:
            return False

        return not occupied and neighbor_height < 4 and height_difference <= 1

    def check_build(self, worker, build_direction):
        """
        True if:
        - destination cell does not have worker
        - destination cell's height is below four
        - destination cell exists
        """
        try:
            occupied = self._board.occupied(worker, build_direction)
            neighbor_height = self._board.neighbor_height(worker, build_direction)
        except ValueError:
            return False

        return not occupied and neighbor_height < 4
