import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rules import SantoriniRules
from Admin.action_board import ActionBoard
from Admin.components import Worker, Height
from Common.components import Direction

class TestCheckPlace(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.q_board = self.board.query_board

        self.incomplete_board = ActionBoard([[Worker(1), Worker(2, 5)], [Height(3), Height(4), Height(5)], [Height(1)]])
        self.q_incomplete_board = self.incomplete_board.query_board

        self.rules_board = SantoriniRules(self.q_board)
        self.rules_incomplete = SantoriniRules(self.q_incomplete_board)


    def test_true_if_height_zero(self):
        self.assertTrue(self.rules_incomplete.check_place(2, 0))

    def test_false_if_height_above_zero(self):
        self.assertFalse(self.rules_incomplete.check_place(1, 1))

    def test_true_if_empty_cell(self):
        self.assertTrue(self.rules_incomplete.check_place(2, 0))

    def test_false_if_occupied_cell(self):
        self.assertFalse(self.rules_incomplete.check_place(0, 0))

    def test_true_if_worker_numbers_below_four(self):
        self.incomplete_board.place(3, 1, 1)
        self.assertEqual(len(self.q_incomplete_board.workers), 3)
        self.assertTrue(self.rules_incomplete.check_place(2, 2))

    def test_false_if_worker_numbers_above_four(self):
        self.incomplete_board.place(3, 1, 1)
        self.incomplete_board.place(4, 0, 1)
        self.assertEqual(len(self.q_incomplete_board.workers), 4)
        self.assertFalse(self.rules_incomplete.check_place(2, 2))

    def test_false_if_invalid_coordinates(self):
        self.assertFalse(self.rules_board.check_place(-1, 0))
        self.assertFalse(self.rules_board.check_place(6, 0))
        self.assertFalse(self.rules_board.check_place(0, -1))
        self.assertFalse(self.rules_board.check_place(0, 6))
        self.assertFalse(self.rules_board.check_place(-1, -1))
        self.assertFalse(self.rules_board.check_place(6, 6))


class TestCheckMove(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.q_board = self.board.query_board

        self.incomplete_board = ActionBoard([[Worker(1), Worker(2, 5), Worker(3, 0)], [Height(0), Height(3), Height(4)], [Height(1)]])
        self.q_incomplete_board = self.incomplete_board.query_board

        self.rules_board = SantoriniRules(self.q_board)
        self.rules_incomplete = SantoriniRules(self.q_incomplete_board)

    
    def test_true_if_destination_is_not_occupied(self):
        self.assertTrue(self.rules_incomplete.check_move(1, Direction.S))

    def test_false_if_destination_is_occupied(self):
        self.assertFalse(self.rules_incomplete.check_move(1, Direction.E))

    def test_true_if_destination_is_at_most_a_floor_heigher(self):
        self.assertTrue(self.rules_incomplete.check_move(2, Direction.S))

    def test_false_if_destination_is_more_than_a_floor_higher(self):
        self.assertFalse(self.rules_incomplete.check_move(3, Direction.SW))

    def test_true_if_destination_is_below_current_height(self):
        self.assertTrue(self.rules_incomplete.check_move(2, Direction.SW))
        self.assertTrue(self.rules_incomplete.check_move(1, Direction.S))

    def test_false_if_destination_is_at_least_four_floors(self):
        self.assertFalse(self.rules_incomplete.check_move(2, Direction.SE))

    def test_false_if_out_of_bounds(self):
        self.assertFalse(self.rules_incomplete.check_move(1, Direction.W))

    def test_false_if_worker_not_found(self):
        self.assertFalse(self.rules_incomplete.check_move(5, Direction.S))


class TestCheckBuild(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.q_board = self.board.query_board

        self.incomplete_board = ActionBoard([[Worker(1), Worker(2, 5), Worker(3, 0)], [Height(0), Height(3), Height(4)], [Height(1)]])
        self.q_incomplete_board = self.incomplete_board.query_board

        self.rules_board = SantoriniRules(self.q_board)
        self.rules_incomplete = SantoriniRules(self.q_incomplete_board)

    def test_true_if_unoccupied(self):
        self.assertTrue(self.rules_incomplete.check_build(1, Direction.S))
        self.assertTrue(self.rules_incomplete.check_build(1, Direction.SE))

    def test_false_if_occupied(self):
        self.assertFalse(self.rules_incomplete.check_build(1, Direction.E))
        self.assertFalse(self.rules_incomplete.check_build(2, Direction.W))

    def test_true_if_destination_height_is_below_four(self):
        self.assertTrue(self.rules_incomplete.check_build(1, Direction.S))
        self.assertTrue(self.rules_incomplete.check_build(1, Direction.SE))
        self.assertTrue(self.rules_incomplete.check_build(2, Direction.SW))
        self.assertTrue(self.rules_incomplete.check_build(2, Direction.S))

    def test_false_if_destination_height_is_at_least_four(self):
        self.assertFalse(self.rules_incomplete.check_build(3, Direction.S))
        self.assertFalse(self.rules_incomplete.check_build(2, Direction.SE))

    def test_false_if_invalid_destination(self):
        self.assertFalse(self.rules_incomplete.check_build(1, Direction.W))
        self.assertFalse(self.rules_incomplete.check_build(2, Direction.N))

    def test_false_if_worker_not_found(self):
        self.assertFalse(self.rules_incomplete.check_build(5, Direction.S))

class TestMoveAndBuild(unittest.TestCase):
    pass


test_cases = [TestCheckPlace, TestCheckMove, TestCheckBuild]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)