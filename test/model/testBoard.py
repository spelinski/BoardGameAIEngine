import unittest
from battleline.model.Board import Board
class TestBoard(unittest.TestCase):
    def test_board_is_empty_to_begin_with(self):
        board = Board()
        for flag in xrange(1,11):
            self.assertTrue(board.get_flag(flag).is_empty())
