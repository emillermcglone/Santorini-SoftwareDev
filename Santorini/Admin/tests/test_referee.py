import pytest

from Santorini.Admin.referee import SantoriniReferee
from Santorini.Player.player import Player
from Santorini.Common.rule_checker import RuleChecker

@pytest.fixture
def player_one():
    return Player(1)

@pytest.fixture
def player_two():
    return Player(2)

@pytest.fixture
def referee(player_one, player_two):
    return SantoriniReferee(player_one, player_two, RuleChecker)


class TestInit:
    def test_players(self, player_one, player_two, referee):
        assert referee.players == [player_one, player_two]

    def test_only_two_players(self, referee):
        assert len(referee.players) is 2


class TestRunGames:
    def test_run_single(self, referee):
        winner = referee.run_games()
        assert winner is 1





