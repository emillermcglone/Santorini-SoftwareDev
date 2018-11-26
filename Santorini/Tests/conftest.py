import pytest
import sys, os, io

dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dir_path + '/../')

from Admin.referee import Referee
from Admin.game_over import GameOverCondition
from Admin.rule_checker import RuleChecker
from Admin.guarded_player import GuardedPlayer
from Admin.board import GameBoard
from Player.players.random_player import Player as RandomPlayer
from Player.players.infinite_loop_player import InfiniteLoopPlayer
from Player.players.misbehaving_player import MisbehavingPlayer
from Player.players.crashing_player import CrashingPlayer

from Observer.observer import Observer
from Observer.xobserver import XObserver

from Remote.proxy import ClientProxy

from Tests.echo_server import EchoServer
from Tests.subscriber import Subscriber


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
def crashing_player_one():
    return CrashingPlayer("crashing_player_one")

@pytest.fixture
def random_random_referee(random_player_one, random_player_two):
    return Referee(random_player_one, random_player_two, time_limit=1, observers=[])

@pytest.fixture
def random_infinite_referee(random_player_one, infinite_player_one):
    return Referee(random_player_one, infinite_player_one, time_limit=1, observers=[])

@pytest.fixture
def infinite_random_referee(random_player_one, infinite_player_one):
    return Referee(infinite_player_one, random_player_one, time_limit=1, observers=[])

@pytest.fixture
def random_misbehaving_referee(random_player_one, misbehaving_player_one):
    return Referee(random_player_one, misbehaving_player_one, time_limit=1, observers=[])

@pytest.fixture
def misbehaving_random_referee(random_player_one, misbehaving_player_one):
    return Referee(misbehaving_player_one, random_player_one, observers=[])

@pytest.fixture
def random_crashing_referee(random_player_one, crashing_player_one):
    return Referee(random_player_one, crashing_player_one, observers=[])

@pytest.fixture
def even_numbers():
    return [2, 4, 6, 8, 10]


@pytest.fixture
def guarded_player(random_player_one):
    return GuardedPlayer(random_player_one)

@pytest.fixture
def board():
    return GameBoard()

@pytest.fixture
def rule_checker(board):
    return RuleChecker(board)


@pytest.fixture
def ip():
    return '127.0.0.1'


@pytest.fixture
def port():
    return 5005


@pytest.fixture
def buffer_size():
    return 1024

@pytest.fixture
def echo_server(ip, port, buffer_size):
    server = EchoServer(ip, port, buffer_size)
    server.start()
    return server

@pytest.fixture
def client_proxy(ip, port, buffer_size):
    proxy = ClientProxy(ip, port, buffer_size)
    yield proxy
    proxy.close()

@pytest.fixture
def subscriber():
    return Subscriber()