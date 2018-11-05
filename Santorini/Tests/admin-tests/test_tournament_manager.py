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


@pytest.fixture
def random_player_one():
    return RandomPlayer("random_one")

@pytest.fixture
def infinite_player_one():
    return InfiniteLoopPlayer("infinite_one")

@pytest.fixture
def misbehaving_player_one():
    return MisbehavingPlayer("misbehaving_one")




