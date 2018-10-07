import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from query_board import QueryBoard
from action_board import ActionBoard
from Admin.components import Height, Worker
from Common.components import Direction

class TestCell(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard().query_board
        self.incomplete_board = ActionBoard([[Height(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]]).query_board

    def test_origin(self):
        self.assertEqual(self.incomplete_board.cell(0, 0), Height(1))

    def test_valid_coordinates(self):
        self.assertEqual(self.incomplete_board.cell(1, 1), Height(4))

    def test_x_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.cell(-1, 2)
        with self.assertRaises(ValueError):
            self.board.cell(7, 2)

    def test_y_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.board.cell(3, -5)
        with self.assertRaises(ValueError):
            self.board.cell(3, 6)

    def test_return_worker(self):
        self.assertEqual(self.incomplete_board.cell(1, 0), Worker(2))


class TestNeighbor(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard().query_board
        self.incomplete_board = ActionBoard([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]]).query_board

    def test_neighbor_exists(self):
        for direction in Direction:
            self.assertTrue(self.incomplete_board.neighbor(2, direction))

    def test_true_for_worker_neighbor(self):
        self.assertTrue(self.incomplete_board.neighbor(1, Direction.E))

    def test_true_for_height_neighbor(self):
        self.assertTrue(self.incomplete_board.neighbor(1, Direction.S))

    def test_neighbor_does_not_exist(self):
        self.assertFalse(self.incomplete_board.neighbor(1, Direction.W))

class TestOccupied(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard().query_board
        self.incomplete_board = ActionBoard([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]]).query_board

    def test_true_if_worker(self):
        self.assertTrue(self.incomplete_board.occupied(2, Direction.W))
    
    def test_false_if_height(self):
        self.assertFalse(self.incomplete_board.occupied(1, Direction.S))

    def test_false_if_out_of_bounds(self):
        self.assertFalse(self.incomplete_board.occupied(1, Direction.W))


class TestNeighborHeight(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard().query_board
        self.incomplete_board = ActionBoard([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]]).query_board
    
    def test_height_of_neighbor(self):
        self.assertEqual(self.incomplete_board.neighbor_height(1, Direction.E), 0)
        self.assertEqual(self.incomplete_board.neighbor_height(2, Direction.S), 4)
        self.assertEqual(self.incomplete_board.neighbor_height(2, Direction.E), 0)

    def test_error_if_no_neighbor(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.neighbor_height(1, Direction.W)

    def test_error_if_invalid_id(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.neighbor_height(20, Direction.S)

    def test_error_if_empty_board(self):
        with self.assertRaises(ValueError):
            self.board.neighbor_height(1, Direction.N)

class TestGetWorkerPosition(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard().query_board
        self.incomplete_board = ActionBoard([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]]).query_board

    def test_get_correct_position(self):
        self.assertEqual(self.incomplete_board.get_worker_position(1), (0, 0))
        self.assertEqual(self.incomplete_board.get_worker_position(2), (1, 0))

    def test_error_given_invalid_id(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.get_worker_position(20)

    def test_error_with_empty_board(self):
        with self.assertRaises(ValueError):
            self.board.get_worker_position(1)

class TestWorkers(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard().query_board
        self.incomplete_board = ActionBoard([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]]).query_board

    def test_empty_list_with_empty_board(self):
        self.assertEqual(self.board.workers, [])

    def test_worker_ids_with_filled_board(self):
        self.assertEqual(self.incomplete_board.workers, [1, 2])


test_cases = [TestCell, TestNeighborHeight, TestNeighbor, TestGetWorkerPosition, TestOccupied, TestWorkers]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)