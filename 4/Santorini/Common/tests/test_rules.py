import unittest
import sys, os
sys.path.append(os.path.realpath("../.."))
from Common.components import Rules, Direction

class TestInit(unittest.TestCase):
    def setUp(self):
        self.rule_true = lambda x, y, z: True
        self.rule_false = lambda x, y, z: False
        self.all_true = [self.rule_true] * 3
        self.all_false = [self.rule_false] * 3
        self.true_and_false = [self.rule_true, self.rule_false]

    def test_move_and_build_rules(self):
        rules = Rules(self.all_true, self.all_false)
        self.assertEqual(rules.move_rules, self.all_true)
        self.assertEqual(rules.build_rules, self.all_false)

class TestCheckMove(unittest.TestCase):
    def setUp(self):
        self.rule_true = lambda x, y, z: True
        self.rule_false = lambda x, y, z: False
        self.all_true = [self.rule_true] * 3
        self.all_false = [self.rule_false] * 3
        self.true_and_false = [self.rule_true, self.rule_false]

    def test_true_with_all_true(self):
        rules = Rules(self.all_true, self.all_false)
        self.assertTrue(rules.check_move([[]], 1, Direction.N))
    
    def test_false_with_all_false(self):
        rules = Rules(self.all_false, self.all_true)
        self.assertFalse(rules.check_move([[]], 1, Direction.N))

    def test_false_with_true_and_false(self):
        rules = Rules(self.true_and_false, self.all_true)
        self.assertFalse(rules.check_move([[]], 1, Direction.N))

class TestCheckBuild(unittest.TestCase):
    def setUp(self):
        self.rule_true = lambda x, y, z: True
        self.rule_false = lambda x, y, z: False
        self.all_true = [self.rule_true] * 3
        self.all_false = [self.rule_false] * 3
        self.true_and_false = [self.rule_true, self.rule_false]

    def test_true_with_all_true(self):
        rules = Rules(self.all_false, self.all_true)
        self.assertTrue(rules.check_build([[]], 1, Direction.N))
    
    def test_false_with_all_false(self):
        rules = Rules(self.all_true, self.all_false)
        self.assertFalse(rules.check_build([[]], 1, Direction.N))

    def test_false_with_true_and_false(self):
        rules = Rules(self.all_true, self.true_and_false)
        self.assertFalse(rules.check_build([[]], 1, Direction.N))

test_cases = [TestInit, TestCheckBuild, TestCheckMove]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)
