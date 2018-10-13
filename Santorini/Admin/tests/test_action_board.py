import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from action_board import ActionBoard
from Admin.components import Height, Worker
from Common.components import Direction

class TestInit(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.incomplete_board = ActionBoard([[Height(1), Height(2)], [Height(3), Height(4), Height(5)], [Height(1)]])
        self.expanded_board = ActionBoard([[1] * 8] * 10)

    def test_width_height_six(self):
        grid = self.board.board
        self.assertEqual(len(grid), 6)
        self.assertTrue(all(map(lambda l: len(l) == 6, grid)))
    
    def test_complete_board(self):
        grid = self.incomplete_board.board
        self.assertEqual(len(grid), 6)
        self.assertTrue(all(map(lambda l: len(l) == 6, grid)))

    def test_expanded_board(self):
        grid = self.expanded_board.board
        self.assertEqual(len(grid), 10)
        self.assertTrue(all(map(lambda l: len(l) == 8, grid)))


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()

    def test_same_empty_ActionBoard(self):
        self.assertEqual(self.board.board, [[Height(0)] * 6] * 6)

    def test_does_not_mutate(self):
        grid = self.board.board
        grid[0][0] = Height(5)
        self.assertEqual(self.board.board, [[Height(0)] * 6] * 6)


class TestPlace(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.incomplete_board = ActionBoard([[Worker(1, 0), Worker(2, 0)], [Height(3), Height(4), Height(5)], [Height(1)]])
    
    def test_place_worker(self):
        self.board.place(1, 0, 0, 0)
        self.board.place(2, 0, 2, 1)
        self.assertEqual(self.board.query_board.cell(0, 0), Worker(1, 0))
        self.assertEqual(self.board.query_board.cell(2, 1), Worker(2, 0))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

    def test_replace_worker(self):
        self.board.place(4, 0, 0, 5)
        self.board.place(5, 0, 0, 5)
        worker = self.board.query_board.cell(0, 5)
        self.assertEqual(worker.id, 5)
    
    def test_error_given_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            self.board.place(3, 0, 0, 7)

    def test_error_given_existing_id(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.place(1, 0, 0, 0)


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.incomplete_board = ActionBoard([[Worker(1, 0), Worker(2, 0)], [Height(3), Height(4), Height(5)], [Height(1)]])

    def test_move_to_open_cell(self):
        self.assertEqual(self.incomplete_board.query_board.get_worker_position(2), (1, 0))
        self.assertFalse(self.incomplete_board.query_board.occupied(2, Direction.S))
        self.incomplete_board.move(2, Direction.S)
        self.assertEqual(self.incomplete_board.query_board.get_worker_position(2), (1, 1))

    def test_move_to_worker(self):
        self.assertEqual(self.incomplete_board.query_board.get_worker_position(2), (1, 0))
        self.assertTrue(self.incomplete_board.query_board.occupied(2, Direction.W))
        self.incomplete_board.move(2, Direction.W)
        self.assertEqual(self.incomplete_board.query_board.get_worker_position(2), (0, 0))
        
        with self.assertRaises(ValueError):
            self.incomplete_board.query_board.get_worker_position(1)

    def test_error_if_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.move(1, Direction.W)

    def test_updates_from_cell(self):
        self.incomplete_board.move(2, Direction.W)
        with self.assertRaises(ValueError):
            self.incomplete_board.query_board.get_worker_position(1)

class TestBuild(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.incomplete_board = ActionBoard([[Worker(1, 0), Worker(2, 0)], [Height(3), Height(4), Height(5)], [Height(1)]])

    def test_build_on_height(self):
        self.assertEqual(self.incomplete_board.query_board.neighbor_height(1, Direction.S), 3)
        self.incomplete_board.build(1, Direction.S)
        self.assertEqual(self.incomplete_board.query_board.neighbor_height(1, Direction.S), 4)

    def test_replace_worker(self):
        self.assertEqual(self.incomplete_board.query_board.neighbor_height(1, Direction.E), 0)
        self.incomplete_board.build(1, Direction.E)
        self.assertEqual(self.incomplete_board.query_board.neighbor_height(1, Direction.E), 1)
        self.assertFalse(self.incomplete_board.query_board.occupied(1, Direction.E))

    def test_build_height_above_four(self):
        self.assertEqual(self.incomplete_board.query_board.neighbor_height(2, Direction.S), 4)
        self.incomplete_board.build(2, Direction.S)
        self.assertEqual(self.incomplete_board.query_board.neighbor_height(2, Direction.S), 5)

    def test_error_if_out_of_bounds(self):
        self.assertFalse(self.incomplete_board.query_board.neighbor(1, Direction.W))
        with self.assertRaises(ValueError):
            self.incomplete_board.build(1, Direction.W)

    def test_error_if_worker_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.build(20, Direction.S)


class TestQueryBoard(unittest.TestCase):
    def setUp(self):
        self.board = ActionBoard()
        self.q_board = self.board.query_board
        self.incomplete_board = ActionBoard([[Worker(1, 0), Worker(2, 0)], [Height(3), Height(4), Height(5)], [Height(1)]])
        self.q_incomplete_board = self.incomplete_board.query_board

    def test_place(self):
        self.assertEqual(self.q_board.cell(0, 0), Height(0))
        self.board.place(1, 0, 0, 0)
        self.assertEqual(self.q_board.cell(0, 0), Worker(1, 0, 0))

    def test_move(self):
        self.assertEqual(self.q_incomplete_board.get_worker_position(1), (0, 0))
        self.incomplete_board.move(1, Direction.E)
        self.assertEqual(self.q_incomplete_board.get_worker_position(1), (1, 0))

    def test_build(self):
        self.assertEqual(self.q_incomplete_board.neighbor_height(1, Direction.S), 3)
        self.incomplete_board.build(1, Direction.S)
        self.assertEqual(self.q_incomplete_board.neighbor_height(1, Direction.S), 4)

test_cases = [TestInit, TestBoard, TestPlace, TestMove, TestBuild, TestQueryBoard]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)