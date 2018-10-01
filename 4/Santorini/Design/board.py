"""
Board is made of a zero-indexed 2D list of Cell for a Santorini game,
and manages the placement of the game's pieces and its buildings. 

Cell is either Height or Worker
Height signifies a building floor: N, 0 to 4 inclusive
Worker has id: N, position: (N, N), and height: N, 0 to 4 inclusive
N is a natural number
Height of 0 signifies the ground floor 

Direction is an Enum, one of N, E, S, W, NE, NW, SE, SW
"""

import copy

from Common.common.components import *
from abc import ABC, abstractmethod

class Board():
    def __init__(self, rules, board=None, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default, and
        list of game rules.

        :param rules: Rules, the rule checking interface
        :param board: [[Cell, ...], ...], a board to initialize from 
        :param width: N, number of cells horizontally
        :param height: N, number of cells vertically
        """
        self._width = width
        self._height = height
        self._rules = rules
        self._board = self.complete(board, width, height) if board is not None else [[Height(0)] * width] * height


    def complete(self, board, width, height):
        """
        Complete the board with trailing unoccupied Cells if dimensions
        are not width x height.

        :param board: [[Cell, ...], ...], the incomplete board
        :param width: N, the width of a complete board
        :param height: N, the height of a complete board
        """
        result = board
        difference = height - len(result)
        result += [[Height(0)] * width] * difference
        result = list(map(lambda l: l + [Height(0)] * (width - len(l)), result))
        return result

    def __str__(self):
        """
        The board's representation.
        """
        return str(self.board)


    def is_game_over(self, win_condition):
        """
        Check if game has been won.

        :param win_condition: (board: [[Cell, ...] ...]) -> N | -1, returns id of winning worker, -1 if game continues
        :return: N | -1, id of winning worker or -1 if game continues
        """
        return win_condition(self.board)

    @property
    def board(self):
        """
        Provide a deep copy of the board representing state of game.

        :return: [[Cell, ...] ...], the state of the game
        """
        return copy.deepcopy(self._board)

    @property
    def rules(self):
        """ 
        Provide a deep copy of the rules interface.

        :return: Rules, the rules of the game
        """
        return copy.deepcopy(self._rules)

    def cell(self, x, y):
        """
        Get a copy of the cell on the given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: Cell, the cell on given coordinates
        :raise ValueError: if given position is out of bounds
        """

        if (x < 0 or x >= self._width or y < 0 or y >= self._height):
            raise ValueError("Given position is out of bounds")
        return self.board[y][x]


    def neighbor(self, worker, direction):
        """
        Is there a cell in the given direction?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: bool, True if it is an empty cell, False otherwise
        """
        x, y = self.get_worker_position(worker)
        
        try:    
            cell = self._next_cell(x, y, direction)
        except ValueError:
            return False
        
        return True


    def occupied(self, worker, direction):
        """
        Is the neighboring cell occupied by worker?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: bool, True if worker occupies neighbor, False otherwise
        """
        x, y = self.get_worker_position(worker)
        
        try:
            cell = self._next_cell(x, y, direction)
        except ValueError:
            return False
        
        return isinstance(cell, Worker)


    def height(self, worker, direction):
        """
        What is the height of neigboring cell?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: N, the height of neighboring building
        :raise ValueError: if there's no neighboring cell
        """

        x, y = self.get_worker_position(worker)
        cell = self._next_cell(x, y, direction)
        return cell.height

    def get_worker_position(self, worker):
        """
        Get the position of given worker.

        :param worker: N, id of worker
        :return: (N, N), position of worker
        :raise ValueError: if worker is not found
        """
        for y, r in enumerate(self._board):
            for x, c in enumerate(r ):
                if isinstance(c, Worker) and c.id == worker:
                    return x, y
        raise ValueError("Worker not found")

    def place_worker(self, worker, x, y):
        """ 
        Place worker on position.

        :param worker: N, id of worker to be placed
        :param x: N, x coordinate
        :param y: N, y coordinate
        :raise ValueError: if another worker is on position
        """
        cell = self.cell(x, y)
        if isinstance(cell, Worker):
            raise ValueError("Another worker is on position")
        placed_worker = Worker(worker, cell.height)
        self._update(x, y, placed_worker)

    def move(self, worker, move_direction):
        """ 
        Move worker to given direction if rules are satisfied.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        if not self.rules.check_move(self.board, worker, move_direction):
            raise ValueError("Move is invalid")

        x, y = self.get_worker_position(worker)
        to_x, to_y = move_direction(x, y)
        
        self._move(worker, to_x, to_y)


    def build(self, worker, build_direction):
        """
        Build a floor in the given direction if rules are satisfied.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        if not self.rules.check_build(self.board, worker, build_direction):
            raise ValueError("Build is invalid")

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
        if (x < 0 or x >= self._width or y < 0 or y >= self._height):
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
        self.cell(x, y)
        self._board[y][x] = new_cell


    def _move(self, worker_id, x, y):
        """
        Moves the given worker to the new position.

        :param worker_id: N, id of worker to be moved
        :param x: N, x coordinate
        :param y: N, y coordinate
        """
        to_cell = self.cell(x, y)
        
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