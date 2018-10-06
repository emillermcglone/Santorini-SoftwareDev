import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board import Board
from Admin.components import Height, Worker
from Common.components import Direction

class TestInit(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.incomplete_board = Board([[Height(1), Height(2)], [Height(3), Height(4), Height(5)], [Height(1)]])
        self.expanded_board = Board([[1] * 8] * 10)

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

class TestIsGameOver(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.expanded_board = Board([[1] * 8] * 10)
        self.height_of_six = lambda g: len(g) == 6

    def test_true_win_condition(self):
        self.assertTrue(self.board.is_game_over(self.height_of_six))

    def test_false_win_condition(self):
        self.assertFalse(self.expanded_board.is_game_over(self.height_of_six))

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_same_empty_board(self):
        self.assertEqual(self.board.board, [[Height(0)] * 6] * 6)

    def test_does_not_mutate(self):
        grid = self.board.board
        grid[0][0] = Height(5)
        self.assertEqual(self.board.board, [[Height(0)] * 6] * 6)


class TestCell(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.incomplete_board = Board([[Height(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])

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
        self.board = Board()
        self.incomplete_board = Board([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])

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
        self.board = Board()
        self.incomplete_board = Board([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])

    def test_true_if_worker(self):
        self.assertTrue(self.incomplete_board.occupied(2, Direction.W))
    
    def test_false_if_height(self):
        self.assertFalse(self.incomplete_board.occupied(1, Direction.S))

    def test_false_if_out_of_bounds(self):
        self.assertFalse(self.incomplete_board.occupied(1, Direction.W))


class TestNeighborHeight(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.incomplete_board = Board([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])
    
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
        self.board = Board()
        self.incomplete_board = Board([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])

    def test_get_correct_position(self):
        self.assertEqual(self.incomplete_board.get_worker_position(1), (0, 0))
        self.assertEqual(self.incomplete_board.get_worker_position(2), (1, 0))

    def test_error_given_invalid_id(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.get_worker_position(20)

    def test_error_with_empty_board(self):
        with self.assertRaises(ValueError):
            self.board.get_worker_position(1)

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.board = Board()
    
    def test_place_worker(self):
        self.board.place(1, 0, 0)
        self.board.place(2, 2, 1)
        self.assertEqual(self.board.cell(0, 0), Worker(0))
        self.assertEqual(self.board.cell(2, 1), Worker(0))

    def test_replace_worker(self):
        self.board.place(4, 0, 5)
        self.board.place(5, 0, 5)
        worker = self.board.cell(0, 5)
        self.assertEqual(worker.id, 5)
    
    def test_error_given_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            self.board.place(3, 0, 7)


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.incomplete_board = Board([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])

    def test_move_to_open_cell(self):
        self.assertEqual(self.incomplete_board.get_worker_position(2), (1, 0))
        self.assertFalse(self.incomplete_board.occupied(2, Direction.S))
        self.incomplete_board.move(2, Direction.S)
        self.assertEqual(self.incomplete_board.get_worker_position(2), (1, 1))

    def test_move_to_worker(self):
        self.assertEqual(self.incomplete_board.get_worker_position(2), (1, 0))
        self.assertTrue(self.incomplete_board.occupied(2, Direction.W))
        self.incomplete_board.move(2, Direction.W)
        self.assertEqual(self.incomplete_board.get_worker_position(2), (0, 0))
        
        with self.assertRaises(ValueError):
            self.incomplete_board.get_worker_position(1)

    def test_error_if_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.move(1, Direction.W)

    def test_updates_from_cell(self):
        self.incomplete_board.move(2, Direction.W)
        with self.assertRaises(ValueError):
            self.incomplete_board.get_worker_position(1)

class TestBuild(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.incomplete_board = Board([[Worker(1), Worker(2)], [Height(3), Height(4), Height(5)], [Height(1)]])

    def test_build_on_height(self):
        self.assertEqual(self.incomplete_board.neighbor_height(1, Direction.S), 3)
        self.incomplete_board.build(1, Direction.S)
        self.assertEqual(self.incomplete_board.neighbor_height(1, Direction.S), 4)

    def test_replace_worker(self):
        self.assertEqual(self.incomplete_board.neighbor_height(1, Direction.E), 0)
        self.incomplete_board.build(1, Direction.E)
        self.assertEqual(self.incomplete_board.neighbor_height(1, Direction.E), 1)
        self.assertFalse(self.incomplete_board.occupied(1, Direction.E))

    def test_build_height_above_four(self):
        self.assertEqual(self.incomplete_board.neighbor_height(2, Direction.S), 4)
        self.incomplete_board.build(2, Direction.S)
        self.assertEqual(self.incomplete_board.neighbor_height(2, Direction.S), 5)

    def test_error_if_out_of_bounds(self):
        self.assertFalse(self.incomplete_board.neighbor(1, Direction.W))
        with self.assertRaises(ValueError):
            self.incomplete_board.build(1, Direction.W)

    def test_error_if_worker_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.incomplete_board.build(20, Direction.S)


test_cases = [TestInit, TestIsGameOver, TestBoard, TestCell, TestNeighbor, 
TestOccupied, TestNeighborHeight, TestGetWorkerPosition, TestPlace, 
TestMove, TestBuild]
    
if __name__ == "__main__":
    test_suites = list(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
    alltests = unittest.TestSuite(test_suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)