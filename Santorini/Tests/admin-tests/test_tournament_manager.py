import pytest
import sys, os
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dir_path + '/../../')

from Admin.tournament_manager import TournamentManager
from Admin.referee import Referee
from Admin.game_over import GameOverCondition
from Admin.rule_checker import RuleChecker
from Player.players.random_player import Player as RandomPlayer
from Player.players.infinite_loop_player import InfiniteLoopPlayer
from Player.players.misbehaving_player import MisbehavingPlayer

from Observer.xobserver import XObserver

from Tests.configuration import Configuration

@pytest.fixture
def duplicate_players_conf(random_player_one, infinite_player_one, misbehaving_player_one):
    return Configuration([random_player_one, infinite_player_one, RandomPlayer("random_one"), misbehaving_player_one], [])

@pytest.fixture
def manager_with_duplicate_players(duplicate_players_conf):
    return TournamentManager(duplicate_players_conf)


class TestInit:
    def no_duplicates(self, players):
        for i in range(len(players)):
            player_id = players[i].get_id()
            for player in players[i + 1:]:
                if player.get_id() is player_id:
                    return False

        return True

    def test_length_of_players_is_same(self, manager_with_duplicate_players):
        assert len(manager_with_duplicate_players.players()) is 4

    def test_changed_player_duplicates(self, duplicate_players_conf, manager_with_duplicate_players):
        assert self.no_duplicates(manager_with_duplicate_players.players())

    




