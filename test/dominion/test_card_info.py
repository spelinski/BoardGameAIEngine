import unittest
from dominion import Identifiers
from dominion.CardInfo import *
class TestCardInfo(unittest.TestCase):

    def test_can_check_if_victory_card(self):
        self.assertTrue(is_victory_card(Identifiers.ESTATE))
        self.assertTrue(is_victory_card(Identifiers.DUCHY))
        self.assertTrue(is_victory_card(Identifiers.PROVINCE))
        self.assertFalse(is_victory_card(Identifiers.CURSE))

    def test_can_victory_points(self):
        self.assertEquals(1, get_victory_points(Identifiers.ESTATE))
        self.assertEquals(3, get_victory_points(Identifiers.DUCHY))
        self.assertEquals(6, get_victory_points(Identifiers.PROVINCE))
        self.assertEquals(-1, get_victory_points(Identifiers.CURSE))
        self.assertEquals(0, get_victory_points(Identifiers.COPPER))

    def test_can_get_worth(self):
        self.assertEquals(1, get_worth(Identifiers.COPPER))
        self.assertEquals(2, get_worth(Identifiers.SILVER))
        self.assertEquals(3, get_worth(Identifiers.GOLD))
        self.assertEquals(0, get_worth(Identifiers.MOAT))

    def test_can_get_cost(self):
        self.assertEquals(0, get_cost(Identifiers.CURSE))
        self.assertEquals(0, get_cost(Identifiers.COPPER))
        self.assertEquals(2, get_cost(Identifiers.CELLAR))
        self.assertEquals(2, get_cost(Identifiers.ESTATE))
        self.assertEquals(2, get_cost(Identifiers.MOAT))
        self.assertEquals(3, get_cost(Identifiers.SILVER))
        self.assertEquals(3, get_cost(Identifiers.VILLAGE))
        self.assertEquals(3, get_cost(Identifiers.WOODCUTTER))
        self.assertEquals(3, get_cost(Identifiers.WORKSHOP))
        self.assertEquals(4, get_cost(Identifiers.MILITIA))
        self.assertEquals(4, get_cost(Identifiers.REMODEL))
        self.assertEquals(4, get_cost(Identifiers.SMITHY))
        self.assertEquals(5, get_cost(Identifiers.MARKET))
        self.assertEquals(5, get_cost(Identifiers.MINE))
        self.assertEquals(5, get_cost(Identifiers.DUCHY))
        self.assertEquals(6, get_cost(Identifiers.GOLD))
        self.assertEquals(8, get_cost(Identifiers.PROVINCE))
