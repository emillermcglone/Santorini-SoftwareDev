import copy, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Admin.components import *
from Common.query_board import IQueryBoard

from functools import reduce

class QueryBoard(IQueryBoard):
    def __init__(self, board):
        """
        Initialize the query board with the given board.

        :param board: [[ICell, ...], ...], a board to initialize from 
        """
        self._board = board
        self._height = len(board)
        self._width = len(board[0])


    def __str__(self):
        """
        The board's representation.
        """
        return str(self.board)


    @property
    def board(self):
        return copy.deepcopy(self._board)


    def cell(self, x, y):
        if (self._out_of_bounds(x, y)):
            raise ValueError("Given position is out of bounds")
        return self.board[y][x]


    def height(self, x, y):
        cell = self.cell(x, y)
        return cell.height


    def neighbor(self, worker, direction):
        x, y = self.get_worker_position(worker)

        try:
            cell = self._next_cell(x, y, direction)
        except ValueError:
            return False

        return True


    def occupied(self, worker, direction):
        x, y = self.get_worker_position(worker)

        try:
            cell = self._next_cell(x, y, direction)
        except ValueError:
            return False

        return isinstance(cell, Worker)


    def neighbor_height(self, worker, direction):
        x, y = self.get_worker_position(worker)
        cell = self._next_cell(x, y, direction)
        return cell.height


    @property
    def workers(self):
        """
        Extract ids of all workers in the board.
        
        :return: [N, ...], the ids of all workers
        """
        workers = []
        for row in self._board:
            for c in row:
                if isinstance(c, Worker):
                    workers.append(c.id)

        return workers


    def get_worker_position(self, worker):
        for y, r in enumerate(self._board):
            for x, c in enumerate(r):
                if isinstance(c, Worker) and c.id == worker:
                    return x, y
        raise ValueError("Worker not found")


    def _next_cell(self, x, y, direction):
        """ 
        Get the next cell in given direction.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :param direction: Direction, direction for next position
        :return: Cell, next cell
        """
        to_x, to_y = direction(x, y)
        return self.cell(to_x, to_y)
    

    def _out_of_bounds(self, x, y):
        """
        Check if given x and y are out of bounds.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: bool, True if given coordinates are out of bounds, False otherwise
        """
        return x < 0 or x >= self._width or y < 0 or y >= self._height