import unittest
from battleline.engine.BoardLogic import BoardLogic
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Flag import TooManyCardsOnOneSideError, FlagAlreadyClaimedError


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
        self.boardLogic.checkAllFlags(self.boardLogic.PLAYER_NORTH)
        for flag in self.boardLogic.board.flags:
            self.assertEquals(flag.is_claimed(), False)

    """test_checkAllFlags_FlagContested_basic

    test if the checkAllFlags function will work on a non-empty board
    """

    def test_checkAllFlags_FlagContested_basic(self):
        # flag 1: 10-9-8 vs 1-2-3
        self.boardLogic.addCard(0, self.boardLogic.PLAYER_NORTH, (10, 'blue'))
        self.boardLogic.addCard(0, self.boardLogic.PLAYER_SOUTH, (1, 'blue'))

        self.boardLogic.addCard(0, self.boardLogic.PLAYER_NORTH, (9, 'blue'))
        self.boardLogic.addCard(0, self.boardLogic.PLAYER_SOUTH, (2, 'blue'))

        self.boardLogic.addCard(0, self.boardLogic.PLAYER_NORTH, (8, 'blue'))
        with self.assertRaisesRegexp(FlagAlreadyClaimedError, "Player South is attempting to place card on already claimed flag."):
            self.boardLogic.addCard(
                0, self.boardLogic.PLAYER_SOUTH, (3, 'blue'))
        self.assertEqual(self.boardLogic.board.flags[
                         0].claimed, self.boardLogic.PLAYER_NORTH)

        # flag 2: 10R-9R-8R vs 1-2-3
        self.boardLogic.addCard(1, self.boardLogic.PLAYER_SOUTH, (1, 'red'))
        self.boardLogic.addCard(1, self.boardLogic.PLAYER_NORTH, (10, 'red'))

        self.boardLogic.addCard(1, self.boardLogic.PLAYER_SOUTH, (2, 'red'))
        self.boardLogic.addCard(1, self.boardLogic.PLAYER_NORTH, (9, 'red'))

        self.boardLogic.addCard(1, self.boardLogic.PLAYER_SOUTH, (3, 'red'))
        self.boardLogic.addCard(1, self.boardLogic.PLAYER_NORTH, (8, 'red'))
        self.assertEqual(self.boardLogic.board.flags[
                         1].claimed, self.boardLogic.PLAYER_NORTH)

        # flag 3: 10-9-_ vs 1-2-3 (8 is played on flag 9)
        self.boardLogic.addCard(8, self.boardLogic.PLAYER_SOUTH, (8, 'green'))

        self.boardLogic.addCard(2, self.boardLogic.PLAYER_NORTH, (10, 'green'))
        self.boardLogic.addCard(2, self.boardLogic.PLAYER_SOUTH, (1, 'green'))

        self.boardLogic.addCard(2, self.boardLogic.PLAYER_NORTH, (9, 'green'))
        self.boardLogic.addCard(2, self.boardLogic.PLAYER_SOUTH, (2, 'green'))

        self.boardLogic.addCard(8, self.boardLogic.PLAYER_NORTH, (5, 'blue'))
        self.boardLogic.addCard(2, self.boardLogic.PLAYER_SOUTH, (3, 'green'))

        self.assertEqual(self.boardLogic.board.flags[
                         2].claimed, self.boardLogic.PLAYER_SOUTH)

    """test_checkAllFlags_FlagContested_tied

    test if the checkAllFlags function will work when both formations and values are exactly the same
    """

    def test_checkAllFlags_FlagContested_tied(self):
        # flag 5: 7-6-5(yellow) vs 7-6-5(purple)
        self.boardLogic.addCard(4, self.boardLogic.PLAYER_NORTH, (7, 'yellow'))
        self.boardLogic.addCard(4, self.boardLogic.PLAYER_SOUTH, (7, 'purple'))

        self.boardLogic.addCard(4, self.boardLogic.PLAYER_NORTH, (6, 'yellow'))
        self.boardLogic.addCard(4, self.boardLogic.PLAYER_SOUTH, (6, 'purple'))

        self.boardLogic.addCard(4, self.boardLogic.PLAYER_NORTH, (5, 'yellow'))
        self.boardLogic.addCard(4, self.boardLogic.PLAYER_SOUTH, (5, 'purple'))

        self.assertEqual(self.boardLogic.board.flags[
                         4].claimed, self.boardLogic.PLAYER_NORTH)

        # flag 6: 3-2-1(yellow) vs 3-2-1(purple)
        self.boardLogic.addCard(5, self.boardLogic.PLAYER_SOUTH, (3, 'purple'))
        self.boardLogic.addCard(5, self.boardLogic.PLAYER_NORTH, (3, 'yellow'))

        self.boardLogic.addCard(5, self.boardLogic.PLAYER_SOUTH, (2, 'purple'))
        self.boardLogic.addCard(5, self.boardLogic.PLAYER_NORTH, (2, 'yellow'))

        self.boardLogic.addCard(5, self.boardLogic.PLAYER_SOUTH, (1, 'purple'))
        self.boardLogic.addCard(5, self.boardLogic.PLAYER_NORTH, (1, 'yellow'))
        self.assertEqual(self.boardLogic.board.flags[
                         5].claimed, self.boardLogic.PLAYER_SOUTH)
