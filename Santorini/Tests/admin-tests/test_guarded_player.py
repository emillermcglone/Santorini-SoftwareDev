import pytest

from Admin.board import GameBoard
from Admin.rule_checker import RuleChecker
from Admin.guarded_player import GuardedPlayer
from Lib.util import make_place, make_move, make_build


""" Test init """
def test_has_external_player(guarded_player, random_player_one):
    assert guarded_player.player == random_player_one

def test_has_external_player_id(guarded_player, random_player_one):
    assert guarded_player.id == random_player_one.get_id()


""" Test get_id """
def test_has_guarded_id(guarded_player, random_player_one):
    original_id = random_player_one.get_id()
    assert guarded_player.get_id() is original_id

def test_has_same_guarded_id_after_change(guarded_player, random_player_one):
    original_id = random_player_one.get_id()
    random_player_one.set_id("not the same")
    assert random_player_one.get_id() is "not the same"
    assert guarded_player.get_id() is not "not the same"
    assert guarded_player.get_id() is original_id


""" Test set_id """
def test_set_guarded_id(guarded_player, random_player_one):
    assert guarded_player.get_id() is random_player_one.get_id()
    guarded_player.set_id("new id")
    assert guarded_player.get_id() is "new id"

def test_set_external_player_id(guarded_player, random_player_one):
    assert guarded_player.get_id() is random_player_one.get_id()
    guarded_player.set_id("new id")
    assert guarded_player.get_id() is "new id"
    assert random_player_one.get_id() is "new id"


""" test get_placement and last_place """
def test_none_after_init_for_last_place(guarded_player):
    assert guarded_player.last_place() is None

def test_place_action_after_get_place(guarded_player, board, rule_checker):
    guarded_player.get_placement(board, "wid", rule_checker)
    assert guarded_player.last_place()['type'] is "place"
    

""" test get_move and last_move """
def test_none_after_init_for_last_move(guarded_player):
    assert guarded_player.last_move() is None

def test_move_action_after_get_move(guarded_player, board, rule_checker):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)

    guarded_player.get_move(board, rule_checker)
    assert guarded_player.last_move()[0] is "wid"
    assert guarded_player.last_move()[1]['type'] is "move"


""" test get_build and last_build """
def test_none_after_init_for_last_build(guarded_player):
    assert guarded_player.last_build() is None

def test_build_action_after_get_build(guarded_player, board, rule_checker):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)

    guarded_player.get_build(board, "wid", rule_checker)
    assert guarded_player.last_build()[0] is "wid"
    assert guarded_player.last_build()[1]['type'] is "build"


""" test reset """
def test_last_place_return_none_after_reset(guarded_player, board, rule_checker):
    guarded_player.get_placement(board, "wid", rule_checker)
    assert guarded_player.last_place()['type'] is "place"

    guarded_player.reset()
    assert guarded_player.last_place() is None


def test_last_move_return_none_after_reset(guarded_player, board, rule_checker):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)

    guarded_player.get_move(board, rule_checker)
    assert guarded_player.last_move()[0] is "wid"
    assert guarded_player.last_move()[1]['type'] is "move"

    guarded_player.reset()
    assert guarded_player.last_move() is None


def test_last_build_return_none_after_reset(guarded_player, board, rule_checker):
    board.place_worker(guarded_player.get_id(), "wid", 0, 0)

    guarded_player.get_build(board, "wid", rule_checker)
    assert guarded_player.last_build()[0] is "wid"
    assert guarded_player.last_build()[1]['type'] is "build"

    guarded_player.reset()
    assert guarded_player.last_build() is None







