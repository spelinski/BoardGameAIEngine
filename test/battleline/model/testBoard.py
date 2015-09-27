import unittest
from battleline.model.Board import Board, FlagNotFoundError


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_is_empty_to_begin_with(self):
        for flag in xrange(1, 10):
            self.assertTrue(self.board.get_flag(flag).is_empty())

    def test_board_cannot_get_invalid_flags(self):
        self.assertRaisesRegexp(
            FlagNotFoundError, "Flag Index 0 is invalid", self.board.get_flag, 0)
        self.assertRaisesRegexp(
            FlagNotFoundError, "Flag Index 10 is invalid", self.board.get_flag, 10)

    def test_board_has_nine_distinct_flags(self):
        board_flags = [self.board.get_flag(x) for x in xrange(1, 10)]
        self.assertEquals(9, len(set(board_flags)))

    def test_getting_a_flag_at_one_index_is_repeatable(self):
        self.assertEquals(self.board.get_flag(1), self.board.get_flag(1))
