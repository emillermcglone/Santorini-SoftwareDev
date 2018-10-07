import copy, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Admin.components import *
from Design.action_board import IActionBoard
from Admin.query_board import QueryBoard

class ActionBoard(IActionBoard):
    
    def __init__(self, board=None, width=6, height=6):
        self._width = width
        self._height = height
        self._board = self._complete(board) if board is not None else [[Height(0)] * width] * height


    def __str__(self):
        """
        The board's representation.
        """
        return str(self.board)


    @property
    def board(self):
        return copy.deepcopy(self._board)


    @property
    def query_board(self):
        return QueryBoard(self.board)


    def get_worker_position(self, worker):
        for y, r in enumerate(self._board):
            for x, c in enumerate(r):
                if isinstance(c, Worker) and c.id == worker:
                    return x, y
        raise ValueError("Worker not found")

    def place(self, worker, x, y):
        cell = self._cell(x, y)
        placed_worker = Worker(worker, cell.height)
        self._update(x, y, placed_worker)

    def move(self, worker, move_direction):
        x, y = self.get_worker_position(worker)
        to_x, to_y = move_direction(x, y)

        self._move(worker, to_x, to_y)

    def build(self, worker, build_direction):
        x, y = self.get_worker_position(worker)
        to_x, to_y = build_direction(x, y)

        self._build(to_x, to_y)

    def _cell(self, x, y):
        """
        Get the cell on given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: Cell, the cell on given coordinates
        :raise ValueError: if given position is out of bounds
        """
        if (self._out_of_bounds(x, y)):
            raise ValueError("Given position is out of bounds")
        return self._board[y][x]


    def _next_cell(self, x, y, direction):
        """ 
        Get the next cell in given direction.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :param direction: Direction, direction for next position
        :return: Cell, next cell
        """
        to_x, to_y = direction(x, y)
        return self._cell(to_x, to_y)


    def _update(self, x, y, new_cell):
        """
        Update the cell with the given new cell.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :param new_cell: Cell, new cell
        :raise ValueError: if cell is not of type Cell
        """
        if not isinstance(new_cell, Cell):
            raise ValueError("Given cell is not of type Cell")
        elif (self._out_of_bounds(x, y)):
            raise ValueError("Given position is out of bounds")
        self._board[y][x] = new_cell


    def _move(self, worker_id, x, y):
        """
        Moves the given worker to the new position.

        :param worker_id: N, id of worker to be moved
        :param x: N, x coordinate
        :param y: N, y coordinate
        """
        to_cell = self._cell(x, y)

        # Updates from cell
        i, j = self.get_worker_position(worker_id)
        worker = self._cell(i, j)
        self._update(i, j, Height(worker.height))

        # Updates to cell / move worker to cell
        to_height = to_cell.height
        worker.height = to_height
        self._update(x, y, worker)


    def _build(self, x, y):
        """
        Builds another floor onto the building on given position

        :param x: N, x coordinate
        :param y: N, y coordinate
        """
        to_cell = self._cell(x, y)
        self._update(x, y, Height(to_cell.height + 1))


    def _out_of_bounds(self, x, y):
        """
        Check if given x and y are out of bounds.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: bool, True if given coordinates are out of bounds, False otherwise
        """
        return x < 0 or x >= self._width or y < 0 or y >= self._height


    def _complete(self, board):
        """
        Complete the board with trailing unoccupied Cells if dimensions
        are not width x height. If board's dimensions exceed current width and
        height, width and height are set to the given board's dimensions.

        :param board: [[Cell, ...], ...], the incomplete board
        """
        max_height = len(board)
        max_width = max(map(len, board))

        if max_height > self._height: 
            self._height = max_height

        if max_width > self._width:
            self._width = max_width
        
        result = board
        difference = self._height - len(result)
        result += [[Height(0)] * self._width] * difference
        result = list(map(lambda l: l + [Height(0)] * (self._width - len(l)), result))
        return result
            
       