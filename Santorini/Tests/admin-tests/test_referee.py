import pytest
import sys, os
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dir_path + '/../../')

from Admin.referee import Referee
from Admin.game_over import GameOverCondition
from Admin.rule_checker import RuleChecker
from Player.mock_players.random_player import Player as RandomPlayer
from Player.mock_players.infinite_loop_player import InfiniteLoopPlayer
from Player.mock_players.misbehaving_player import MisbehavingPlayer

from Observer.xobserver import XObserver


@pytest.fixture
def random_player_one():
    return RandomPlayer("random_one")

@pytest.fixture
def random_player_two():
    return RandomPlayer("random_two")

@pytest.fixture
def infinite_player_one():
    return InfiniteLoopPlayer("infinite_one")

@pytest.fixture
def misbehaving_player_one():
    return MisbehavingPlayer("misbehaving_one")

@pytest.fixture
def random_random_referee(random_player_one, random_player_two):
    return Referee(random_player_one, random_player_two, time_limit=1)

@pytest.fixture
def random_infinite_referee(random_player_one, infinite_player_one):
    return Referee(random_player_one, infinite_player_one, time_limit=1)

@pytest.fixture
def infinite_random_referee(random_player_one, infinite_player_one):
    return Referee(infinite_player_one, random_player_one, time_limit=1)

@pytest.fixture
def random_misbehaving_referee(random_player_one, misbehaving_player_one):
    return Referee(random_player_one, misbehaving_player_one, time_limit=1)

@pytest.fixture
def misbehaving_random_referee(random_player_one, misbehaving_player_one):
    return Referee(misbehaving_player_one, random_player_one)


class TestInit:
    def test_players(self, random_player_one, random_player_two, random_random_referee):
        assert random_random_referee.players == [random_player_one, random_player_two]

    def test_only_two_players(self, random_random_referee):
        assert len(random_random_referee.players) is 2

    def test_empty_observers(self, random_random_referee):
        assert len(random_random_referee.observers) is 0


class TestAddObserver:
    def test_empty_observers(self, random_random_referee):
        assert len(random_random_referee.observers) is 0

    def test_add_one_observer(self, random_random_referee):
        random_random_referee.add_observer(XObserver())
        assert len(random_random_referee.observers) is 1

    def test_add_two_observers(self, random_random_referee):
        random_random_referee.add_observer(XObserver())
        assert len(random_random_referee.observers) is 2


class TestRunGames:
    def test_run_single(self, random_random_referee):
        game_over = random_random_referee.run_games(5)
        assert game_over.condition is GameOverCondition.FairGame
        assert game_over.winner.get_id() is "random_one"


    def test_run_random_and_infinite(self, random_infinite_referee):
        game_over = random_infinite_referee.run_games()
        assert game_over.condition is GameOverCondition.Timeout
        assert game_over.winner.get_id() is "random_one"


    def test_run_infinite_and_random(self, infinite_random_referee):
        game_over = infinite_random_referee.run_games()
        assert game_over.condition is GameOverCondition.Timeout
        assert game_over.winner.get_id() is "random_one"


    def test_run_random_and_misbehaving(self, random_misbehaving_referee):
        game_over = random_misbehaving_referee.run_games()
        assert game_over.condition is GameOverCondition.InvalidAction
        assert game_over.winner.get_id() is "random_one"


    def test_run_misbehaving_and_random(self, misbehaving_random_referee):
        game_over = misbehaving_random_referee.run_games()
        assert game_over.condition is GameOverCondition.InvalidAction
        assert game_over.winner.get_id() is "random_one"
