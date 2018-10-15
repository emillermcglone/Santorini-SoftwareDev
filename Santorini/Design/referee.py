from abc import ABC, abstractmethod

class IReferee(ABC):
    """
    Referee that manages a game of Santorini between two players.
    It manages the board, passes the appropriate data to components that
    need them, and prompts the players for their moves.
    """

    @abstractmethod
    def start_game(self, player_1, player_2, rules, callback, timeout=5):
        """
        Start a game of Santorini given two players and the rules for the game.
         
        :param player_1: IPlayer, player 1, who goes first
        :param player_2: IPlayer, player 2
        :param rules: IRules, the rule checker for the given game
        :param callback: (N) -> void, function to call when game ends. Passes in winning player id.
        :param timeout: N, time limit for a turn
        """
        pass


    @abstractmethod
    def status_of_game(self):
        """
        Check the state of game.
        
        :return: N, winning player id, -1 if game continues
        """
        pass


    @abstractmethod
    def end_game(self):
        """
        End the game by notifying the players. 

        :return: N, id of winning player
        """
        pass