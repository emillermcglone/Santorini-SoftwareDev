import names, sys
import copy

from Admin.game_over import GameOver, GameOverCondition
from Admin.referee import Referee
from Admin.configurations.stdin_configuration import STDINConfiguration

class TournamentManager:
    """
    Santorini tournament manager that runs games in a round robin fashion among 
    a fixed but arbitrary number of players. 

    Policy on Names If the tournament manager discovers that several players with the same name are to participate in a tournament, it picks a unique name for all but one of the players and informs these players of the chosen names.

    Policy on Broken Players 
    When a tournament manager is informed that a player misbehaved, it acts as follows:

    - The player is removed from all future encounters; there are no second chances.

    - All past meet-ups involving the player are counted as won by the opponent.

    - If a player breaks after winning past games due to its opponents' breakage, the game is eliminated from the tournament evaluation.

    The End When the tournament is over, the tournament manager delivers two pieces of information:

    - The first is a list of names of players that misbehaved in any way. They are listed in the order of failure.

    - The second lists all completed games where each piece of game information lists the winner’s and the loser’s name. The games are listed in the order of "first plays against rest, second plays against rest, etc."
    """

    def __init__(self, configuration=STDINConfiguration()):
        """
        Initialize a tournament manager with configuration.

        :param configuration: Configuration, game configuration containing players
        """
        self.__players = configuration.players()
        self.__observers = configuration.observers()

        self.__change_duplicate_ids(self.__players)
        self.__misbehaved_players = []
        self.__meet_ups = []


    def players(self):
        """
        Get the players in this tournament

        :return: [Player, ...], all the players in this tournament
        """
        return copy.deepcopy(self.__players)


    def observers(self):
        """
        Get the observers in this tournament

        :return: [Observer, ...], all the observers in this tournament
        """
        return copy.deepcopy(self.__observers)

   
    def run_tournament(self):
        """
        Run a round robin tournament with the players.

        Each meet-up between players runs a series of 3 Santorini games.

        :return: TournamentResult, result of tournament
        """
        # Run round robin game
        for i, player in enumerate(self.__players):
            self.__match_against_rest(player, self.__players[i + 1:])

        # Reformat all meet ups
        meet_ups = list(map(lambda x: [x.winner.get_id(), x.loser.get_id()], self.__meet_ups))
        
        return [self.__misbehaved_players, meet_ups]

    
    def __handle_misbehaving_player(self, player):
        """
        Add the player to the misbehaved players list,
        and change all past meet-ups involving the player to be counted as win for the opponent.

        If the player lost in a past meet up, nothing is changed in the meetup. 

        If a player breaks after winning past games due to its opponents' breakage, 
        the game is eliminated from the tournament evaluation.
        
        :param player: Player, the player that misbehaved
        """
        self.__misbehaved_players.append(player.get_id())
        new_meet_ups = []

        for meet_up in self.__meet_ups:
            winner = meet_up.winner
            loser = meet_up.loser
            condition = meet_up.condition

            # Leave out if both winner and loser are broken
            if winner.get_id() == player.get_id() and condition is not GameOverCondition.FairGame:
                continue

            # Switch winner and loser if winner is broken player
            if winner.get_id() == player.get_id() and condition is GameOverCondition.FairGame:
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
            if player_id in players_set or any(c.isupper() for c in player_id):
                new_id = self.__get_unique_id(players_set)
                player.set_id(new_id)
                player_id = new_id
            players_set.add(player_id)

        
    def __get_unique_id(self, ids):
        """
        Get a new id unique from those in the given set.

        :param ids: {}, set of existing ids
        """
        new_id = names.get_first_name().lower()
        while new_id in ids:
            new_id = names.get_first_name().lower()
        return new_id


    def __match_against_rest(self, player, opponents):
        """
        Match given player to the given opponents, updating the meet ups.

        :param player: Player, player 
        :param opponents: [Player, ...], opponents of player 
        """
        for opponent in opponents:

            if player.get_id() in self.__misbehaved_players:
                break

            if opponent.get_id() in self.__misbehaved_players:
                continue
            
            referee = Referee(player, opponent, time_limit=5, observers=self.__observers)
            self.__notify_of_opponents(player, opponent)
            series_result = referee.run_games(3)

            # Penalize loser if game ended unfairly
            if series_result.condition is not GameOverCondition.FairGame:
                self.__handle_misbehaving_player(series_result.loser.player)

            self.__meet_ups.append(series_result)
                
    
    def __notify_of_opponents(self, player_one, player_two):
        """
        Notify the given matched up players of each other's ids.

        :param player_one: Player, player one
        :param player_two: Player, player two
        """
        player_one.notify_of_opponent(player_two.get_id())
        player_two.notify_of_opponent(player_one.get_id())


