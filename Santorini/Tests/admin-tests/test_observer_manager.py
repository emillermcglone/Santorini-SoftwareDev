import pytest
import io

from Admin.observer_manager import ObserverManager
from Admin.board import GameBoard
from Admin.game_over import GameOverCondition
from Observer.xobserver import XObserver
from Lib.util import xboard, make_build, make_move, make_place, make_action


@pytest.fixture
def output():
    return io.StringIO()

@pytest.fixture
def observer(output):
    return XObserver(output)

@pytest.fixture
def manager(observer):
    return ObserverManager([observer])


""" Test init """
def test_has_observers(manager, observer):
    assert len(manager.observers) is 1
    assert manager.observers[0] is observer


""" Test add_observer """
def test_add_one_observer(manager, observer):
    assert len(manager.observers) is 1
    manager.add_observer(observer)
    assert len(manager.observers) is 2


""" Test update state """
def test_update_state_with_empty_board(manager, board, output):
    assert output.getvalue() is ""
    manager.update_state(board)
    assert output.getvalue() == xboard(board)

def test_update_state_with_occupied_board(manager, board, output):
    assert output.getvalue() is ""
    board.place_worker("pid", "wid", 0, 0)
    manager.update_state(board)
    assert output.getvalue() == xboard(board)

def test_empty_if_update_state_crashes(manager, board, output):
    assert output.getvalue() is ""
    manager.update_state(None)
    assert output.getvalue() is ""

def test_broken_observer_is_removed_after_update_state(manager, board, output):
    assert len(manager.observers) is 1
    assert output.getvalue() is ""
    manager.update_state(None)
    assert output.getvalue() is ""
    assert manager.observers == []


""" Test update_action """
def test_update_action_with_move_and_build(guarded_player, random_player_one, rule_checker, manager, board, output):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)
    move = guarded_player.get_move(board, rule_checker)
    board.move_worker(*move['xy1'], *move['xy2'])
    build = guarded_player.get_build(board, "wid", rule_checker)
    board.build_floor(*build['xy2'])

    manager.update_action(guarded_player, board)
    assert output.getvalue() == make_action("wid", move, build) + "\n" + xboard(board)


def test_empty_if_update_action_crashes(guarded_player, random_player_one, rule_checker, manager, board, output):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)
    move = guarded_player.get_move(board, rule_checker)
    board.move_worker(*move['xy1'], *move['xy2'])
    build = guarded_player.get_build(board, "wid", rule_checker)
    board.build_floor(*build['xy2'])

    manager.update_action(guarded_player, None)
    assert output.getvalue() == make_action("wid", move, build) + "\n"

def test_broken_observer_is_removed_after_update_action(guarded_player, random_player_one, rule_checker, manager, board, output):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)
    move = guarded_player.get_move(board, rule_checker)
    board.move_worker(*move['xy1'], *move['xy2'])
    build = guarded_player.get_build(board, "wid", rule_checker)
    board.build_floor(*build['xy2'])

    manager.update_action(guarded_player, None)
    assert manager.observers == []


""" Test give_up """
def test_player_give_up(manager, output):
    assert output.getvalue() is ""
    manager.give_up("player")
    assert output.getvalue() == f"Player gave up: player\n"

def test_empty_if_give_up_crashes(manager, output):
    assert output.getvalue() is ""
    manager.give_up(None)
    assert output.getvalue() is ""

def test_broken_observer_is_removed_after_give_up_crashes(manager, output):
    assert output.getvalue() is ""
    manager.give_up(None)
    assert output.getvalue() is ""
    assert manager.observers == []


""" Test error """
def test_player_error(manager, output):
    assert output.getvalue() is ""
    manager.error("pid", GameOverCondition.Crash)
    assert output.getvalue() == "Player error by: " + "pid. " + GameOverCondition.Crash.value + "\n"

def test_empty_if_error_crashes(manager, output):
    assert output.getvalue() is ""
    manager.error("pid", None)
    assert output.getvalue() is ""

def test_broken_observer_is_removed_after_error_crashes(manager, output):
    assert output.getvalue() is ""
    manager.error("pid", None)
    assert output.getvalue() is ""
    assert manager.observers == []


""" Test game_over """
def test_player_game_over(guarded_player, board, rule_checker, manager, output):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)
    guarded_player.get_move(board, rule_checker)

    assert output.getvalue() is ""
    manager.game_over(guarded_player)
    assert output.getvalue() is not ""