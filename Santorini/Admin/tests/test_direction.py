import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import Direction

class TestDirection(unittest.TestCase):
    def setUp(self):
        self.x, self.y = 0, 0

    def test_north(self):
        self.assertEqual(Direction.N(self.x, self.y), (0, -1))

    def test_south(self):
        self.assertEqual(Direction.S(self.x, self.y), (0, 1))

    def test_east(self):
        self.assertEqual(Direction.E(self.x, self.y), (1, 0))

    def test_west(self):
        self.assertEqual(Direction.W(self.x, self.y), (-1, 0))

    def test_north_east(self):
        self.assertEqual(Direction.NE(self.x, self.y), (1, -1))

    def test_north_west(self):
        self.assertEqual(Direction.NW(self.x, self.y), (-1, -1))

    def test_south_east(self):
        self.assertEqual(Direction.SE(self.x, self.y), (1, 1))
    
    def test_south_west(self):
        self.assertEqual(Direction.SW(self.x, self.y), (-1, 1))

test_cases = [TestDirection]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)