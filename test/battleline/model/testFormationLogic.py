import unittest
from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Formation import FormationInvalidError
from battleline.Identifiers import Identifiers, TroopCard
from itertools import product


def make_troop_card_list(color_number_tuples):
    return [TroopCard(number, color) for color, number in color_number_tuples]


def get_base_cards():
    return make_troop_card_list([("color1", 10), ("color1", 7),
                                 ("color1", 6), ("color2", 10),
                                 ("color1", 3), ("color3", 5),
                                 ("color1", 2), ("color1", 1),
                                 ("color2", 1), ("color3", 1)])


class TestFormationLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.logic = FormationLogic()
        self.fullList = [(number, color)
                         for color, number in product(Identifiers.COLORS, range(1, 11))]

    def assert_best_formation(self, expected_cards, given_cards, unplayed_cards):
        self.assertEquals(make_troop_card_list(expected_cards),
                          sorted(self.logic.get_best_formation(make_troop_card_list(given_cards),
                                                        unplayed_cards), key=lambda x: (x[1], x[0]), reverse=True))

    def test_get_best_formation_wedge(self):
        unplayed_cards = get_base_cards()
        self.assert_best_formation([("color1", 10), ("color1", 9), ("color1", 8)],
                                   [("color1", 10), ("color1", 9), ("color1", 8)], unplayed_cards)
        self.assert_best_formation([("color1", 10), ("color1", 9), ("color1", 8)],
                                   [("color1", 9), ("color1", 8)], unplayed_cards)

        del unplayed_cards[0]
        self.assert_best_formation([("color1", 9), ("color1", 8), ("color1", 7)],
                                   [("color1", 9), ("color1", 8)], unplayed_cards)
        self.assert_best_formation([("color1", 8), ("color1", 7), ("color1", 6)],
                                   [("color1", 8)], unplayed_cards)
        self.assert_best_formation([("color1", 3), ("color1", 2), ("color1", 1)],
                                   [], unplayed_cards)

    def test_get_best_formation_phalanax(self):
        unplayed_cards = get_base_cards()
        self.assert_best_formation([("color3", 7), ("color2", 7), ("color1", 7)],
                                   [("color3", 7), ("color2", 7)], unplayed_cards)
        self.assert_best_formation([("color3", 10), ("color2", 10), ("color1", 10)],
                                   [("color3", 10)], unplayed_cards)

        unplayed_cards = [c for c in unplayed_cards if c.number != 2]
        self.assert_best_formation([("color3", 1), ("color2", 1), ("color1", 1)],
                                   [], unplayed_cards)

    def test_get_best_formation_battalion(self):
        unplayed_cards = get_base_cards()
        self.assert_best_formation([("color2", 10), ("color2", 8), ("color2", 7)],
                                   [("color2", 8), ("color2", 7)], unplayed_cards)
        self.assert_best_formation([("color3", 5), ("color3", 3), ("color3", 1)],
                                   [("color3", 3)], unplayed_cards)

        unplayed_cards = [c for c in unplayed_cards if c.number != 1]
        self.assert_best_formation([("color1", 10), ("color1", 7), ("color1", 6)],
                                   [], unplayed_cards)

    def test_get_best_formation_skirmish(self):
        unplayed_cards = get_base_cards()

        self.assert_best_formation([("color4", 9), ("color4", 8), ("color1", 10), ],
                                   [("color4", 9), ("color4", 8)], unplayed_cards)
        self.assert_best_formation([("color4", 8), ("color1", 7), ("color1", 6)],
                                   [("color4", 8)], unplayed_cards)

        unplayed_cards = make_troop_card_list([("color1", 10), ("color4", 9), ("color4", 8),
                                               ("color2", 3), ("color2", 4), ("color3", 5)])
        self.assert_best_formation([("color4", 9), ("color4", 8), ("color1", 10), ],
                                   [], unplayed_cards)

    def test_get_best_formation_host(self):
        unplayed_cards = make_troop_card_list([("color1", 10), ("color4", 8),
                                               ("color2", 3),  ("color3", 5)])
        self.assert_best_formation([("color5", 10), ("color5", 8), ("color1", 10)],
                                   [("color5", 10), ("color5", 8)], unplayed_cards)
        self.assert_best_formation([("color5", 10), ("color4", 8), ("color1", 10)],
                                   [("color5", 10)], unplayed_cards)
        self.assert_best_formation([("color4", 8), ("color3", 5), ("color1", 10)],
                                   [], unplayed_cards)
