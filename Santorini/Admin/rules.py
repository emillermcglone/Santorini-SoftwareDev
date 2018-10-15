import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.components import IRules
from abc import ABC, abstractmethod
from Admin.components import Worker
from Admin.query_board import QueryBoard
from Common.components import Direction

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
        if not check_move(worker, move_direction):
           return False

        x, y = self.__board.get_worker_position(worker)  
        move_x, move_y = move_direction(x, y)
        build_x, build_y = build_direction(move_x, move_y)
        build_cell = self.__board.cell(build_x, build_y)

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
        players = { worker.player_id for worker in workers }

        first_player_workers = [w for w in workers if w.player_id is players[0]]
        second_player_workers = [w for w in workers if w.player_id is players[1]]
        
        # Winning case 1
        for worker in workers:
            if self._worker_reach_third(worker):
                return worker.player_id

        # Winning case 2
        first_player_cannot_move = all(map(self._worker_cannot_move, first_player_workers))
        second_player_cannot_move = all(map(self._worker_cannot_move, second_player_workers))
        if first_player_cannot_move:
            return players[1]

        if second_player_cannot_move:
            return players[0]

        # Winning case 3
        first_player_cannot_build = all(map(self._worker_cannot_build_after_move, first_player_workers))
        second_player_cannot_build = all(map(self._worker_cannot_build_after_move, second_player_workers))
        if first_player_cannot_build:
            return players[1]

        if second_player_cannot_build:
            return players[0]

        return -1


    def _worker_reach_third(self, worker):
        """
        Check in every direction if cell is not occupied and its height 
        is equal to height to win.

        :param worker: Worker, the worker to check
        :return: bool, True if worker can move to third floor, False otherwise
        """
        for direction in Direction:
            occupied = self.__board.occupied(worker.id, direction)
            height = self.__board.neighbor_height(worker.id, direction)
            if not occupied and height is self.height_to_win:
                return True

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