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
    def __init__(self, player_1, player_2, checker, board=None):
        """
        initilization setup to hold state

        :param player_1: string, player 1 id
        :param player_2: string, player 2 id

        checker_cls: A Santorini RuleChecker class that is used for logic
        board: A Santorini GameBoard that is used for state lookup
        players: List-of Player IDs
        current_player: player ID of the current player
        current_worker: assigned after a move is done
        cmd_handler: used to dispatch to appropriate function based on incoming action
        """
        pass

    def run_games(self, best_of=1):
        """
        Run the game between the two players once or as many as the given 
        number of matches. 

        :param best_of: N, odd number of matches at least 1
        """
        pass


    def check(self, action):
        """
        Method to check if a given action is valid

        :param action:  JSON representing an action
        :return: Boolean representing whether the action was valid or not
        """
        pass
