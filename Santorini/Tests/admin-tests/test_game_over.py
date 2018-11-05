import pytest
import sys, os
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dir_path + '/../../')

from Player.mock_players.random_player import Player
from Admin.game_over import GameOver, GameOverCondition

@pytest.fixture
def john_doe():
    return Player("John Doe")

@pytest.fixture
def winner():
    return Player(1)

@pytest.fixture
def loser():
    return Player(2)

@pytest.fixture
def condition():
    return GameOverCondition.FairGame

@pytest.fixture
def game_over(winner, loser, condition):
    return GameOver(winner, loser, condition)


def test_value_error_with_same_players(john_doe, condition):
    with pytest.raises(ValueError):
        GameOver(john_doe, john_doe, condition)

def test_game_over_has_winner(game_over, winner):
    assert game_over.winner is winner

def test_game_over_has_loser(game_over, loser):
    assert game_over.loser is loser

def test_game_over_has_condition(game_over, condition):
    assert game_over.condition is condition
