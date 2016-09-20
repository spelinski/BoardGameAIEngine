import unittest
from dominion import Identifiers
from dominion.CardInfo import *
class TestCardInfo(unittest.TestCase):

    def test_can_check_if_victory_card(self):
        self.assertTrue(is_victory_card(Identifiers.ESTATE))
        self.assertTrue(is_victory_card(Identifiers.DUCHY))
        self.assertTrue(is_victory_card(Identifiers.PROVINCE))
        self.assertFalse(is_victory_card(Identifiers.CURSE))

    def test_can_check_if_treasure_card(self):
        self.assertTrue(is_treasure(Identifiers.COPPER))
        self.assertTrue(is_treasure(Identifiers.SILVER))
        self.assertTrue(is_treasure(Identifiers.GOLD))
        self.assertFalse(is_treasure(Identifiers.CURSE))

    def test_can_check_if_is_action_card(self):
        self.assertTrue(is_action_card(Identifiers.CELLAR))
        self.assertTrue(is_action_card(Identifiers.MOAT))
        self.assertTrue(is_action_card(Identifiers.VILLAGE))
        self.assertTrue(is_action_card(Identifiers.WOODCUTTER))
        self.assertTrue(is_action_card(Identifiers.WORKSHOP))
        self.assertTrue(is_action_card(Identifiers.MILITIA))
        self.assertTrue(is_action_card(Identifiers.REMODEL))
        self.assertTrue(is_action_card(Identifiers.SMITHY))
        self.assertTrue(is_action_card(Identifiers.MARKET))
        self.assertTrue(is_action_card(Identifiers.MINE))
        self.assertFalse(is_action_card(Identifiers.CURSE))
        self.assertFalse(is_action_card(Identifiers.COPPER))
        self.assertFalse(is_action_card(Identifiers.ESTATE))
        self.assertFalse(is_action_card(Identifiers.SILVER))
        self.assertFalse(is_action_card(Identifiers.DUCHY))
        self.assertFalse(is_action_card(Identifiers.GOLD))
        self.assertFalse(is_action_card(Identifiers.PROVINCE))

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

    def test_cost_throws_exception_if_invalid_card(self):
        with self.assertRaises(ValueError):
            get_cost("Bad Name")

    def test_can_get_extra_actions(self):
        self.assertEquals(2, get_extra_actions(Identifiers.VILLAGE))
        self.assertEquals(1, get_extra_actions(Identifiers.MARKET))
        self.assertEquals(0, get_extra_actions(Identifiers.MINE))

    def test_can_get_extra_buys(self):
        self.assertEquals(1, get_extra_buys(Identifiers.MARKET))
        self.assertEquals(1, get_extra_buys(Identifiers.WOODCUTTER))
        self.assertEquals(0, get_extra_buys(Identifiers.VILLAGE))

    def test_can_get_extra_cards(self):
        self.assertEquals(0, get_extra_cards(Identifiers.CELLAR))
        self.assertEquals(1, get_extra_cards(Identifiers.VILLAGE))
        self.assertEquals(1, get_extra_cards(Identifiers.MARKET))
        self.assertEquals(3, get_extra_cards(Identifiers.SMITHY))
        self.assertEquals(2, get_extra_cards(Identifiers.MOAT))
        self.assertEquals(0, get_extra_cards(Identifiers.WOODCUTTER))

    def test_can_get_extra_treasure(self):
        self.assertEquals(1, get_extra_treasure(Identifiers.MARKET))
        self.assertEquals(2, get_extra_treasure(Identifiers.MILITIA))
        self.assertEquals(2, get_extra_treasure(Identifiers.WOODCUTTER))
        self.assertEquals(0, get_extra_treasure(Identifiers.REMODEL))
