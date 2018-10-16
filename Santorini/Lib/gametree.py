import copy, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.components import *
from action_board import ActionBoard
from Admin.rules import SantoriniRules


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