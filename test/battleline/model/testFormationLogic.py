import unittest
from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Formation import FormationInvalidError
from battleline.Identifiers import Identifiers, TroopCard
from itertools import product

COLORS = Identifiers.COLORS


def make_troop_card_list( color_number_tuples):
    return [TroopCard(number,color) for color,number in color_number_tuples]

def get_base_cards():
    return make_troop_card_list([("color1", 10), ("color1", 7), ("color1", 6), ("color2", 10),
                                       ("color1", 3), ("color3", 5), ("color1",2), ("color1", 1),
                                       ("color2", 1), ("color3", 1)])


class TestFormationLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.logic = FormationLogic()
        self.fullList = [(number, color)
                         for color, number in product(COLORS, range(1, 11))]

    def assert_best_formation(self,expected_cards, given_cards, unplayed_cards):
        self.assertEquals(make_troop_card_list(expected_cards),
                           self.logic.get_best_formation(make_troop_card_list(given_cards),
                          unplayed_cards))

    def test_get_best_formation_wedge(self):
        unplayed_cards = get_base_cards()
        self.assert_best_formation([("color1", 10), ("color1", 9), ("color1", 8)], [("color1", 10), ("color1", 9), ("color1", 8)], unplayed_cards)

        self.assertEquals([TroopCard(color="color1", number=10), TroopCard(color="color1", number=9), TroopCard(color="color1", number=8)],
                          self.logic.get_best_formation([TroopCard(color="color1", number=9), TroopCard(color="color1", number=8)], unplayed_cards))

        del unplayed_cards[0]

        self.assertEquals([TroopCard(color="color1", number=9), TroopCard(color="color1", number=8), TroopCard(color="color1", number=7)],
                          self.logic.get_best_formation([TroopCard(color="color1", number=9), TroopCard(color="color1", number=8)], unplayed_cards))

        self.assertEquals([TroopCard(color="color1", number=8), TroopCard(color="color1", number=7), TroopCard(color="color1", number=6)],
                          self.logic.get_best_formation([TroopCard(color="color1", number=8)], unplayed_cards))

        self.assertEquals([TroopCard(color="color1", number=3), TroopCard(color="color1", number=2), TroopCard(color="color1", number=1)],
                          self.logic.get_best_formation([], unplayed_cards))

    def test_get_best_formation_phalanax(self):
        unplayed_cards = get_base_cards()

        self.assertEquals([TroopCard(color="color3", number=7), TroopCard(color="color2", number=7), TroopCard(color="color1", number=7)],
                          self.logic.get_best_formation([TroopCard(color="color2", number=7), TroopCard(color="color3", number=7)], unplayed_cards))

        self.assertEquals([TroopCard(color="color3", number=10), TroopCard(color="color2", number=10), TroopCard(color="color1", number=10)],
                          self.logic.get_best_formation([TroopCard(color="color3", number=10)], unplayed_cards))

        unplayed_cards = [c for c in unplayed_cards if c.number != 2]
        self.assertEquals([TroopCard(color="color3", number=1), TroopCard(color="color2", number=1), TroopCard(color="color1", number=1)],
                          self.logic.get_best_formation([], unplayed_cards))

    def test_get_best_formation_battalion(self):
        unplayed_cards = get_base_cards()

        self.assertEquals([TroopCard(color="color2", number=10), TroopCard(color="color2", number=8), TroopCard(color="color2", number=7)],
                          self.logic.get_best_formation([TroopCard(color="color2", number=8), TroopCard(color="color2", number=7)], unplayed_cards))

        self.assertEquals([TroopCard(color="color3", number=5), TroopCard(color="color3", number=3), TroopCard(color="color3", number=1)],
                          self.logic.get_best_formation([TroopCard(color="color3", number=3)], unplayed_cards))

        unplayed_cards = [c for c in unplayed_cards if c.number != 1]
        self.assertEquals([TroopCard(color="color1", number=10), TroopCard(color="color1", number=7), TroopCard(color="color1", number=6)],
                          self.logic.get_best_formation([], unplayed_cards))

    """test_greatestPossibleFormation

    test if the greatestPossibleFormation function will give the correct best formation with all available cards
    """

    def test_greatestPossibleFormation_empty(self):
        self.assertEquals(self.logic.greatestPossibleFormation([], []), [
                          (8, COLORS[0]), (9, COLORS[0]), (10, COLORS[0])])
        self.assertEquals(self.logic.greatestPossibleFormation(
            [(1, COLORS[0]), (2, COLORS[0]), (3, COLORS[0])], []), [(1, COLORS[0]), (2, COLORS[0]), (3, COLORS[0])])

    def test_is_equivalent_in_strength_true(self):
        formation1 = [(1, COLORS[0]), (2, COLORS[0]), (3, COLORS[0])]
        formation2 = [(1, COLORS[1]), (2, COLORS[1]), (3, COLORS[1])]
        self.assertTrue(self.logic.is_equivalent_in_strength(
            formation1, formation2))

    def test_is_equivalent_in_strength_false(self):
        formation1 = [(1, COLORS[0]), (2, COLORS[0]), (3, COLORS[0])]
        formation2 = [(2, COLORS[1]), (3, COLORS[1]), (4, COLORS[1])]
        self.assertFalse(self.logic.is_equivalent_in_strength(
            formation1, formation2))

    """test_creationFunctions_empty

    test if the create function will give the correct formation
    """

    def test_creationFunctions_empty(self):
        self.assertEquals(self.logic.createStraightFlush(
            [], []), [(8, COLORS[0]), (9, COLORS[0]), (10, COLORS[0])])
        self.assertEquals(self.logic.createThreeOfAKind(
            [], []), [(10, COLORS[0]), (10, COLORS[1]), (10, COLORS[2])])
        self.assertEquals(self.logic.createFlush(
            [], []), [(10, COLORS[0]), (9, COLORS[0]), (8, COLORS[0])])
        self.assertEquals(self.logic.createStraight(
            [], []), [(10, COLORS[0]), (9, COLORS[0]), (8, COLORS[0])])
        self.assertEquals(self.logic.createHost(
            [], []), [(10, COLORS[0]), (10, COLORS[1]), (10, COLORS[2])])

    """test_creationFunctions_without10blue

    test if (10,COLORS[0]) card is used, the create function will give the correct formation
    """

    def test_creationFunctions_without10blue(self):
        playedCardList = [(10, COLORS[0])]
        self.assertEquals(self.logic.createStraightFlush([], playedCardList), [
                          (8, COLORS[1]), (9, COLORS[1]), (10, COLORS[1])])
        self.assertEquals(self.logic.createThreeOfAKind(
            [], playedCardList), [(10, COLORS[1]), (10, COLORS[2]), (10, COLORS[3])])
        self.assertEquals(self.logic.createFlush(
            [], playedCardList), [(9, COLORS[0]), (8, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createStraight(
            [], playedCardList), [(10, COLORS[1]), (9, COLORS[0]), (8, COLORS[0])])
        self.assertEquals(self.logic.createHost(
            [], playedCardList), [(10, COLORS[1]), (10, COLORS[2]), (10, COLORS[3])])

    """test_creationFunctions_oneCard

    test if the create function is passed 1 cards, that it will give the correct formation
    """

    def test_creationFunctions_oneCard(self):
        playedCardList = [(5, COLORS[0])]
        card5Blue = (5, COLORS[0])
        self.assertEquals(self.logic.createStraightFlush([card5Blue], playedCardList), [
                          (5, COLORS[0]), (6, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue], playedCardList), [
                          (5, COLORS[0]), (5, COLORS[1]), (5, COLORS[2])])
        self.assertEquals(self.logic.createFlush([card5Blue], playedCardList), [
                          (5, COLORS[0]), (10, COLORS[0]), (9, COLORS[0])])
        self.assertEquals(self.logic.createStraight([card5Blue], playedCardList), [
                          (5, COLORS[0]), (7, COLORS[0]), (6, COLORS[0])])
        self.assertEquals(self.logic.createHost([card5Blue], playedCardList), [
                          (5, COLORS[0]), (10, COLORS[0]), (10, COLORS[1])])

    """test_creationFunctions_twoCards

    test if the create function is passed 2 cards, that it will give the correct formation
    """

    def test_creationFunctions_twoCards(self):
        card5Blue = (5, COLORS[0])
        card5Red = (5, COLORS[1])
        card6Blue = (6, COLORS[0])
        playedCardList = [card5Blue, card6Blue, card5Red]
        self.assertEquals(self.logic.createStraightFlush([card5Blue, card6Blue], playedCardList), [
                          (5, COLORS[0]), (6, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue, card5Red], playedCardList), [
                          (5, COLORS[0]), (5, COLORS[1]), (5, COLORS[2])])
        self.assertEquals(self.logic.createFlush([card5Blue, card6Blue], playedCardList), [
                          (5, COLORS[0]), (6, COLORS[0]), (10, COLORS[0])])
        self.assertEquals(self.logic.createStraight([card5Blue, card6Blue], playedCardList), [
                          (5, COLORS[0]), (6, COLORS[0]), (7, COLORS[0])])
        self.assertEquals(self.logic.createHost([card5Blue, card6Blue], playedCardList), [
                          (5, COLORS[0]), (6, COLORS[0]), (10, COLORS[0])])

    """test_creationFunctions_invalids_empty

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_empty(self):
        playedCardList = self.fullList
        self.assertEquals(
            self.logic.createStraightFlush([], playedCardList), [])
        self.assertEquals(
            self.logic.createThreeOfAKind([], playedCardList), [])
        self.assertEquals(self.logic.createFlush([], playedCardList), [])
        self.assertEquals(self.logic.createStraight([], playedCardList), [])
        self.assertEquals(self.logic.createHost([], playedCardList), [])

    """test_creationFunctions_invalids_oneCard

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_oneCard(self):
        card5Blue = (5, COLORS[0])
        playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush(
            [card5Blue], playedCardList), [])
        self.assertEquals(self.logic.createThreeOfAKind(
            [card5Blue], playedCardList), [])
        self.assertEquals(self.logic.createFlush(
            [card5Blue], playedCardList), [])
        self.assertEquals(self.logic.createStraight(
            [card5Blue], playedCardList), [])
        self.assertEquals(self.logic.createHost(
            [card5Blue], playedCardList), [])

    """test_creationFunctions_invalids_twoCards

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_twoCards(self):
        card5Blue = (5, COLORS[0])
        card5Red = (5, COLORS[1])
        card6Blue = (6, COLORS[0])
        playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush(
            [card5Blue, card6Blue], playedCardList), [])
        self.assertEquals(self.logic.createThreeOfAKind(
            [card5Blue, card5Red], playedCardList), [])
        self.assertEquals(self.logic.createFlush(
            [card5Blue, card6Blue], playedCardList), [])
        self.assertEquals(self.logic.createStraight(
            [card5Blue, card6Blue], playedCardList), [])
        self.assertEquals(self.logic.createHost(
            [card5Blue, card6Blue], playedCardList), [])
