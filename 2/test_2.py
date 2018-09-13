import unittest
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

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestIsJson)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestConcatenateJsonInputs)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestEchoJsonInputs)
    alltests = unittest.TestSuite([suite1, suite2, suite3])
    unittest.TextTestRunner(verbosity=2).run(alltests)
