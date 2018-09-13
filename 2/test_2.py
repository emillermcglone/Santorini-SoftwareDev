import unittest
import time
import sys
from mock_output import MockOutput

two = __import__('2')

class TestIsJson(unittest.TestCase):
    def test_true_given_array_json_string(self):
        self.assertTrue(two.is_json("[1, 2]"))

    def test_true_given_dict_json_string(self):
        self.assertTrue(two.is_json('{"a": 1}'))

    def test_false_given_number(self):
        self.assertFalse(two.is_json(2))

    def test_false_given_non_json_string(self):
        self.assertFalse(two.is_json("CS4500"))

    def test_false_given_dict(self):
        self.assertFalse(two.is_json({}))

    def test_false_given_list(self):
        self.assertFalse(two.is_json([1, 2]))

    def test_false_given_none(self):
        self.assertFalse(two.is_json(None))

class TestConcatenateJsonInputs(unittest.TestCase):
    def setUp(self):
        self.input_list = ["Welcome", "to", "hell"]
        self.result_list = two.concatenate_json_inputs(self.input_list)

    def test_empty_list_given_empty_inputs(self):
        self.assertEqual(two.concatenate_json_inputs([]), [])

    def test_empty_list_given_none(self):
        self.assertEqual(two.concatenate_json_inputs(None), [])

    def test_concatenate_non_empty_list_with_positions(self):
        length_from_zero = len(self.result_list) - 1
        for index, (position, item) in enumerate(self.result_list):
            self.assertTrue(position == length_from_zero - index)

    def test_every_input_has_position(self):
        for index, element in enumerate(self.result_list):
            self.assertEqual(len(element), 2)
            self.assertEqual(self.input_list[index], element[1])

class TestEchoJsonInputs(unittest.TestCase):
    def setUp(self):
        self.mock_output = MockOutput()
        self.expected_output = ['[2, [1, 2]]\n','[1, [3,4,5]]\n', '[0, {"a": 1}]\n']
        self.file = open('sample-input', 'r+')

    def test_writes_into_output(self):
        two.echo_json_inputs(self.file, self.mock_output)
        self.assertTrue(len(self.mock_output.results) > 0)

    def test_expected_output_from_sample_input(self):
        two.echo_json_inputs(self.file, self.mock_output)
        self.assertTrue(self.mock_output.equal(self.expected_output))

class TestGetJsonInputs(unittest.TestCase):
    def setUp(self):
        self.expected_output = ['[1, 2]', '[3,4,5]', '{"a": 1}']
        self.expected_output_edge_cases = ['[1, 2]']

    def test_empty_list_from_empty_source(self):
        self.assertEqual([], two.get_json_inputs(open('sample-input-empty', 'r+')))

    def test_expected_output_from_sample_input(self):
        self.assertEqual(self.expected_output, 
            two.get_json_inputs(open('sample-input', 'r+')))

    def test_filter_out_non_json(self):
        self.assertEqual(self.expected_output_edge_cases, 
            two.get_json_inputs(open('sample-input-non-json', 'r+')))

    def test_end_at_control_d(self):
        self.assertEqual(self.expected_output_edge_cases,
            two.get_json_inputs(open('sample-input-control-d', 'r+')))

    def test_end_at_control_c(self):
        self.assertEqual(self.expected_output_edge_cases,
            two.get_json_inputs(open('sample-input-control-c', 'r+')))

    def test_end_at_end_of_file(self):
        self.assertEqual(self.expected_output_edge_cases,
            two.get_json_inputs(open('sample-input-end-of-line', 'r+')))

    def test_expected_output_from_multiline_json(self):
        self.assertEqual(self.expected_output_edge_cases,
            two.get_json_inputs(open('sample-input-multiline', 'r+')))

    def test_timeout_after_ten_seconds_of_inactivity(self):
        start = time.time()
        two.get_json_inputs(sys.stdin)
        end = time.time() - start
        self.assertTrue(end >= 10)

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestIsJson)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestConcatenateJsonInputs)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestEchoJsonInputs)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(TestGetJsonInputs)
    alltests = unittest.TestSuite([suite1, suite2, suite3, suite4])
    unittest.TextTestRunner(verbosity=2).run(alltests)
