# Class that checks to see if the requested move conforms to the rules

from Common.rule_checker import RuleChecker as IRuleChecker
from Lib.util import check_distance, get_adjacent



class RuleChecker(IRuleChecker):
    """Defines the Rule Checker interface"""

    def __init__(self, board):
        """
        Initializes a RuleChecker object with the given GameBoard

        :param board: The GameBoard
        :type board:  GameBoardThis 
        """
        # The GameBoard that the RuleChecker will be using for operations
        self.__board = board  # type: GameBoard

    def check_build(self, x1, y1, x2, y2):
        """
        Determines whether building at the
        given coordinate is valid

        :param pid: string, player id for build move
        :param wid: string, worker id for build move

        :param x1: Represents the x coordinate of the worker board cell
        :type x1:  int
        :param y1: Represents the y coordinate of the worker board cell
        :type y1:  int
        :param x2: Represents the x coordinate of the board cell to build
        :type x2:  int
        :param y2: Represents the y coordinate of the board cell to build
        :type y2:  int
        :return:   True if valid build, else False
        :rtype     bool
        """
        # Check that the source cell is valid
        # Check that the destination cell is valid
        # Check that the worker at origin belongs to given player
        # Check that the worker at origin has the right id
        # Check that there is not a worker in the board cell to build
        # Check that the worker is adjacent to the board cell to build
        # Check that the height of the targeted board cell is less than 4
        return self.check_valid_cell(x1, y1) \
               and self.check_valid_cell(x2, y2) \
               and not self.__board.get_player_id(x2, y2) \
               and check_distance(x1, y1, x2, y2) \
               and self.__board.get_height(x2, y2) < 4

    def check_move(self, x1, y1, x2, y2):
        """
        Determines whether moving a worker from the given
        coordinate to the other given coordinate is valid

        :param pid: string, player id for build move

        :param x1: Represents the x coordinate of the source board cell
        :type x1:  int
        :param y1: Represents the y coordinate of the source board cell
        :type y1:  int
        :param x2: Represents the x coordinate of the destination board cell
        :type x2:  int
        :param y2: Represents the y coordinate of the destination board cell
        :type y2:  int
        :return:   True if valid move, else False
        :rtype     bool
        """
        # Check that the source cell is valid
        # Check that the destination cell is valid
        # Check that the worker at origin belongs to given player
        # Check that the destination height is up to one higher than the source
        # Check that the destination does not already contain a player
        # Check that the worker is moving to an adjacent cell
        return self.check_valid_cell(x1, y1) \
               and self.check_valid_cell(x2, y2) \
               and self.__board.get_height(x2, y2) < 4 \
               and self.__board.get_height(x1, y1) + 1 >= self.__board.get_height(x2, y2) \
               and not self.__board.get_player_id(x2, y2) \
               and check_distance(x1, y1, x2, y2)


    def check_place(self, pid, wid, x, y):
        """
        Determines whether placing a worker
        at the given coordinates is valid

        :param pid: Identifies the player whose worker to place
        :type pid:  str
        :param wid: Identifies the worker to place
        :type wid:  int
        :param x:   Represents the x coordinate of the targeted board cell
        :type x:    int
        :param y:   Represents the y coordinate of the targeted board cell
        :type y:    int
        :return:    True if valid place, else False
        :rtype      bool
        """
        # Check that the worker ID is valid
        # Check that the destination cell is valid
        # Check that the destination does not already contain a player
        # Check that the given worker ID has not already been placed on the board
        return self.check_valid_cell(x, y) \
               and self.__board.get_player_id(x, y) is None \
               and self.__board.find_worker(pid, wid) is None

    def check_valid_cell(self, x, y):
        """
        Determines whether the given coordinates
        represent a valid cell on a GameBoard

        :param x: Represents the x coordinate of the targeted board cell
        :type x:  int
        :param y: Represents the y coordinate of the targeted board cell
        :type y:  int
        :return:  True if valid coordinates, else False
        :rtype    bool
        """
        # Check that the coordinates are between 0 and 5
        return x in range(0, 6) and y in range(0, 6)


    def check_game_over(self, player1, player2):
        """
        Determines the winner if the game is over

        :param player1: ID of the first player
        :type player1:  str
        :param player2: ID of the second player
        :type player2:  str
        :return:        Player ID if there is a winner, else None
        :rtype:         Optional[str]
        """
        # Get coordinates of all workers on the board
        for x1, y1 in self.__board.find_workers():
            height = self.__board.get_height(x1, y1)
            player = self.__board.get_player_id(x1, y1)
            wid = self.__board.get_worker_id(x1, y1)

            # Check if current worker is on the third floor
            if height is 3:
                return player

            # Assume there are no valid moves to start
            can_move = False

            # Assume there are no valid builds to start
            can_build = False

            # Iterate over all possible adjacent cells
            for x2, y2 in get_adjacent(x1, y1):

                # Determine whether the worker can move to this cell
                if self.check_move(x1, y1, x2, y2):

                    # The worker can make a valid move, game is not over
                    can_move = True

                # Determine whether the worker can build on this cell
                if self.check_build(x1, y1, x2, y2):
                    # The worker can make a valid build, game is not over
                    can_build = True

            # If the worker can't build or can't move, game is over
            if not (can_move and can_build):

                # The winner will be the other player
                if self.__board.get_player_id(x1, y1) == player1:
                    return player2
                return player1

        # Otherwise, the game is not over, so there is no winner
        return None
