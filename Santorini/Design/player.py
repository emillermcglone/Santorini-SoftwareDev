# This file describes the high-level interactions that a `Player` will be responsible for


class Player:
    """
    Class representing a Player with a unique string identifier.

    Attributes:
        __player_id: Unique string identifying the Player
    """

    def __init__(self, player_id):
        """
        Initialize the Player object

        :param player_id: Unique ID for the Player
        """
        pass

    def get_id(self):
        """
        Getter for the Player's ID

        :return: String Player ID
        """
        pass

    def get_placement(self, board, wid, rule_checker):
        """
        Asks the player to place a worker on the board

        :param board: GameBoard, copy of the current state of the game
        :param wid: The ID of the worker the player is to place
        :param rule_checker: RuleChecker, rule checker for current game

        :return: JSON that represents a place_worker action
        """
        pass

    def get_move(self, board, rule_checker):
        """
        Asks the player to make a move

        :param board: GameBoard, copy of the current state of the game
        :param rule_checker: RuleChecker, rule checker for current game

        :return: JSON that represents a move action
        """
        pass

    def get_build(self, board, wid, rule_checker):
        """
        Asks the player to build a floor

        :param board: GameBoard, copy of the current state of the game
        :param wid: Worker ID of the worker that the player needs to build with
        :param rule_checker: RuleChecker, rule checker for current game

        :return: JSON that represents a build action
        """
        pass

    def game_over(self, status):
        """
        Alerts the player that the game is over with status

        :param status: one of "WIN" | "LOSE" depending on the outcome of the board
        """
        pass
