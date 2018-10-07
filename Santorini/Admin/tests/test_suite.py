import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_direction import test_cases as direction_test_cases
from test_height import test_cases as height_test_cases
from test_rules import test_cases as rules_test_cases
from test_worker import test_cases as worker_test_cases
from test_action_board import test_cases as action_board_test_cases
from test_query_board import test_cases as query_board_test_cases

"""
Test program for Common components
"""

test_cases = direction_test_cases + height_test_cases + rules_test_cases + worker_test_cases + action_board_test_cases + query_board_test_cases


if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)