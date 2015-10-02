import unittest
from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Formation import FormationInvalidError
from battleline.Identifiers import Identifiers
from itertools import product

COLORS = Identifiers.COLORS

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.logic = FormationLogic()
        self.fullList = [(number, color) for color, number in product(COLORS, range(1, 11))]


    """test_checkAllFlags_empty

    test if the checkAllFlags function will work on an empty board
    """

    def test_checkAllFlags_empty(self):
        self.logic.checkAllFlags(self.board)
        for flag in self.board.flags:
	    self.assertEquals(flag.is_claimed(),False)

    """test_checkAllFlags_FlagContested

    test if the checkAllFlags function will work on an empty board
    """

    def test_checkAllFlags_FlagContested(self):
        # flag 1: 10-9-8 vs 1-2-3
        self.board.flags[0].add_card(
            self.board.flags[0].PLAYER_NORTH, (10, COLORS[0]))
        self.board.flags[0].add_card(
            self.board.flags[0].PLAYER_NORTH, (9, COLORS[0]))
        self.board.flags[0].add_card(
            self.board.flags[0].PLAYER_NORTH, (8, COLORS[0]))

        self.board.flags[0].add_card(
            self.board.flags[0].PLAYER_SOUTH, (1, COLORS[0]))
        self.board.flags[0].add_card(
            self.board.flags[0].PLAYER_SOUTH, (2, COLORS[0]))
        self.board.flags[0].add_card(
            self.board.flags[0].PLAYER_SOUTH, (3, COLORS[0]))

        # flag 2: 10R-9R-8R vs 1-2-_
        self.board.flags[1].add_card(
            self.board.flags[1].PLAYER_NORTH, (10, COLORS[1]))
        self.board.flags[1].add_card(
            self.board.flags[1].PLAYER_NORTH, (9, COLORS[1]))
        self.board.flags[1].add_card(
            self.board.flags[1].PLAYER_NORTH, (8, COLORS[1]))

        self.board.flags[1].add_card(
            self.board.flags[1].PLAYER_SOUTH, (1, COLORS[1]))
        self.board.flags[1].add_card(
            self.board.flags[1].PLAYER_SOUTH, (2, COLORS[1]))

        # flag 3: 10-9-_ vs 1-2-3 (8 is played on flag 4)
        self.board.flags[2].add_card(
            self.board.flags[1].PLAYER_NORTH, (10, COLORS[2]))
        self.board.flags[2].add_card(
            self.board.flags[1].PLAYER_NORTH, (9, COLORS[2]))

        self.board.flags[2].add_card(
            self.board.flags[1].PLAYER_SOUTH, (1, COLORS[2]))
        self.board.flags[2].add_card(
            self.board.flags[1].PLAYER_SOUTH, (2, COLORS[2]))
        self.board.flags[2].add_card(
            self.board.flags[1].PLAYER_SOUTH, (3, COLORS[2]))
        self.board.flags[3].add_card(
            self.board.flags[1].PLAYER_SOUTH, (8, COLORS[2]))
        self.logic.checkAllFlags(self.board)

        # right now I just check if the flag has been claimed, I need to check
        # if it has been claimed by the right person
        expectedResults = [True, True, True, False,
                           False, False, False, False, False]
        actualResults = [False, False, False, False,
                         False, False, False, False, False]
        for i, flag in enumerate(self.board.flags):
            actualResults[i] = flag.is_claimed()
        self.assertEquals(actualResults, expectedResults)

    """test_setPlayedCardList_empty

    test if the setPlayedCardList function will parse an empty board
    """

    def test_setPlayedCardList_empty(self):
        self.logic.setPlayedCardList(self.board)
        self.assertEquals(self.logic.playedCardList, [])

    """test_greatestPossibleFormation

    test if the greatestPossibleFormation function will give the correct best formation with all available cards
    """

    def test_greatestPossibleFormation_empty(self):
        self.assertEquals(self.logic.greatestPossibleFormation([]), [
                          (8, COLORS[0]), (9, COLORS[0]), (10, COLORS[0])])
        self.assertEquals(self.logic.greatestPossibleFormation(
            [(1, COLORS[0]), (2, COLORS[0]), (3, COLORS[0])]), [(1, COLORS[0]), (2, COLORS[0]), (3, COLORS[0])])
    """test_creationFunctions_empty

    test if the create function will give the correct formation
    """

    def test_creationFunctions_empty(self):
        self.assertEquals(self.logic.createStraightFlush(
            []), [(8, COLORS[0]), (9, COLORS[0]), (10, COLORS[0])])
        self.assertEquals(self.logic.createThreeOfAKind(
            []), [(10, COLORS[0]), (10, COLORS[1]), (10, COLORS[2])])
        self.assertEquals(self.logic.createFlush(
            []), [(10, COLORS[0]), (9, COLORS[0]), (8, COLORS[0])])
        self.assertEquals(self.logic.createStraight(
            []), [(10, COLORS[0]), (9, COLORS[0]), (8, COLORS[0])])
        self.assertEquals(self.logic.createHost(
            []), [(10, COLORS[0]), (10, COLORS[1]), (10, COLORS[2])])

    """test_creationFunctions_without10blue

    test if (10,COLORS[0]) card is used, the create function will give the correct formation
    """

    def test_creationFunctions_without10blue(self):
        self.logic.playedCardList = [(10, COLORS[0])]
        self.assertEquals(self.logic.createStraightFlush([]), [
                          (8, COLORS[1]), (9, COLORS[1]), (10, COLORS[1])])
        self.assertEquals(self.logic.createThreeOfAKind(
            []), [(10, COLORS[1]), (10, COLORS[2]), (10, COLORS[3])])
        self.assertEquals(self.logic.createFlush(
            []), [(9, COLORS[0]), (8, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createStraight(
            []), [(10, COLORS[1]), (9, COLORS[0]), (8, COLORS[0])])
        self.assertEquals(self.logic.createHost(
            []), [(10, COLORS[1]), (10, COLORS[2]), (10, COLORS[3])])

    """test_creationFunctions_oneCard

    test if the create function is passed 1 cards, that it will give the correct formation
    """

    def test_creationFunctions_oneCard(self):
        self.logic.playedCardList = [(5, COLORS[0])]
        card5Blue = (5, COLORS[0])
        self.assertEquals(self.logic.createStraightFlush([card5Blue]), [
                          (5, COLORS[0]), (6, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue]), [
                          (5, COLORS[0]), (5, COLORS[1]), (5, COLORS[2])])
        self.assertEquals(self.logic.createFlush([card5Blue]), [
                          (5, COLORS[0]), (10, COLORS[0]), (9, COLORS[0])])
        self.assertEquals(self.logic.createStraight([card5Blue]), [
                          (5, COLORS[0]), (7, COLORS[0]), (6, COLORS[0])])
        self.assertEquals(self.logic.createHost([card5Blue]), [
                          (5, COLORS[0]), (10, COLORS[0]), (10, COLORS[1])])

    """test_creationFunctions_twoCards

    test if the create function is passed 2 cards, that it will give the correct formation
    """

    def test_creationFunctions_twoCards(self):
        card5Blue = (5, COLORS[0])
        card5Red = (5, COLORS[1])
        card6Blue = (6, COLORS[0])
        self.logic.playedCardList = [card5Blue, card6Blue, card5Red]
        self.assertEquals(self.logic.createStraightFlush([card5Blue, card6Blue]), [
                          (5, COLORS[0]), (6, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue, card5Red]), [
                          (5, COLORS[0]), (5, COLORS[1]), (5, COLORS[2])])
        self.assertEquals(self.logic.createFlush([card5Blue, card6Blue]), [
                          (5, COLORS[0]), (6, COLORS[0]), (10, COLORS[0])])
        self.assertEquals(self.logic.createStraight([card5Blue, card6Blue]), [
                          (5, COLORS[0]), (6, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createHost([card5Blue, card6Blue]), [
                          (5, COLORS[0]), (6, COLORS[0]), (10, COLORS[0])])

    """test_creationFunctions_invalids_empty

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_empty(self):
        self.logic.playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([]), [])
        self.assertEquals(self.logic.createThreeOfAKind([]), [])
        self.assertEquals(self.logic.createFlush([]), [])
        self.assertEquals(self.logic.createStraight([]), [])
        self.assertEquals(self.logic.createHost([]), [])

    """test_creationFunctions_invalids_oneCard

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_oneCard(self):
        card5Blue = (5, COLORS[0])
        self.logic.playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([card5Blue]), [])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue]), [])
        self.assertEquals(self.logic.createFlush([card5Blue]), [])
        self.assertEquals(self.logic.createStraight([card5Blue]), [])
        self.assertEquals(self.logic.createHost([card5Blue]), [])

    """test_creationFunctions_invalids_twoCards

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_twoCards(self):
        card5Blue = (5, COLORS[0])
        card5Red = (5, COLORS[1])
        card6Blue = (6, COLORS[0])
        self.logic.playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush(
            [card5Blue, card6Blue]), [])
        self.assertEquals(self.logic.createThreeOfAKind(
            [card5Blue, card5Red]), [])
        self.assertEquals(self.logic.createFlush([card5Blue, card6Blue]), [])
        self.assertEquals(self.logic.createStraight(
            [card5Blue, card6Blue]), [])
        self.assertEquals(self.logic.createHost([card5Blue, card6Blue]), [])
