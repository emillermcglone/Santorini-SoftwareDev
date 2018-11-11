import names, sys
import copy

from Admin.game_over import GameOver, GameOverCondition
from Admin.referee import Referee

class TournamentManager:
    """
    Santorini tournament manager that runs games in a round robin fashion among 
    a fixed but arbitrary number of players. 

    Policy on Names If the tournament manager discovers that several players with the same name are to participate in a tournament, it picks a unique name for all but one of the players and informs these players of the chosen names.

    Policy on Broken Players When a tournament manager is informed that a player misbehaved, it acts as follows:

    - The player is removed from all future encounters; there are no second chances.

    - All past meet-ups involving the player are counted as won by the opponent.

    - If a player breaks after winning past games due to its opponents' breakage, the game is eliminated from the tournament evaluation.

    The End When the tournament is over, the tournament manager delivers two pieces of information:

    - The first is a list of names of players that misbehaved in any way. They are listed in the order of failure.

    - The second lists all completed games where each piece of game information lists the winner’s and the loser’s name. The games are listed in the order of "first plays against rest, second plays against rest, etc."
    """

    def __init__(self, configuration=None):
        """
        Initialize a tournament manager with configuration.

        :param configuration: Configuration, game configuration containing players
        """
        self.__players = configuration.players()
        self.__change_duplicate_ids(self.__players)

        self.__observers = configuration.observers()

        self.__misbehaved_players = []
        self.__meet_ups = []


    def players(self):
        return copy.deepcopy(self.__players)

    def observers(self):
        return copy.deepcopy(self.__observers)

    
    def __handle_misbehaving_player(self, player):
        """
        Add the player to the misbehaved players list,
        and change all past meet-ups involving the player to be counted as won by the opponent.

        If the player lost in a past meet up, nothing is changed in the meetup. 

        If a player breaks after winning past games due to its opponents' breakage, 
        the game is eliminated from the tournament evaluation.
        
        :param player: Player, the player that misbehaved
        """
        self.__misbehaved_players.append(player)

        new_meet_ups = []

        for meet_up in self.__meet_ups:
            winner = meet_up.winner
            loser = meet_up.loser
            condition = meet_up.condition

            if condition is GameOverCondition.LoserBrokeInTournament:
                continue

            if winner.get_id() is player.get_id():
                game_over = GameOver(loser, winner, GameOverCondition.LoserBrokeInTournament)
                new_meet_ups.append(game_over)
                continue

            new_meet_ups.append(meet_up)

        self.__meet_ups = new_meet_ups

    
    def __change_duplicate_ids(self, players):
        """
        Change the ids of duplicate players. 

        :param players: [Player, ...], list of Players 
        """

        players_set = set()

        for player in players:
            player_id = player.get_id()
            if player_id in players_set:
                new_id = names.get_first_name().lower()
                while new_id in players_set:
                    new_id = names.get_first_name().lower()
                player.set_id(new_id)
                player_id = new_id
            players_set.add(player_id)

            
    def run_tournament(self):
        """
        Run a round robin tournament with the players.

        Each meet-up between players runs a series of 3 Santorini games.

        :return: TournamentResult, result of tournament
        """
        for i in range(len(self.__players)):
            player_1 = self.__players[i]

            if player_1 in self.__misbehaved_players:
                continue

            for player_2 in self.__players[i + 1:]:
                if player_1 in self.__misbehaved_players:
                    break

                if player_2 in self.__misbehaved_players:
                    continue

                referee = Referee(player_1, player_2, time_limit=3, observers=self.__observers)
                game_result = referee.run_games(3)
                if game_result.condition is not GameOverCondition.FairGame:
                    self.__handle_misbehaving_player(game_result.loser)
                self.__meet_ups.append(game_result)

        meet_ups = list(map(lambda x: [x.winner.get_id(), x.loser.get_id()], self.__meet_ups))

        return [list(map(lambda x: x.get_id(), self.__misbehaved_players)), meet_ups]
                
                


