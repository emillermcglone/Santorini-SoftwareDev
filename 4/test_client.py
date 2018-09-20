import unittest
import socket
from client import *

class TestConnect(unittest.TestCase): 
    def setUp(self):
        self.sock = connect()

    def test_returns_valid_socket(self):
        self.assertEqual(self.sock.type, socket.SOCK_STREAM)
        self.assertEqual(self.sock.family, socket.AF_INET)

    def test_returned_socket_has_connected(self):
        with self.assertRaises(OSError):
            self.sock.connect((HOST, PORT))


class TestSend(unittest.TestCase):
    pass

class TestGetJsonInputs(unittest.TestCase):
    pass


if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestConnect)
    alltests = unittest.TestSuite([suite1])
    unittest.TextTestRunner(verbosity=2).run(alltests)