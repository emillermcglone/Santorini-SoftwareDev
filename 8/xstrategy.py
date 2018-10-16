import copy, os, sys, json, fileinput

from splitstream import splitfile
from functools import reduce
from enum import Enum

from abc import ABC, abstractmethod
""" 
Implementations for common components.
"""


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
        Set cell's height to new height.

        :param new_height: the new height
        :raise ValueError: if given height is less than 0
        """
        pass

class IRules(ABC):
    """
    Set of rules for a Santorini game which both the administrative components
    and players can use to validate their moves before making them.
    """

    @property
    @abstractmethod
    def max_height(self):
        """ N, maximum height of each building """
        pass

    @property
    @abstractmethod
    def height_to_win(self):
        """ N, height of worker to win the game """
        pass

    @property
    @abstractmethod
    def max_height_difference(self):
        """ N, maximum height difference to climb onto buildings """
        pass

    @property
    @abstractmethod
    def max_workers_per_player(self):
        """ N, maximum workers per player """
        pass

    @property
    @abstractmethod
    def max_workers(self):
        """ N, maximum workers in a game """
        pass

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
        :return, bool, True if valid, False otherwise
        """
        pass


    @abstractmethod
    def check_build(self, worker, build_direction):
        """
        Check if the build is valid.

        :param worker: N, id of worker
        :param build_direction: Direction, direction for build
        :return, bool, True if valid, False otherwise
        """
        pass

    @abstractmethod
    def check_move_and_build(self, worker, move_direction, build_direction):
        """
        Check if build after move is valid.

        :param worker: N, id of worker
        :param move_direction: Direction, direction for move
        :param build_direction: Direction, direction for build after move
        :return, bool, True if valid, False otherwise
        """
        pass

    @abstractmethod
    def is_game_over(self):
        """
        Check if game has ended.

        :return: N, id of player who won, -1 if game has not ended.
        """
        pass



class Direction(Enum):
    """
    Direction for moving or building in a zero-indexed 2D list of Cell where
    origin is on the top left corner. Going North means y - 1 and West means x - 1.
    Each Enum maps to a function of type (x, y: (N, N)) -> (N, N) that gives the next
    coordinates in its direction.
    """
    N = (lambda x, y: (x, y - 1),)
    S = (lambda x, y: (x, y + 1),)
    W = (lambda x, y: (x - 1, y),)
    E = (lambda x, y: (x + 1, y),)
    NW = (lambda x, y: (x - 1, y - 1),)
    NE = (lambda x, y: (x + 1, y - 1),)
    SW = (lambda x, y: (x - 1, y + 1),)
    SE = (lambda x, y: (x + 1, y + 1),)

    def __call__(self, *args, **kwargs):
        return self.value[0](*args, **kwargs)

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
        return isinstance(other, type(self)) and self.height == other.height
        

class Height(Cell):
    """
    Height of a building.
    """

class Worker(Cell):
    """
    Worker of a Santorini board whose height represents which floor
    it is on.
    """

    def __init__(self, worker_id, player_id, height = 0):
        """
        Initialize with id, position, and height of building the worker is on.

        :param worker_id: N, id of Worker
        :param player_id: N, id of this worker's player
        :param height: N, height of building worker is on, defaults to 0
        :raise ValueError: if height is not from 0 to 4        
        """
        super().__init__(height)
        self.id = worker_id
        self.player_id = player_id

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id and self.player_id == other.player_id


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
    def place(self, worker, player, x, y):
        """ 
        Place worker on position.

        :param worker: N, id of worker to be placed
        :param player: N, id of player of given worker
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


"""
Interface for a physical board with which Santorini components interact with.

ICell is an individual cell with height on the board.

N is a natural number
"""

class IQueryBoard(IBoard):
    """
    A query board provides an interface for components to inquire basic information
    on game pieces. 
    """

    @property
    def dimensions(self):
        """
        Dimensions of board.

        :return: (N, N), width and height of board
        """
        pass

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
        Deep copy of all workers on board.
        
        :return: [Worker, ...], deep copy of all workers
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
       

""" 
Common data and knowledge among administrative components and players
in a Santorini game.

Common data include physical game pieces, the rules of the game,
and the player interface.

N is a natural number. 
"""


class QueryBoard(IQueryBoard):
    def __init__(self, board):
        """
        Initialize the query board with the given board.

        :param board: [[ICell, ...], ...], a board to initialize from 
        """
        self.__board = board
        self._height = len(board)
        self._width = len(board[0])


    def __str__(self):
        """
        The board's representation.
        """
        return str(self.board)


    @property
    def board(self):
        return copy.deepcopy(self.__board)
        
    
    @property
    def dimensions(self):
        return (self._width, self._height)


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
        Deep copy of all workers on board.
        
        :return: [Worker, ...], deep copy of all workers
        """
        workers = []
        for row in self.__board:
            for c in row:
                if isinstance(c, Worker):
                    workers.append(copy.deepcopy(c))

        return workers


    def get_worker_position(self, worker):
        for y, r in enumerate(self.__board):
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
        self.__board = self._complete(board) if board is not None else [[Height(0)] * width for _ in range(height)]


    def __str__(self):
        """
        The board's representation.
        """
        return str(self.board)


    @property
    def board(self):
        return copy.deepcopy(self.__board)


    @property
    def query_board(self):
        return QueryBoard(self.__board)


    def _get_worker_position(self, worker):
        for y, r in enumerate(self.__board):
            for x, c in enumerate(r):
                if isinstance(c, Worker) and c.id == worker:
                    return x, y
        raise ValueError("Worker not found")

    def place(self, worker, player, x, y):
        placed_worker = Worker(worker, player)
        if placed_worker in self.query_board.workers:
            raise ValueError("Given id is already on the board")

        cell = self._cell(x, y)
        placed_worker.height = cell.height
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
        return self.__board[y][x]


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
        self.__board[y][x] = new_cell


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
            
       



class GameTree:
    def __init__(self, board, workers, rules):
        """
        Initialize the game tree. 

        :param board: IActionBoard, a board to make moves with
        :param workers: [N, ...], a list of the player's worker ids 
        :param rules: IRules, the rule checker for the given game                        
        """
        self._action_board = board
        self._query_board = self.action_board.query_board
        self._workers = workers
        self._rules = rules


    @property
    def board(self):
        return copy.deepcopy(self._board)

    @property
    def action_board(self):
        return copy.deepcopy(self._action_board)

    @property
    def query_board(self):
        return self._action_board.query_board

    @property
    def workers(self):
        return copy.deepcopy(self._workers)
        

    def survive(self, worker, move_direction, build_direction, rounds):
        """
        Can the player survive in the next number of specified rounds of play. 
        A round of play denotes any player taking any turn action.

        To ask if the player can survive is to ask if opponent can win in next round. 
        To ask if the player can win in next round is to ask if opponent can lose in next round.
        To ask if the player can lose is to ask if opponent can win in next round.

        :param worker: N, id of the worker
        :param move_direction: Direction, direction to move in 
        :param build_direction: Direction, direction to build in 
        :param rounds: N, number of rounds to survive in 
        :return: bool, True if survived, False otherwise
        """

        # Rounds is 0
        if rounds is 0:
            return True

        # Board has been won
        winner = self.winner_from_move(worker, move_direction)
        if not winner is -1:
            return self._is_my_worker(winner)

        # Can opponent win in the next N - 1 rounds?
        try:
            opponent_win = self.opponent_after_move_and_build(worker, move_direction, build_direction).can_win(rounds - 1)
            return not opponent_win
        except ValueError:
            return False

        return False

    def winner_from_move(self, worker, move_direction):
        """
        Check if the move will result in the given worker winning the game 
        
        :param worker: N, id of the worker
        :param move_direction: Direction, direction to move in 
        :return: N | -1, the id of the winning worker or -1, the game has not been won
        """

        if self._rules.check_move(worker, move_direction):

            action_copy = self.action_board
            rules_copy = SantoriniRules(action_copy.query_board)
            action_copy.move(worker, move_direction)
            return rules_copy.is_game_over()
        return -1
           
    def opponent_after_move_and_build(self, worker, move_direction, build_direction):
        """
        Get the gametree of the opponent after the given move and build have been executed 

        :param worker: N, id of the worker
        :param move_direction: Direction, direction to move in 
        :param build_direction: Direction, direction to build in 
        :return: GameTree, next node after move and build
        :raise ValueError: if move and build are invalid
        """
        if self._rules.check_move_and_build(worker, move_direction, build_direction):
            action_copy = self.action_board
            rules_copy = SantoriniRules(action_copy.query_board)
            action_copy.move(worker, move_direction)
            action_copy.build(worker, build_direction)
            return GameTree(action_copy, self._get_opponent_workers(), rules_copy)
        raise ValueError("Move and build are invalid")
        

    def _get_opponent_workers(self):
        """
        Get the workers of the opponent. 

        :return: [N, ...], list of opponent workers
        """
        opponent_workers = []
        for w in self.query_board.workers:
            if not w.id in self.workers:
                opponent_workers.append(w.id)
        return opponent_workers


    def _is_my_worker(self, winner):
        """
        Check if the winner of the game is one of the GameTree workers

        :param winner: N, id of winner
        :return: bool, True if winner is one of current player's workers, False otherwise
        """
        return winner in self.workers


    def can_win_or_lose(self, rounds, win):
        """
        Check if the player can win or lose in the next number of rounds. 
        Helper method for can_win and can_lose

        :param rounds: N, number of rounds
        :param win: bool, True to check for win, False to check for lose
        :return: bool, True if can win or lose, False otherwise
        """
        # Game has ended condition
        winner = self._rules.is_game_over()
        if not winner is -1:
            return not self._is_my_worker(winner) != win # Not Exclusive Or

        # Rounds is 0 condition
        if rounds is 0:
            return False

        # Rounds is more than 0
        for w in self.workers:
            for move_direction in Direction:
                # See if our move will lead to opponent losing 
                winner = self.winner_from_move(w, move_direction)
                
                if not winner is -1:
                    return not self._is_my_worker(winner)

                

                # See if our move and build will lead to opponent losing 
                for build_direction in Direction:
                    try:
                        node = self.opponent_after_move_and_build(w, move_direction, build_direction)
                        opponent = node.can_win(rounds - 1) if win else node.can_lose(rounds - 1)
                        return not opponent
                    except:
                        return False



    def can_win(self, rounds):
        """
        Can any one of player's turns lead to a win?
        """
        return self.can_win_or_lose(rounds, True)


    def can_lose(self, rounds):
        """
        Can the given turn lead to a loss?
        """
        return self.can_win_or_lose(rounds, False)


def create_board(board):
    """
    Translate test harness board to Santorini board.

    :param board: [[Cell, ...], ...], the test harness board
    :return: Board, instance of Santorini board
    """

    new_board = [[create_cell(c) for c in l] for l in board]
    return ActionBoard(new_board)



def create_cell(cell):
    """
    Create the appropriate cell instance that is one of Worker or Height.

    :param cell: String | N, a buildingworker or height 
    """
    if isinstance(cell, str):
        height = int(cell[0])
        player = cell[1:-1]
        worker_id = cell[1:]
        return Worker(worker_id, player, height)
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
        self.__board = query_board


    @property
    def max_height(self):
        return 4


    @property
    def height_to_win(self):
        return 3


    @property
    def max_height_difference(self):
        return 1


    @property
    def max_workers_per_player(self):
        return 2


    @property
    def max_workers(self):
        return self.max_workers_per_player * 2


    def check_place(self, x, y):
        """
        True if:
        - destination height is 0
        - destination has not been taken by another worker
        - number of workers does not exceed four.
        - x and y are valid coordinates on the board
        """

        try:
            cell = self.__board.cell(x, y)
            number_of_workers = len(self.__board.workers)
        except ValueError:
            return False

        return cell.height == 0 and not isinstance(cell, Worker) and number_of_workers < self.max_workers


    def check_move(self, worker, move_direction):
        """
        True if:
        - destination cell is not occupied
        - destination cell is at most a floor higher
        - destination cell's height is not four
        - destination cell exists
        """
        try:
            x, y = self.__board.get_worker_position(worker)
            height = self.__board.height(x, y)

            occupied = self.__board.occupied(worker, move_direction)
            neighbor_height = self.__board.neighbor_height(worker, move_direction)

            height_difference = neighbor_height - height
        except ValueError:
            return False

        return not occupied and neighbor_height < self.max_height and height_difference <= self.max_height_difference

    def check_build(self, worker, build_direction):
        """
        True if:
        - destination cell does not have worker
        - destination cell's height is below four
        - destination cell exists
        """
        try:
            occupied = self.__board.occupied(worker, build_direction)
            neighbor_height = self.__board.neighbor_height(worker, build_direction)
        except ValueError:
            return False

        return not occupied and neighbor_height < self.max_height

    def check_move_and_build(self, worker, move_direction, build_direction):
        """
        True if move and build are valid
        """
        if not self.check_move(worker, move_direction):
           return False

        x, y = self.__board.get_worker_position(worker)  
        move_x, move_y = move_direction(x, y)
        build_x, build_y = build_direction(move_x, move_y)

        try:
            build_cell = self.__board.cell(build_x, build_y)
        except:
            return False

        if isinstance(build_cell, Worker) or build_cell.height >= self.max_height:
            return False
       
        return True


    def is_game_over(self):
        """
        A game ends when:
        1. a player's worker CAN reach the third level of a building; or
        2. a player can't move any worker to at least a two-story (or shorter) building; or
        3. a player can move a worker but not add a floor to a building after

        In the first case, the active player is the winner of the game, 
        in the last two cases the opponent is the winner.
        """
        workers = self.__board.workers
        players_set = { worker.player_id for worker in workers }
        players = list(players_set)

        first_player_workers = [w for w in workers if w.player_id is players[0]]
        second_player_workers = [w for w in workers if w.player_id is players[1]]
        
        # Winning case 1
        for worker in workers:
            if self._worker_reach_third(worker):
                return worker.player_id

        # Winning case 2
        winner_case_2 = self._get_winner_from_condition(
            (players[0], first_player_workers), (players[1], second_player_workers), self._worker_cannot_move)
        if not winner_case_2 is None: return winner_case_2

        # Winning case 3
        winner_case_3 = self._get_winner_from_condition(
            (players[0], first_player_workers), (players[1], second_player_workers), self._worker_cannot_build_after_move)
        if not winner_case_3 is None: return winner_case_3

        return -1

    def _get_winner_from_condition(self, first_workers, second_workers, condition):
        """
        Get winner if any of the player's workers satisfy the loss condition.

        :param first_workers: (N, [N, ...]), first player id and list of worker ids
        :param second_workers: (N, [N, ...]), second player id and list of worker ids
        :param condition: (N) -> bool, loss condition
        """
        first_player_cannot_build = all(map(condition, first_workers[1]))
        second_player_cannot_build = all(map(condition, second_workers[1]))
        if first_player_cannot_build:
            return second_workers[0]

        if second_player_cannot_build:
            return first_workers[0]
        
        return None


    def _worker_reach_third(self, worker):
        """
        Check in every direction if cell is not occupied and its height 
        is equal to height to win.

        :param worker: Worker, the worker to check
        :return: bool, True if worker can move to third floor, False otherwise
        """
        for direction in Direction:
            try:
                occupied = self.__board.occupied(worker.id, direction)
                height = self.__board.neighbor_height(worker.id, direction)
                if not occupied and height is self.height_to_win:
                    return True
            except:
                continue

        return False

    def _worker_cannot_move(self, worker):
        """
        Check if worker cannot move anywhere.

        :param worker: Worker, the worker to check
        :return: bool, True if worker cannot move, False otherwise
        """
        stuck = [not self.check_move(worker.id, move) for move in Direction]
        return all(stuck)


    def _worker_cannot_build_after_move(self, worker):
        """
        Check if worker can move but cannot build anywhere after.

        :param worker: Worker, the worker to check
        :return: bool, True if worker cannot build after move, False otherwise
        """
        stuck = [not self.check_move_and_build(worker.id, move, build) for build in Direction for move in Direction]
        return all(stuck)

def get_player_workers(board, player):
    workers = board.workers
    return list(filter(lambda w: player in w.id, workers))


def move_and_build(player, board, worker, move_direction, build_direction, rounds):
    query_board = board.query_board
    workers = get_player_workers(query_board, player)
    worker_ids = list(map(lambda w: w.id, workers))
    game_tree = GameTree(board, worker_ids, SantoriniRules(query_board))

    survived = game_tree.survive(player + str(worker), move_direction, build_direction, rounds)
    return "yes" if survived else "no"


def main():
    output = open(sys.argv[2], 'w') if len(sys.argv) >= 3 else sys.stdout
    player = ""
    worker = 0
    move_direction = None
    build_direction = None
    rounds = 0


    with fileinput.input() as f:
        
        inputs = reduce(lambda x, y: x + y, f)
        for request in get_jsons(inputs):
            if isinstance(request, str):
                player = request
            elif isinstance(request, int):
                rounds = request
            elif request[0] == "move":
                worker = request[1][-1:]
                move_direction = create_direction(request[2])
            elif request[0] == "+build":
                build_direction = create_direction(request[1])
            else:
                board = create_board(request)

    output.write(move_and_build(player, board, worker, move_direction, build_direction, rounds))

def get_jsons(string):
    jsons = []
    acc = ""
    for c in string:
        acc += c
        try:
            obj = json.loads(acc)
            acc = ""
            jsons.append(obj)
        except:
            continue
    return jsons


            
if __name__ == "__main__":
    main()