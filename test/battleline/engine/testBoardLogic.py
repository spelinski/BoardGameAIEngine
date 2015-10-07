import unittest
from battleline.engine.BoardLogic import BoardLogic
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Flag import TooManyCardsOnOneSideError, FlagAlreadyClaimedError
from battleline.Identifiers import Identifiers


class TestBoardLogic(unittest.TestCase):

    def setUp(self):
        self.logic = FormationLogic()
        self.boardLogic = BoardLogic()
        self.fullList = [(1, 'blue'), (2, 'blue'), (3, 'blue'), (4, 'blue'), (5, 'blue'), (6, 'blue'), (7, 'blue'), (8, 'blue'), (9, 'blue'), (10, 'blue'), (1, 'red'), (2, 'red'), (3, 'red'), (4, 'red'), (5, 'red'), (6, 'red'), (7, 'red'), (8, 'red'), (9, 'red'), (10, 'red'), (1, 'green'), (2, 'green'), (3, 'green'), (4, 'green'), (5, 'green'), (6, 'green'), (7, 'green'), (8, 'green'), (9, 'green'), (10, 'green'), (1, 'orange'), (
            2, 'orange'), (3, 'orange'), (4, 'orange'), (5, 'orange'), (6, 'orange'), (7, 'orange'), (8, 'orange'), (9, 'orange'), (10, 'orange'), (1, 'purple'), (2, 'purple'), (3, 'purple'), (4, 'purple'), (5, 'purple'), (6, 'purple'), (7, 'purple'), (8, 'purple'), (9, 'purple'), (10, 'purple'), (1, 'yellow'), (2, 'yellow'), (3, 'yellow'), (4, 'yellow'), (5, 'yellow'), (6, 'yellow'), (7, 'yellow'), (8, 'yellow'), (9, 'yellow'), (10, 'yellow')]

    """test_checkAllFlags_empty

    test if the checkAllFlags function will work on an empty board
    """

    def test_checkAllFlags_empty(self):
        self.boardLogic.checkAllFlags(Identifiers.NORTH)
        for flag in self.boardLogic.board.flags:
            self.assertEquals(flag.is_claimed(), False)

    """test_checkAllFlags_FlagContested_basic

    test if the checkAllFlags function will work on a non-empty board
    """

    def test_checkAllFlags_FlagContested_basic(self):
        # flag 1: 10-9-8 vs 1-2-3
        self.boardLogic.addCard(0, Identifiers.NORTH, (10, 'blue'))
        self.boardLogic.addCard(0, Identifiers.SOUTH, (1, 'blue'))

        self.boardLogic.addCard(0, Identifiers.NORTH, (9, 'blue'))
        self.boardLogic.addCard(0, Identifiers.SOUTH, (2, 'blue'))

        self.boardLogic.addCard(0, Identifiers.NORTH, (8, 'blue'))
        with self.assertRaisesRegexp(FlagAlreadyClaimedError, "south is attempting to place card on already claimed flag."):
            self.boardLogic.addCard(0, Identifiers.SOUTH, (3, 'blue'))
        self.assertEqual(self.boardLogic.board.flags[
                         0].claimed, Identifiers.NORTH)

        # flag 2: 10R-9R-8R vs 1-2-3
        self.boardLogic.addCard(1, Identifiers.SOUTH, (1, 'red'))
        self.boardLogic.addCard(1, Identifiers.NORTH, (10, 'red'))

        self.boardLogic.addCard(1, Identifiers.SOUTH, (2, 'red'))
        self.boardLogic.addCard(1, Identifiers.NORTH, (9, 'red'))

        self.boardLogic.addCard(1, Identifiers.SOUTH, (3, 'red'))
        self.boardLogic.addCard(1, Identifiers.NORTH, (8, 'red'))
        self.assertEqual(self.boardLogic.board.flags[
                         1].claimed, Identifiers.NORTH)

        # flag 3: 10-9-_ vs 1-2-3 (8 is played on flag 9)
        self.boardLogic.addCard(8, Identifiers.SOUTH, (8, 'green'))

        self.boardLogic.addCard(2, Identifiers.NORTH, (10, 'green'))
        self.boardLogic.addCard(2, Identifiers.SOUTH, (1, 'green'))

        self.boardLogic.addCard(2, Identifiers.NORTH, (9, 'green'))
        self.boardLogic.addCard(2, Identifiers.SOUTH, (2, 'green'))

        self.boardLogic.addCard(8, Identifiers.NORTH, (5, 'blue'))
        self.boardLogic.addCard(2, Identifiers.SOUTH, (3, 'green'))

        self.assertEqual(self.boardLogic.board.flags[
                         2].claimed, Identifiers.SOUTH)

    """test_checkAllFlags_FlagContested_tied

    test if the checkAllFlags function will work when both formations and values are exactly the same
    """

    def test_checkAllFlags_FlagContested_tied(self):
        # flag 5: 7-6-5(yellow) vs 7-6-5(purple)
        self.boardLogic.addCard(4, Identifiers.NORTH, (7, 'yellow'))
        self.boardLogic.addCard(4, Identifiers.SOUTH, (7, 'purple'))

        self.boardLogic.addCard(4, Identifiers.NORTH, (6, 'yellow'))
        self.boardLogic.addCard(4, Identifiers.SOUTH, (6, 'purple'))

        self.boardLogic.addCard(4, Identifiers.NORTH, (5, 'yellow'))
        self.boardLogic.addCard(4, Identifiers.SOUTH, (5, 'purple'))

        self.assertEqual(self.boardLogic.board.flags[
                         4].claimed, Identifiers.NORTH)

        # flag 6: 3-2-1(yellow) vs 3-2-1(purple)
        self.boardLogic.addCard(5, Identifiers.SOUTH, (3, 'purple'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (3, 'yellow'))

        self.boardLogic.addCard(5, Identifiers.SOUTH, (2, 'purple'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (2, 'yellow'))

        self.boardLogic.addCard(5, Identifiers.SOUTH, (1, 'purple'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (1, 'yellow'))
        self.assertEqual(self.boardLogic.board.flags[
                         5].claimed, Identifiers.SOUTH)

    def test_flag_is_playable(self):
        self.assertTrue(self.boardLogic.is_flag_playable(0, Identifiers.NORTH))
        self.assertTrue(self.boardLogic.is_flag_playable(0, Identifiers.SOUTH))

        self.boardLogic.board.get_flag(1).sides[Identifiers.NORTH] = [1, 2, 3]

        self.assertFalse(
            self.boardLogic.is_flag_playable(0, Identifiers.NORTH))
        self.assertTrue(self.boardLogic.is_flag_playable(0, Identifiers.SOUTH))

    def test_check_breakthrough(self):
        #3 adjacent flags.
        self.assertFalse(self.boardLogic.is_game_over())
        self.boardLogic.addCard(4, Identifiers.NORTH, (9, 'yellow'))
        self.boardLogic.addCard(4, Identifiers.NORTH, (8, 'yellow'))
        self.boardLogic.addCard(4, Identifiers.NORTH, (7, 'yellow'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (9, 'red'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (8, 'red'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (7, 'red'))
        self.boardLogic.addCard(6, Identifiers.NORTH, (9, 'blue'))
        self.boardLogic.addCard(6, Identifiers.NORTH, (8, 'blue'))
        self.boardLogic.addCard(6, Identifiers.NORTH, (7, 'blue'))
        self.assertTrue(self.boardLogic.is_game_over())
        self.assertEqual(self.boardLogic.get_game_winner(), Identifiers.NORTH)

    def test_check_envelopment(self):
        #5 flags.
        self.assertFalse(self.boardLogic.is_game_over())
        self.boardLogic.addCard(1, Identifiers.NORTH, (9, 'yellow'))
        self.boardLogic.addCard(1, Identifiers.NORTH, (8, 'yellow'))
        self.boardLogic.addCard(1, Identifiers.NORTH, (7, 'yellow'))
        self.boardLogic.addCard(2, Identifiers.NORTH, (9, 'red'))
        self.boardLogic.addCard(2, Identifiers.NORTH, (8, 'red'))
        self.boardLogic.addCard(2, Identifiers.NORTH, (7, 'red'))
        self.boardLogic.addCard(4, Identifiers.NORTH, (9, 'blue'))
        self.boardLogic.addCard(4, Identifiers.NORTH, (8, 'blue'))
        self.boardLogic.addCard(4, Identifiers.NORTH, (7, 'blue'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (9, 'purple'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (8, 'purple'))
        self.boardLogic.addCard(5, Identifiers.NORTH, (7, 'purple'))
        self.boardLogic.addCard(7, Identifiers.NORTH, (9, 'green'))
        self.boardLogic.addCard(7, Identifiers.NORTH, (8, 'green'))
        self.boardLogic.addCard(7, Identifiers.NORTH, (7, 'green'))
        self.assertTrue(self.boardLogic.is_game_over())
        self.assertEqual(self.boardLogic.get_game_winner(), Identifiers.NORTH)


