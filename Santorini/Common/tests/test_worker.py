import unittest
from ..components import Worker


class TestInit(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(1, (0, 0))
        
    def test_id(self):
        self.assertEqual(self.worker.id, 1)

    def test_position(self):
        self.assertEqual(self.worker.position, (0, 0))
    
    def test_default_height(self):
        self.assertEqual(self.worker.height, 0)

    def test_height_below_zero_error(self):
        with self.assertRaises(ValueError):
            Worker(1, (0, 0), -1)

    def test_height_above_four_error(self):
        with self.assertRaises(ValueError):
            Worker(1, (0, 0), 5)

    def test_height_equals_zero(self):
        self.assertEqual(Worker(1, (0,0), 0).height, 0)

    def test_height_equals_four(self):
        self.assertEqual(Worker(1, (0, 0), 4).height, 4)

class TestHeightProperty(unittest.TestCase):
    def setUp(self):
        self.given_height = 3
        self.worker = Worker(1, (0, 0), self.given_height)
    
    def test_height_returns_given_height(self):
        self.assertEqual(self.worker.height, self.given_height)

class TestHeightSetter(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(1, (0, 0))

    def test_change_height_within_boundaries(self):
        self.assertEqual(self.worker.height, 0)
        self.worker.height = 1
        self.assertEqual(self.worker.height, 1)

    def test_change_height_below_zero(self):
        self.assertEqual(self.worker.height, 0)
        with self.assertRaises(ValueError):
            self.worker.height = -1

    def test_change_height_above_four(self):
        self.assertEqual(self.worker.height, 0)
        with self.assertRaises(ValueError):
            self.worker.height = 5
    
test_cases = [TestInit, TestHeightProperty, TestHeightSetter]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)


