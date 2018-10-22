from Design.referee import Referee

class SantoriniReferee(Referee):
    def __init__(self, board, checker):
        """
        initilization setup to hold state

        checker: A Santorini RuleChecker that is used for logic
        board: A Santorini GameBoard that is used for state lookup
        players: List-of Player IDs
        current_player: player ID of the current player
        current_worker: assigned after a move is done
        cmd_handler: used to dispatch to appropriate function based on incoming action
        """
        self.__board = board
        self.__checker = checker
        self.players = []
        self.current_player = self.players[0]
        self.current_worker = None
        
        

    def check(self, action):
        """
        Method to check if a given action is valid

        :param action:  JSON representing an action
        :return: Boolean representing whether the action was valid or not
        """
        action_type = action["type"]