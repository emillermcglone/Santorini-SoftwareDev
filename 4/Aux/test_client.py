import unittest
import socket
import socketserver
from client import *
from server import MyTCPHandler

HOST, PORT = "localhost", 8000

""" Run 'python3 server.py' before running this program """
class TestConnect(unittest.TestCase): 
    def setUp(self):
        self.sock = connect(HOST, PORT)

    def tearDown(self):
        self.sock.close()

    def test_returns_valid_socket(self):
        self.assertEqual(self.sock.type, socket.SOCK_STREAM)
        self.assertEqual(self.sock.family, socket.AF_INET)

    def test_returned_socket_has_connected(self):
        with self.assertRaises(OSError):
            self.sock.connect((HOST, PORT))

class TestSend(unittest.TestCase):
    def test_server_mirrors_data(self):
        self.assertEqual(send(HOST, PORT, "cs4500"), "cs4500")

    def test_empty_string_if_given_empty_string(self):
        self.assertEqual(send(HOST, PORT, ""), "")

class TestGetJsonInputs(unittest.TestCase):
    def setUp(self):
        self.expected_output = [[1, 2], [3,4,5], {"a": 1}]
        self.expected_output_edge_cases = [[1, 2]]

    def test_empty_list_from_empty_source(self):
        self.assertEqual([], get_json_inputs(open('sample-input-empty', 'r+')))

    def test_expected_output_from_sample_input(self):
        self.assertEqual(self.expected_output, 
            get_json_inputs(open('sample-input', 'r+')))

    def test_filter_out_non_json(self):
        self.assertEqual(self.expected_output_edge_cases, 
            get_json_inputs(open('sample-input-non-json', 'r+')))

    def test_end_at_control_d(self):
        self.assertEqual(self.expected_output_edge_cases,
            get_json_inputs(open('sample-input-control-d', 'r+')))

    def test_end_at_control_c(self):
        self.assertEqual(self.expected_output_edge_cases,
            get_json_inputs(open('sample-input-control-c', 'r+')))

    def test_end_at_end_of_file(self):
        self.assertEqual(self.expected_output_edge_cases,
            get_json_inputs(open('sample-input-end-of-line', 'r+')))

    def test_expected_output_from_multiline_json(self):
        self.assertEqual(self.expected_output_edge_cases,
            get_json_inputs(open('sample-input-multiline', 'r+')))

    def test_parses_multi_json_in_one_line(self):
        self.assertEquals([[1, 2], [3, 4], [5, 6]],
            get_json_inputs(open('sample-input-multi-json', 'r+')))

class TestIsIPAddress(unittest.TestCase):
    def test_true_if_valid_ip(self):
        self.assertTrue(is_ip_address("127.0.0.1"))
        self.assertTrue(is_ip_address("192.0.0.1"))
    
    def test_false_if_invalid_ip(self):
        self.assertFalse(is_ip_address("1234.0.0.2"))
        self.assertFalse(is_ip_address("192.121231.1.2"))
        self.assertFalse(is_ip_address("192.0.2321321321.1"))
        self.assertFalse(is_ip_address("192.0.0.32132133"))

    def test_false_if_localhost(self):
        self.assertFalse(is_ip_address("localhost"))

class TestIsFileFound(unittest.TestCase):
    def test_true_if_file_exists(self):
        self.assertTrue(is_file_found('sample-input.txt'))

    def test_false_if_file_does_not_exist(self):
        self.assertFalse(is_file_found('file.txt'))

if __name__ == "__main__":
    test_cases = [TestConnect, TestSend, TestIsIPAddress, TestIsFileFound, TestGetJsonInputs]
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)