import pytest
import sys, os
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dir_path + '/../../')

from Admin.referee import Referee
from Admin.game_over import GameOverCondition
from Admin.rule_checker import RuleChecker
from Player.random_player import Player


@pytest.fixture
def player_one():
    return Player(1)

@pytest.fixture
def player_two():
    return Player(2)

@pytest.fixture
def referee(player_one, player_two):
    return Referee(player_one, player_two, RuleChecker)


class TestInit:
    def test_players(self, player_one, player_two, referee):
        assert referee.players == [player_one, player_two]

    def test_only_two_players(self, referee):
        assert len(referee.players) is 2


class TestRunGames:
    def test_run_single(self, referee):
        game_over = referee.run_games()
        assert game_over.winner.get_id() is 1





