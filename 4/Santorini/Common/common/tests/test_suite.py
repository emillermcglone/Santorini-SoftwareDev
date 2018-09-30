import unittest
import sys, os

from .test_direction import test_cases as direction_test_cases
from .test_height import test_cases as height_test_cases
from .test_rules import test_cases as rules_test_cases
from .test_worker import test_cases as worker_test_cases

"""
Test program for Common components
"""

if __name__ == "__main__":
    test_cases = direction_test_cases + height_test_cases + rules_test_cases + worker_test_cases
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)