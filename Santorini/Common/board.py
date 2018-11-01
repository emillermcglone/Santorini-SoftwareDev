# This file describes the high-level interactions that a `GameBoard` will be responsible for


# A BoardDict is a:
#   wrapper class around a dict that will ensure that lookups
#   will not exceed the maximal board game coordinates

# A Cell is one of:
# - Worker, a class representing a worker game piece
# - Building, a class representing a building game piece
# - None, representing an empty Cell

# A TurnPhase is one of:
# - "PLACE", representing the initial piece placement phase
# - "MOVE", representing the move phase of a player's turn
# - "BUILD", representing the build phase of a player's turn
# This file describes the high-level interactions that a `GameBoard` will be responsible for

from abc import ABC

from Common.cell import Cell


class GameBoard:
    """Class representing a Santorini game board"""

    def place_worker(self, pid, wid, x, y):
        """
        Places a worker with given pid and wid at the cell x,y

        :param pid: Identifies the player whose worker to place
        :type pid:  str
        :param wid: Identifies the worker to place
        :type wid:  int
        :param x:   Represents the x coordinate of the targeted board cell
        :type x:    int
        :param y:   Represents the y coordinate of the targeted board cell
        :type y:    int
        """
        pass

    def move_worker(self, x1, y1, x2, y2):
        """
        Moves a worker from x1,y1 to x2,y2.

        :param x1: Represents the x coordinate of the source board cell
        :type x1:  int
        :param y1: Represents the y coordinate of the source board cell
        :type y1:  int
        :param x2: Represents the x coordinate of the destination board cell
        :type x2:  int
        :param y2: Represents the y coordinate of the destination board cell
        :type y2:  int
        """
        pass


    def build_floor(self, x, y, n=1):
        """
        Adds 1 to the height of the Cell at x,y.

        :param x: Represents the x coordinate of the Worker board cell
        :type x:  int
        :param y: Represents the y coordinate of the Worker board cell
        :type y:  int
        :param n: Represents how many floors to build
        :type n:  int
        """
        pass


    def get_height(self, x, y):
        """
        Returns the height of the Cell at the given coordinates

        :param x: Represents the x coordinate of the Cell to get
        :type x:  int
        :param y: Represents the y coordinate of the Cell to get
        :type y:  int
        :return:  Height of the Cell
        :rtype    float
        """
        pass


    def get_player_id(self, x, y):
        """
        Gets the player ID for the given coordinates if there is one

        :param x: Represents the x coordinate of the Cell to get
        :type x:  int
        :param y: Represents the y coordinate of the Cell to get
        :type y:  int
        :return:  Player ID if there is one, else None
        :rtype    Optional[str]
        """
        pass


    def get_worker_id(self, x, y):
        """
        Gets the worker ID for the given coordinates if there is one

        :param x: Represents the x coordinate of the Cell to get
        :type x:  int
        :param y: Represents the y coordinate of the Cell to get
        :type y:  int
        :return:  Worker ID if there is one, else None
        :rtype    Optional[int]
        """
        pass


    def find_worker(self, pid, wid):
        """
        Method to find the x, y coordinates of the given Worker ID

        :param pid: Identifies the player whose worker to look up
        :type  pid: str
        :param wid: Identifies the worker to look up
        :type  wid: int
        :return:    x, y coordinate of the Worker, or None if it does not exist
        :rtype      Optional[Tuple[int, int]]
        """
        pass


    def find_player_workers(self, pid):
        """
        Find all workers of given player.

        :param pid: string, id of player
        :return: [(N, N), ...], positions of player's workers
        """
        pass


    def find_workers(self):
        """
        Method to find the x, y coordinates of all the workers on the board

        :return: x, y coordinates of the workers, or None if there are no workers
        :rtype   Optional[List[Tuple[int, int]]]
        """
        pass
