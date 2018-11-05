# Class that checks to see if the requested move conforms to the rules
from abc import ABC, abstractmethod


class RuleChecker(ABC):
    """Defines the Rule Checker interface"""

    @abstractmethod
    def check_build(self, x1, y1, x2, y2):
        """
        Determines whether building at the
        given coordinate is valid

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
        pass

    @abstractmethod
    def check_move(self, x1, y1, x2, y2):
        """
        Determines whether moving a worker from the given
        coordinate to the other given coordinate is valid

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
        pass


    @abstractmethod
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
        pass


    @abstractmethod
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
        pass


    @abstractmethod
    def get_winning_move(self, pid):
        """
        Get winning move.

        :param pid
        """
        pass
    

    @abstractmethod
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
        pass
