import pytest

from Admin.game_over import GameOverCondition
from Observer.xobserver import XObserver

""" Test __init__ """
def test_players(random_player_one, random_player_two, random_random_referee):
    assert random_random_referee.players == [
        random_player_one, random_player_two]

def test_only_two_players(random_random_referee):
    assert len(random_random_referee.players) is 2

def test_empty_observers(random_random_referee):
    assert len(random_random_referee.observers) is 0


""" Test add_observer """
def test_empty_observers(random_random_referee):
    assert len(random_random_referee.observers) is 0

def test_add_one_observer(random_random_referee):
    random_random_referee.add_observer(XObserver())
    assert len(random_random_referee.observers) is 1

def test_add_two_observers(random_random_referee):
    random_random_referee.add_observer(XObserver())
    random_random_referee.add_observer(XObserver())
    assert len(random_random_referee.observers) is 2


""" Test run_games """
def test_run_single(random_random_referee):
    game_over = random_random_referee.run_games()
    assert game_over.condition is GameOverCondition.FairGame
    assert game_over.winner.get_id() is "random_two"

def test_run_zero_yields_winner(random_random_referee):
    game_over = random_random_referee.run_games(0)
    assert game_over.condition is GameOverCondition.FairGame
    assert game_over.winner.get_id() is "random_two"

def test_run_even_yields_winner(random_random_referee, even_numbers):
    for num in even_numbers:
        game_over = random_random_referee.run_games(num)
        assert game_over.condition is GameOverCondition.FairGame
        assert game_over.winner.get_id() is "random_two"

def test_run_single_random_and_infinite(random_infinite_referee):
    game_over = random_infinite_referee.run_games()
    assert game_over.condition is GameOverCondition.Timeout
    assert game_over.winner.get_id() is "random_one"

def test_run_single_infinite_and_random(infinite_random_referee):
    game_over = infinite_random_referee.run_games()
    assert game_over.condition is GameOverCondition.Timeout
    assert game_over.winner.get_id() is "random_one"

def test_run_single_random_and_misbehaving(random_misbehaving_referee):
    game_over = random_misbehaving_referee.run_games()
    assert game_over.condition is GameOverCondition.InvalidAction
    assert game_over.winner.get_id() is "random_one"

def test_run_single_misbehaving_and_random(misbehaving_random_referee):
    game_over = misbehaving_random_referee.run_games()
    assert game_over.condition is GameOverCondition.InvalidAction
    assert game_over.winner.get_id() is "random_one"

def test_run_single_random_crashing(random_crashing_referee):
    game_over = random_crashing_referee.run_games()
    assert game_over.condition is GameOverCondition.Crash
    assert game_over.winner.get_id() is "random_one"


