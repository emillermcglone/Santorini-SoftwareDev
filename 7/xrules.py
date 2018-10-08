""" 
Implementations for common components.
"""

import copy
import fileinput, io, sys, json, os

from abc import ABC, abstractmethod
from enum import Enum

class IBoard(ABC):
    """
    IBoard is made of a zero-indexed 2D list of ICell for a Santorini game,
    and manages the placement of the game's pieces and its buildings. 
    No rules are baked into the board. The board is in charge of the game's pieces 
    and provide basic inquiries about its pieces.
    """

    @property
    @abstractmethod
    def board(self):
        """
        Provide a representation of the board.
        """
        pass

class IActionBoard(IBoard):
    """
    An action board handles placing and moving workers, and building floors on top of buildings. 
    No rules are baked into this board. This board is in charge of the game's pieces.
    """

    @abstractmethod
    def place(self, worker, x, y):
        """ 
        Place worker on position.

        :param worker: N, id of worker to be placed
        :param x: N, x coordinate
        :param y: N, y coordinate
        :raise ValueError: if id exists on board, or x and y are out of bounds
        """
        pass


    @abstractmethod
    def move(self, worker, move_direction):
        """ 
        Move worker to given direction.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        pass


    @abstractmethod
    def build(self, worker, build_direction):
        """
        Build a floor in the given direction.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        pass

class ICell(ABC):
    """
    Individual cell element with height on a Santorini board.
    """

    @property
    @abstractmethod
    def height(self):
        """
        Height of cell.
        """
        pass

    @height.setter
    @abstractmethod
    def height(self, new_height):
        """
        Set cell's height to new_height.

        :param new_height: the new height
        :raise ValueError: if given height is less than 0
        """
        pass

class IRules(ABC):
    """
    Set of rules for a Santorini game which both the administrative components
    and players can use to validate their moves before making them.
    """

    @abstractmethod
    def check_place(self, x, y):
        """
        Check if place request is valid.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: bool, True if valid, False otherwise
        """
        pass


    @abstractmethod
    def check_move(self, worker, move_direction):
        """
        Check if the move is valid.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        pass


    @abstractmethod
    def check_build(self, worker, build_direction):
        """
        Check if the build is valid.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        pass

class Direction(Enum):
    """
    Direction for moving or building in a zero-indexed 2D list of Cell where
    origin is on the top left corner. Going North means y - 1 and West means x - 1.
    Each Enum maps to a function of type (x, y: (N, N)) -> (N, N) that gives the next
    coordinates in its direction.
    """
    N = lambda x, y: (x, y - 1)
    S = lambda x, y: (x, y + 1)
    W = lambda x, y: (x - 1, y)
    E = lambda x, y: (x + 1, y)
    NW = lambda x, y: (x - 1, y - 1)
    NE = lambda x, y: (x + 1, y - 1)
    SW = lambda x, y: (x - 1, y + 1)
    SE = lambda x, y: (x + 1, y + 1)

    @staticmethod
    def compose(direction_1, direction_2):
        """
        Composes two direction functions.

        :param direction_1: Direction, first direction
        :param direction_2: Direction, second direction
        :return: (int, int) -> (int, int), composed direction function
        """
        def go(x, y):
            i, j = direction_1(x, y)
            return direction_2(i, j)

        return go

class Cell(ICell):
    """
    Individual cell element with height on a Santorini board.
    """

    def __init__(self, height = 0):
        """
        Initialize cell with height, defaults to 0.

        :param height: N, height of cell 
        :raise ValueError: if given height is less than 0
        """
        if height < 0: raise ValueError("Given height is less than 0")
        self.height = height

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        if new_height < 0: raise ValueError("Given height is less than 0")
        self._height = new_height

    def __repr__(self):
        return "{0} {1}".format(type(self).__name__, self.height)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.height == other.height
        

class Height(Cell):
    """
    Height of a building.
    """

class Worker(Cell):
    """
    Worker of a Santorini board whose height represents which floor
    it is on.
    """

    def __init__(self, worker_id, height = 0):
        """
        Initialize with id, position, and height of building the worker is on.

        :param worker_id: N, id of Worker
        :param position: (N, N), the position of Worker
        :param height: N, height of building worker is on, defaults to 0
        :raise ValueError: if height is not from 0 to 4        
        """
        super().__init__(height)
        self.id = worker_id


class ActionBoard(IActionBoard):
    
    def __init__(self, board=None, width=6, height=6):
        """
        Initialize board with the given dimensions, 6 x 6 by default. Board can
        be initialized with a given 2D list of Cells.

        :param board: [[Cell, ...], ...], a board to initialize from 
        :param width: N, number of cells horizontally
        :param height: N, number of cells vertically
        """
        self._width = width
        self._height = height
        self._board = self._complete(board) if board is not None else [[Height(0)] * width for _ in range(height)]


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
        return QueryBoard(self._board)


    def _get_worker_position(self, worker):
        for y, r in enumerate(self._board):
            for x, c in enumerate(r):
                if isinstance(c, Worker) and c.id == worker:
                    return x, y
        raise ValueError("Worker not found")

    def place(self, worker, x, y):
        if worker in self.query_board.workers:
            raise ValueError("Given id is already on the board")

        cell = self._cell(x, y)
        placed_worker = Worker(worker, cell.height)
        self._update(x, y, placed_worker)


    def move(self, worker, move_direction):
        x, y = self._get_worker_position(worker)
        to_x, to_y = move_direction(x, y)

        self._move(worker, to_x, to_y)

    def build(self, worker, build_direction):
        x, y = self._get_worker_position(worker)
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
        i, j = self._get_worker_position(worker_id)
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
        result += [[Height(0)] * self._width for _ in range(difference)] 
        result = list(map(lambda l: l + [Height(0)] * (self._width - len(l)), result))
        return result
            
       

"""
Test harness for SantoriniRules
"""

from splitstream import splitfile
from functools import reduce

"""
IQueryBoard provides components such as Player, Rules, and Strategy an interface to make
inquiries about game pieces. It does not mutate the state of the game.

The referee passes this board representation to components that need it to fulfill
their purpose. 
"""


class IQueryBoard(IBoard):
    """
    A query board provides an interface for components to inquire basic information
    on game pieces. 
    """

    @abstractmethod
    def cell(self, x, y):
        """
        Get a copy of the cell on the given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: ICell, the cell on given coordinates
        :raise ValueError: if given position is out of bounds
        """
        pass

    @abstractmethod
    def height(self, x, y):
        """
        Get the height of the cell on the given coordinates.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: N, the height of the cell
        :raise ValueError: if given position is out of bounds
        """
        pass

    @abstractmethod
    def neighbor(self, worker, direction):
        """
        Is there a cell in the given direction?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: bool, True if it is an empty cell, False otherwise
        """
        pass


    @abstractmethod
    def occupied(self, worker, direction):
        """
        Is the neighboring cell occupied by worker?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: bool, True if worker occupies neighbor, False otherwise
        :raise ValueError: if neighboring cell does not exist
        """
        pass


    @abstractmethod
    def neighbor_height(self, worker, direction):
        """
        What is the height of neigboring cell?

        :param worker: N, id of worker
        :param direction: Direction, direction of neighbor
        :return: N, the height of neighboring building
        :raise ValueError: if there's no neighboring cell
        """
        pass


    @property
    @abstractmethod
    def workers(self):
        """
        Provide the ids of every worker on the board.

        :return: [N, ...], ids of every worker on the board
        """
        pass


    @abstractmethod
    def get_worker_position(self, worker):
        """
        Get the position of given worker.

        :param worker: N, id of worker
        :return: (N, N), position of worker
        :raise ValueError: if worker is not found
        """
        pass         
       


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

class IRules(ABC):
    """
    Set of rules for a Santorini game which both the administrative components
    and players can use to validate their moves before making them.
    """

    @abstractmethod
    def check_place(self, x, y):
        """
        Check if place request is valid.

        :param x: N, x coordinate
        :param y: N, y coordinate
        :return: bool, True if valid, False otherwise
        """
        pass


    @abstractmethod
    def check_move(self, worker, move_direction):
        """
        Check if the move is valid.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        """
        pass


    @abstractmethod
    def check_build(self, worker, build_direction):
        """
        Check if the build is valid.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        """
        pass


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


def create_cell(cell):
    """
    Create the appropriate cell instance that is one of Worker or Height.

    :param cell: String | N, a buildingworker or height 
    """
    if isinstance(cell, str):
        height = int(cell[0])
        worker_id = cell[1:]
        return Worker(worker_id, height)
    else:
        return Height(cell)

def create_direction(direction):
    """
    Create the appropriate Direction for move or build.

    :param direction: [String, String], the test harness directions
    """

    directions = {
        "EAST": Direction.E, 
        "WEST": Direction.W,
        "NORTH": Direction.N,
        "SOUTH": Direction.S,
        "PUT": lambda x, y: (x, y)
    }

    east_west = directions[direction[0]]
    north_south = directions[direction[1]]

    return Direction.compose(east_west, north_south)

def create_board(state, request):
    """
    Translate test harness board to ActionBoard.

    :param state: {}, state of the turn action  
    :param request: [[Cell, ...], ...], the test harness board
    :return: IActionBoard, the query board
    """

    new_board = [[create_cell(c) for c in l] for l in request]
    state["action_board"] = ActionBoard(new_board)
    state["rules"] = SantoriniRules(state["action_board"].query_board)

def write(valid, output):
    """
    Write the output with a new line.

    :param valid: true | false, whether the turn action is valid or invalid
    """
    output.write(("yes" if valid else "no") + "\n")
    

def respond(state):
    """
    Respond to the requested action. 

    :param state: {}, state of the turn action
    """
    if state["move"] is None:
        return
    elif state["build"] is None:
        write(state["move"], state["output"])
    else:
        write(state["move"] and state["build"], state["output"])
    reset_state(state)

              
def move(state, request):
    """
    Check if the move request is valid and update the state.
    If the move is valid, move the worker in the direction given.

    :param state: {}, state of the turn action
    :param request: [String, String, String], the test harness check move request, worker, direction
    """
    worker = request[1]
    direction = create_direction(request[2])

    if state["rules"].check_move(worker, direction):
        state["action_board"].move(worker, direction)
        state["move"] = True
        state["moved_worker"] = worker
    else:
        state["move"] = False
        state["moved_worker"] = worker


def build(state, request):
    """
    Check if the build request is valid and update the state.

    :param state: {}, state of the turn action
    :param request: [String, String], the test harness check build request, direction
    """
    worker = state["moved_worker"]
    direction = create_direction(request[1])
    state["build"] = state["rules"].check_build(worker, direction)
    respond(state)


def handle_requests(state, request):
    """
    Handle the request, depending on whether it's check move, or check build. 

    :param state: {}, state of the turn action
    :param request: [String, String, String], the test harness check move request, worker, direction
    :param request: [String, String], the test harness check build request, direction
    """
    requests = { "move": move, "+build": build }
    requests[request[0]](state, request)


def reset_state(state):
    """
    Reset the state to None.

    :param state: {}, state of the turn action
    """
    state["action_board"] = None
    state["rules"] = None
    state["move"] = None
    state["build"] = None
    state["moved_worker"] = None


def main():
    output = open(sys.argv[2], 'w') if len(sys.argv) >= 3 else sys.stdout

    state = {
        "action_board": None,
        "rules": None,
        "move": None,
        "build": None,
        "moved_worker": None,
        "output": output
    }

    with fileinput.input() as f:
        inputs = reduce(lambda x, y: x + y, f)
        readable = io.BytesIO(inputs.encode())
        
        for json_input in splitfile(readable, format="json"):
            request = json.loads(json_input)
            if isinstance(request[0], list):
                respond(state)
                state["board"] = create_board(state, request)
            else:
                handle_requests(state, request)

    respond(state)
    output.close()
            
if __name__ == "__main__":
    main()