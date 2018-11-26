import pytest
import time

from timeout_decorator import timeout, TimeoutError
from Remote.proxy import ClientProxy

from Tests.echo_server import EchoServer

class Holder:
    def __init__(self):
        self.value = ""

    def update(self, new_value):
        self.value = new_value


@pytest.fixture
def holder():
    return Holder()


@pytest.fixture
def echo_server(ip, port, holder, buffer_size):
    server = EchoServer(ip, port, holder, buffer_size)
    server.start()
    yield server
    server.close()


class TestInit:
    def test_has_ip(self, ip, client_proxy):
        assert ip is client_proxy.ip

    def test_has_port(self, port, client_proxy):
        assert port is client_proxy.port

    def test_has_buffer_size(self, buffer_size, client_proxy):
        assert buffer_size is client_proxy.buffer_size

    def test_is_not_live(self, client_proxy):
        assert not client_proxy.live


class TestConnect:
    def test_is_live_after_connect(self, echo_server, client_proxy):
        assert not client_proxy.live
        client_proxy.connect()
        assert client_proxy.live

    def test_is_live_after_multiple_connects(self, echo_server, client_proxy):
        assert not client_proxy.live

        client_proxy.connect()
        assert client_proxy.live

        client_proxy.connect()
        assert client_proxy.live


class TestSend:
    def test_message_is_sent(self, holder, echo_server, client_proxy):
        client_proxy.send("Message")
        time.sleep(1)
        assert holder.value == "Message"

        client_proxy.send("Second Message")
        time.sleep(2)
        assert holder.value == "Second Message"


class TestReceive:
    def test_receive_message(self, holder, echo_server, client_proxy):
        client_proxy.send("Message")
        time.sleep(1)
        assert client_proxy.receive() == "Message"

    def test_wait_for_next_message(self, holder, echo_server, client_proxy):
        timeout_receive = timeout(2)(client_proxy.receive)
        with pytest.raises(TimeoutError) as e:
            timeout_receive()
