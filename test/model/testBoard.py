import unittest
from battleline.model.Board import Board, FlagNotFoundError
class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_is_empty_to_begin_with(self):
        for flag in xrange(1,11):
            self.assertTrue(self.board.get_flag(flag).is_empty())

    def test_board_cannot_get_invalid_flags(self):
        self.assertRaisesRegexp(FlagNotFoundError, "Flag Index 0 is invalid", self.board.get_flag, 0)
        self.assertRaisesRegexp(FlagNotFoundError, "Flag Index 11 is invalid", self.board.get_flag, 11)
