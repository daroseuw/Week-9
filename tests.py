import unittest
from logic import *

moves = Moves()
gameboard = Board()
players = Players()

class TestLogic(unittest.TestCase):

    def test_get_winner_diag(self):
        board = [
            ['X', ' ', '0'],
            [' ', 'X', ' '],
            [' ', 'O', 'X']
        ]
        self.assertEqual(moves.check_for_win(board), True)

    def test_get_winner_horizontal(self):
        board = [
            ['X', 'X', 'X'],
            [' ', 'O', ' '],
            ['O', 'O', 'X']
        ]
        self.assertEqual(moves.check_for_win(board), True)

    def test_get_winner_vertical(self):
        board = [
            ['X', 'O', 'X'],
            ['X', 'O', ' '],
            ['O', 'O', 'X']
        ]
        self.assertEqual(moves.check_for_win(board), True)
    
    def test_board_full(self):
        board = [
        ['X','O','X'],
        ['O','X','O'],
        ['X','O','X']
        ]
        self.assertEqual(gameboard.board_full(board), True)

    # TODO: Test all functions from logic.py!


if __name__ == '__main__':
    unittest.main()