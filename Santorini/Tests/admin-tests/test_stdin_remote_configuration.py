import pytest
import copy
import json

from Admin.configurations.stdin_remote_configuration import STDINRemoteConfiguration
from Player.players.infinite_loop_player import InfiniteLoopPlayer
from Player.players.place_infinite_loop_player import PlaceInfiniteLoopPlayer
from Player.players.random_player import Player

@pytest.fixture
def valid_conf():
    return '{ "players": [["infinite", "infinite_move", "Player.players.infinite_loop_player.InfiniteLoopPlayer"], ["good", "random_one", "Player.players.random_player.Player"], ["infinite", "infinite_place", "Player.players.place_infinite_loop_player.PlaceInfiniteLoopPlayer"]], "observers": [], "ip": "localhost", "port": 55556 }'

@pytest.fixture
def players():
    return [InfiniteLoopPlayer("infinite_move"), Player("random_one"), PlaceInfiniteLoopPlayer("infinite_place")]

@pytest.fixture
def observers():
    return []


@pytest.fixture
def valid_conf_json(valid_conf):
    return json.loads(valid_conf)

@pytest.fixture
def valid_conf_readable(valid_conf):
    return lambda: valid_conf

def modify_conf_readable(conf, key, value):
    conf_json = json.loads(conf)
    conf_json[key] = value
    return lambda: json.dumps(conf_json)

def make_conf(readable):
    return STDINRemoteConfiguration(readable)

def same_ids(players_one, players_two):
    for one, two in zip(players_one, players_two):
        if not one.get_id() == two.get_id():
            return False
    return True


class TestPlayers:
    def test_correct_players(self, players, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert same_ids(conf.players(), players)

    def test_empty_list_with_empty(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [])
        conf = make_conf(new_conf)
        assert conf.players() == []

    def test_exit_with_number_as_kind(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [[1, "foo", "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_true_as_kind(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [[True, "foo", "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_false_as_kind(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [[False, "foo", "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_none_as_kind(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [[None, "foo", "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_list_as_kind(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [[[], "foo", "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()


    def test_exit_with_number_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", 1, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_true_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", True, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_false_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", False, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_none_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", None, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_list_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", [], "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_number_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", "foo", 1]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_true_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", "foo", True]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_false_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", "foo", False]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_none_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", "foo", None]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()

    def test_exit_with_list_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "players", [["good", "foo", []]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.players()


class TestObservers:
    def test_correct_observers(self, observers, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert same_ids(conf.observers(), observers)

    def test_exit_with_number_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [])
        conf = make_conf(new_conf)
        assert conf.observers() == []

    def test_exit_with_number_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [[1, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_true_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [[True, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_false_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [[False, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_none_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [[None, "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_list_as_name(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [[[], "bar"]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_number_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [["foo", 1]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_true_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [["foo", True]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_false_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [["foo", False]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_none_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [["foo", None]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()

    def test_exit_with_list_as_path_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "observers", [["foo", []]])
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.observers()






class TestPort:
    def test_correct_port(self, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert conf.port() == valid_conf_json["port"]
    
    def test_exit_with_float(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "port", 50500.1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()

    def test_exit_with_negative_number(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'port', -1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()

    def test_exit_below_50000(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'port', 49999)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()

    def test_exit_above_60000(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'port', 60001)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()

    def test_exit_with_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'port', "invalid")
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()

    def test_exit_with_bool(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'port', True)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()

    def test_exit_with_none(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'port', None)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.port()


class TestIP:
    def test_correct_ip(self, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert conf.ip() == valid_conf_json["ip"]
    
    def test_exit_with_float(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "ip", 50500.1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.ip()

    def test_exit_with_number(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "ip", 2)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.ip()

    def test_does_not_exit_with_invalid_ip(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "ip", "invalid")
        conf = make_conf(new_conf)
        assert conf.ip() == "invalid"

    def test_exit_with_bool(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "ip", True)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.ip()

    def test_exit_with_none(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "ip", None)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.ip()
