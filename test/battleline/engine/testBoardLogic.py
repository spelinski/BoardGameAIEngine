import unittest
from battleline.engine.BoardLogic import BoardLogic
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Flag import FlagAlreadyClaimedError
from battleline.Identifiers import Identifiers, TroopCard
import itertools


class MockEngine(object):

    def __init__(self):
        self.played_cards = []

    def get_unplayed_cards(self):
        return set(get_all_cards()) - set(self.played_cards)


def get_all_cards():
    return [TroopCard(number, color) for number, color in itertools.product(range(1, 11), Identifiers.COLORS)]


class TestBoardLogic(unittest.TestCase):

    def setUp(self):
        self.logic = FormationLogic()
        self.engine = MockEngine()
        self.boardLogic = BoardLogic(self.engine)
        self.fullList = get_all_cards()

    def addCard(self, flag, player, card):
        self.boardLogic.addCard(flag, player, card)
        self.engine.played_cards.append(
            TroopCard(number=card[0], color=card[1]))
    """test_checkAllFlags_empty

    test if the checkAllFlags function will work on an empty board
    """

    def test_checkAllFlags_empty(self):
        self.boardLogic.checkAllFlags()
        for flag in self.boardLogic.board.flags:
            self.assertEquals(flag.is_claimed(), False)

    def test_check_all_flags_one_side_empty_no_claim(self):
        self.addCard(0, Identifiers.NORTH, TroopCard(1, "blue"))
        self.addCard(0, Identifiers.NORTH, TroopCard(3, "green"))
        self.addCard(0, Identifiers.NORTH, TroopCard(5, "red"))
        self.boardLogic.checkAllFlags()
        self.assertNotEqual(self.boardLogic.board.flags[
                            0].claimed, Identifiers.NORTH)
        self.assertNotEqual(self.boardLogic.board.flags[
                            0].claimed, Identifiers.SOUTH)

    def test_check_all_flags_one_side_empty_north_winner(self):
        for i, colors in enumerate(Identifiers.COLORS):
            if i + 1 != len(Identifiers.COLORS):
                self.addCard(i, Identifiers.NORTH, TroopCard(8, colors))
                self.addCard(i, Identifiers.NORTH, TroopCard(9, colors))
                self.addCard(i, Identifiers.SOUTH, TroopCard(10, colors))
            else:
                self.addCard(i, Identifiers.NORTH, TroopCard(8, colors))
                self.addCard(i, Identifiers.NORTH, TroopCard(9, colors))
                self.addCard(i, Identifiers.NORTH, TroopCard(10, colors))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.board.flags[
                         i].claimed, Identifiers.NORTH)

    def test_check_all_flags_one_side_empty_north_winner_formation_equivalent(self):
        self.addCard(0, Identifiers.NORTH,
                     TroopCard(8, Identifiers.COLORS[0]))
        self.addCard(0, Identifiers.NORTH,
                     TroopCard(9, Identifiers.COLORS[0]))
        self.addCard(0, Identifiers.NORTH,
                     TroopCard(10, Identifiers.COLORS[0]))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.board.flags[
                         0].claimed, Identifiers.NORTH)

    """test_checkAllFlags_FlagContested_basic

    test if the checkAllFlags function will work on a non-empty board
    """

    def test_checkAllFlags_FlagContested_basic(self):
        # flag 1: 10-9-8 vs 1-2-3
        self.addCard(0, Identifiers.NORTH, TroopCard(10, 'blue'))
        self.addCard(0, Identifiers.SOUTH, TroopCard(1, 'blue'))

        self.addCard(0, Identifiers.NORTH, TroopCard(9, 'blue'))
        self.addCard(0, Identifiers.SOUTH, TroopCard(2, 'blue'))

        self.addCard(0, Identifiers.NORTH, TroopCard(8, 'blue'))
        self.boardLogic.checkAllFlags()
        with self.assertRaisesRegexp(FlagAlreadyClaimedError, "south is attempting to place card on already claimed flag."):
            self.addCard(0, Identifiers.SOUTH, TroopCard(3, 'blue'))
        self.assertEqual(self.boardLogic.board.flags[
                         0].claimed, Identifiers.NORTH)

        # flag 2: 10R-9R-8R vs 1-2-3
        self.addCard(1, Identifiers.SOUTH, TroopCard(1, 'red'))
        self.addCard(1, Identifiers.NORTH, TroopCard(10, 'red'))

        self.addCard(1, Identifiers.SOUTH, TroopCard(2, 'red'))
        self.addCard(1, Identifiers.NORTH, TroopCard(9, 'red'))

        self.addCard(1, Identifiers.SOUTH, TroopCard(3, 'red'))
        self.addCard(1, Identifiers.NORTH, TroopCard(8, 'red'))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.board.flags[
                         1].claimed, Identifiers.NORTH)

        # flag 3: 10-9-_ vs 1-2-3 (8 is played on flag 9)
        self.addCard(8, Identifiers.SOUTH, TroopCard(8, 'green'))

        self.addCard(2, Identifiers.NORTH, TroopCard(10, 'green'))
        self.addCard(2, Identifiers.SOUTH, TroopCard(1, 'green'))

        self.addCard(2, Identifiers.NORTH, TroopCard(9, 'green'))
        self.addCard(2, Identifiers.SOUTH, TroopCard(2, 'green'))

        self.addCard(8, Identifiers.NORTH, TroopCard(5, 'blue'))
        self.addCard(2, Identifiers.SOUTH, TroopCard(3, 'green'))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.board.flags[
                         2].claimed, Identifiers.SOUTH)

    """test_checkAllFlags_FlagContested_tied

    test if the checkAllFlags function will work when both formations and values are exactly the same
    """

    def test_checkAllFlags_FlagContested_tied(self):
        # flag 5: 7-6-5(yellow) vs 7-6-5(purple)
        self.addCard(4, Identifiers.NORTH, TroopCard(7, 'yellow'))
        self.addCard(4, Identifiers.SOUTH, TroopCard(7, 'purple'))

        self.addCard(4, Identifiers.NORTH, TroopCard(6, 'yellow'))
        self.addCard(4, Identifiers.SOUTH, TroopCard(6, 'purple'))

        self.addCard(4, Identifiers.NORTH, TroopCard(5, 'yellow'))
        self.addCard(4, Identifiers.SOUTH, TroopCard(5, 'purple'))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.board.flags[
                         4].claimed, Identifiers.NORTH)

        # flag 6: 3-2-1(yellow) vs 3-2-1(purple)
        self.addCard(5, Identifiers.SOUTH, TroopCard(3, 'purple'))
        self.addCard(5, Identifiers.NORTH, TroopCard(3, 'yellow'))

        self.addCard(5, Identifiers.SOUTH, TroopCard(2, 'purple'))
        self.addCard(5, Identifiers.NORTH, TroopCard(2, 'yellow'))

        self.addCard(5, Identifiers.SOUTH, TroopCard(1, 'purple'))
        self.addCard(5, Identifiers.NORTH, TroopCard(1, 'yellow'))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.board.flags[
                         5].claimed, Identifiers.SOUTH)

    def test_flag_is_playable(self):
        self.assertTrue(self.boardLogic.is_flag_playable(0, Identifiers.NORTH))
        self.assertTrue(self.boardLogic.is_flag_playable(0, Identifiers.SOUTH))

        self.boardLogic.board.get_flag(1).sides[Identifiers.NORTH] = [TroopCard(
            1, "color1"), TroopCard(2, "color1"), TroopCard(3, "color1")]
        self.boardLogic.checkAllFlags()
        self.assertFalse(
            self.boardLogic.is_flag_playable(0, Identifiers.NORTH))
        self.assertTrue(self.boardLogic.is_flag_playable(0, Identifiers.SOUTH))

    def test_check_breakthrough(self):
        # 3 adjacent flags.
        for flag, colorId in zip([1, 2, 3], range(0, 3)):
            for cardValue in range(8, 11):
                self.boardLogic.checkAllFlags()
                self.assertIsNone(self.boardLogic.winner)
                self.boardLogic.addCard(
                    flag, Identifiers.NORTH, (cardValue, Identifiers.COLORS[colorId]))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.winner, Identifiers.NORTH)

    def test_check_envelopment(self):
        # 5 flags.
        for flag, colorId in zip([1, 2, 4, 5, 7], range(0, 5)):
            for cardValue in range(8, 11):
                self.boardLogic.checkAllFlags()
                self.assertIsNone(self.boardLogic.winner)
                self.boardLogic.addCard(
                    flag, Identifiers.NORTH, (cardValue, Identifiers.COLORS[colorId]))
        self.boardLogic.checkAllFlags()
        self.assertEqual(self.boardLogic.winner, Identifiers.NORTH)
