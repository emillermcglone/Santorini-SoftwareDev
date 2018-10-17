# Class that checks to see if the requested move conforms to the rules


class RuleChecker:
    """Defines the Rule Checker interface"""

    def __init__(self):
        pass

    def check_build(self, board, x, y):
        """
        Determines whether building at the
        given coordinate is valid

        :param board: A GameBoard object
        :param x: An integer representing the x coordinate
        :param y: An integer representing the x coordinate
        :return: True if valid build, else False
        """
        pass

    def check_move(self, board, x1, y1, x2, y2):
        """
        Determines whether moving a worker from the given
        coordinate to the other given coordinate is valid

        :param board: A GameBoard object
        :param x1: An integer representing the x coordinate of the source board cell
        :param y1: An integer representing the y coordinate of the source board cell
        :param x2: An integer representing the x coordinate of the destination board cell
        :param y2: An integer representing the y coordinate of the destination board cell
        :return: True if valid move, else False
        """
        pass

    def check_place(self, board, pid, wid, x, y):
        """
        Determines whether placing a worker
        at the given coordinates is valid

        :param board: A GameBoard object
        :param pid: A string identifying the player whose worker to place
        :param wid: A number that identifies the worker to place, either 1 or 2
        :param x: An integer representing the x coordinate of the targeted board cell
        :param y: An integer representing the y coordinate of the targeted board cell
        :return: True if valid place, else False
        """
        pass

    def check_valid_cell(self, x, y):
        """
        Determines whether the given coordinates
        represent a valid cell on a GameBoard

        :param x: An integer representing the x coordinate
        :param y: An integer representing the y coordinate
        :return: True if valid coordinates, else False
        """
        pass

    def get_winner(self, board):
        """
        Determines whether the game is over,
        and returns the winner if it is

        :param board: A GameBoard object
        :return: The string id of the winner if the game is over, else None
        """
        pass
