# This file describes the high-level interactions that a `Cell` will be responsible for


class Cell:
    """Class representing a Cell."""

    def __init__(self):
        """Initializes the Cell object"""
        # If None, there is no worker in this Cell, else, the ID of the player the worker belongs to
        self.player_id = None  # type: Optional[str]
        # If None, there is no worker in this cell, else, a worker ID
        self.worker_id = None  # type: Optional[int]
        # If zero, this is no building in this Cell, else, the height of the building
        self.height = 0  # type: int

    def place_worker(self, player_id, worker_id):
        """
        Places a worker in the Cell object

        Note: Mutates self.player_id and self.worker_id

        :param player_id: ID of the player
        :type player_id:  str
        :param worker_id: ID of the worker
        :type worker_id:  int
        """
        self.player_id = player_id
        self.worker_id = worker_id

    def clear_worker(self):
        """
        Removes a worker from the Cell object

        Note: Mutates self.player_id and self.worker_id
        """
        self.player_id = None
        self.worker_id = None

    def build(self, n):
        """
        Increases the size of the building by one

        Note: Mutates self.height by n

        :param n: Amount to change height by
        """
        self.height += n
