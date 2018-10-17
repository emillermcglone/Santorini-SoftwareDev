# this file represent what we expect a referee to look like
# We decided to keep this simple and have this class hold the
# required information to know if a requested action is valid#
# firstly based off of turn order and pahse of the game and then
# if the action is valid for that actually ask the RuleChecker if
# the action is valid considering the state of the board


class Referee():
    """
    Defines a Referee interface
    """
    def __init__(self, board, checker):
        """
        initilization setup to hold state

        checker: A Santorini RuleChecker that is used for logic
        board: A Santorini GameBoard that is used for state lookup
        players: List-of Player IDs
        current_player: player ID of the current player
        current_worker: assigned after a move is done
        cmd_handler: used to dispatch to appropriate function based of incoming action
        """
        pass

    def check(self, action):
        """
        Method to check if a given action is valid

        :param action:  JSON representing an action
        :return: Boolean representing whether the action was valid or not
        """
        pass
