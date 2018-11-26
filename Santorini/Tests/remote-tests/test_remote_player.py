import pytest

from Remote.remote_player import RemotePlayer

class MockConnection:
    def __init__(self):
        self.message = ""
        self.count = 0
        self.commands = [
            '[0, 0]',
            '["one", "EAST", "NORTH", "WEST", "SOUTH"]',
            'invalid JSON'            
            ]

    def change_count(self, new_count):
        self.count = new_count

    def sendall(self, message):
        self.message = message.decode()

    def recv(self, buffer_size):
        command = self.commands[self.count]
        self.count += 1
        return command.encode()


@pytest.fixture
def player_id():
    return "player"

@pytest.fixture
def connection():
    conn = MockConnection()
    yield conn
    conn.change_count(0)

@pytest.fixture
def remote_player(player_id, connection):
    return RemotePlayer(player_id, connection)



class TestGetId:
    def test_get_correct_id(self, player_id, remote_player):
        assert remote_player.get_id() == player_id


class TestSetId:
    def test_changes_new_id(self, remote_player):
        new_id = "new"
        remote_player.set_id(new_id)
        assert remote_player.get_id() == new_id

    def test_sends_new_id_to_connection(self, connection, remote_player):
        new_id = "new"
        remote_player.set_id(new_id)
        assert connection.message == f'["playing as", "{new_id}"]'


class TestGetPlacement:
    def test_return_correct_place_spec(self, player_id, remote_player, board, rule_checker):
        wid = "one"
        spec = remote_player.get_placement(board, wid, rule_checker)
        assert spec['type'] == 'place'
        assert spec['wid'] == wid
        assert spec['xy'] == [0, 0]

    def test_raise_exception_with_wrong_response(self, remote_player, board, rule_checker, connection):
        connection.change_count(2)
        with pytest.raises(Exception) as e:
            remote_player.get_placement(board, "one", rule_checker)


class TestGetMove:
    def test_return_correct_move_spec(self, player_id, connection, remote_player, board, rule_checker):
        connection.change_count(1)
        board.place_worker(player_id, "one", 0, 0)
        spec = remote_player.get_move(board, rule_checker)
        assert spec['type'] == 'move'
        assert spec['xy1'] == [0, 0]
        assert spec['xy2'] == [1, -1]
    
    def test_raise_exception_with_wrong_response(self, player_id, connection, remote_player, board, rule_checker):
        connection.change_count(2)
        board.place_worker(player_id, "one", 0, 0)
        with pytest.raises(Exception) as e:
            remote_player.get_move(board, rule_checker)


class TestGetBuild:
    def test_return_correct_build_spec(self, player_id, connection, remote_player, board, rule_checker):
        connection.change_count(1)
        board.place_worker(player_id, "one", 0, 0)
        spec = remote_player.get_move(board, rule_checker)
        spec = remote_player.get_build(board, "one", rule_checker)
        assert spec['type'] == 'build'
        assert spec['xy1'] == [1, -1]
        assert spec['xy2'] == [0, 0]
    
    def test_raise_exception_with_wrong_response(self, player_id, connection, remote_player, board, rule_checker):
        connection.change_count(2)
        board.place_worker(player_id, "one", 0, 0)
        with pytest.raises(Exception) as e:
            remote_player.get_build(board, "one", rule_checker)
