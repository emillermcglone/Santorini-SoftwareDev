# This file describes the high-level interactions that a `GameBoard` will be responsible for

from collections import defaultdict

from Santorini.Common.cell import Cell


class GameBoard:
    """Class representing a Santorini game board"""

    def __init__(self):
        """
        Initializes this GameBoard with default values
        """
        # The dictionary backend mapping coordinate pairs to Cells
        self.__board = defaultdict(Cell)  # type: DefaultDict[Tuple[int, int], Cell]

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
        # Place the worker in the destination coordinates by setting its player_id and worker_id
        self.__get_cell(x, y).place_worker(pid, wid)

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
        # Get the origin Cell of the worker
        origin_cell = self.__get_cell(x1, y1)
        # Place the worker in the destination coordinates by setting its player_id and worker_id
        self.__get_cell(x2, y2).place_worker(origin_cell.player_id, origin_cell.worker_id)
        # Remove the worker from the origin Cell
        origin_cell.clear_worker()

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
        # Build onto the building at the given coordinates
        self.__get_cell(x, y).build(n)

    def __get_cell(self, x, y):
        """
        Looks up (x,y) in the board and returns the Cell

        :param x: Represents the x coordinate of the Cell to get
        :type x:  int
        :param y: Represents the y coordinate of the Cell to get
        :type y:  int
        :return:  Cell object at (x,y) in the board
        :rtype    Cell
        """
        return self.__board[(x, y)]

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
        return self.__get_cell(x, y).height

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
        return self.__get_cell(x, y).player_id

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
        return self.__get_cell(x, y).worker_id

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
        # Iterate over the entire __board
        for key, value in self.__board.items():
            # Search for a Cell with the given player_id and worker_id
            if value.player_id == pid and value.worker_id == wid:
                # Return its coordinates
                return key
        # Otherwise, there was no Cell matching the given player_id and worker_id
        return None

    def find_player_workers(self, pid):
        """
        Find all workers of given player.

        :param pid: string, id of player
        :return: [(N, N), ...], positions of player's workers
        """
        workers = []
        for key, value in self.__board.items():
            if value.player_id and value.player_id == pid:
                workers.append(key)
        return workers

    def find_workers(self):
        """
        Method to find the x, y coordinates of all the workers on the board

        :return: x, y coordinates of the workers, or None if there are no workers
        :rtype   Optional[List[Tuple[int, int]]]
        """
        workers = []
        # Iterate over the entire __board
        for key, value in self.__board.items():
            # Search for a Cell with the given player_id and worker_id
            if value.player_id:
                # Return its coordinates
                workers.append(key)
        # Otherwise, there was no Cell matching the given player_id and worker_id
        return workers
