import pytest
import copy
import json

from Admin.server_configurations.stdin_server_configuration import ServerConfiguration

@pytest.fixture
def valid_conf():
    return '{ "min players" : 3, "port": 56789, "waiting for": 10, "repeat": 1 }'

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
    return ServerConfiguration(readable)


class TestMinPlayers:
    def test_correct_min_players(self, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert conf.min_players() == valid_conf_json["min players"]

    def test_continue_with_zero(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'min players', 0)
        conf = make_conf(new_conf)
        assert conf.min_players() == 0

    def test_exit_with_float(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "min players", 2.1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.min_players()

    def test_exit_with_negative_number(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'min players', -1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.min_players()

    def test_exit_with_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'min players', "invalid")
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.min_players()

    def test_exit_with_bool(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'min players', True)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.min_players()

    def test_exit_with_none(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, 'min players', None)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.min_players()


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


class TestWaitingFor:
    def test_correct_waiting_for(self, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert conf.waiting_for() == valid_conf_json["waiting for"]

    def test_exit_with_zero(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "waiting for", 0)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.waiting_for()

    def test_exit_with_float(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "waiting for", 2.1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.waiting_for()

    def test_exit_with_negative_number(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "waiting for", -1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.waiting_for()

    def test_exit_with_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "waiting for", "invalid")
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.waiting_for()

    def test_exit_with_bool(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "waiting for", True)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.waiting_for()

    def test_exit_with_none(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "waiting for", None)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.waiting_for()


class TestRepeat:
    def test_correct_repeat(self, valid_conf_readable, valid_conf_json):
        conf = make_conf(valid_conf_readable)
        assert conf.repeat() == valid_conf_json["repeat"]

    def test_false_with_zero(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", 0)
        conf = make_conf(new_conf)
        assert not conf.repeat() 

    def test_true_with_one(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", 1)
        conf = make_conf(new_conf)
        assert conf.repeat()

    def test_exit_with_above_1(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", 2)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.repeat()

    def test_exit_with_float(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", 0.2)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.repeat()

    def test_exit_with_negative_number(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", -1)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.repeat()

    def test_exit_with_string(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", "invalid")
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.repeat()

    def test_exit_with_bool(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", True)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.repeat()

    def test_exit_with_none(self, valid_conf):
        new_conf = modify_conf_readable(valid_conf, "repeat", None)
        conf = make_conf(new_conf)
        with pytest.raises(SystemExit) as e:
            conf.repeat()