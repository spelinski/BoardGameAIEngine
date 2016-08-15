import unittest
from dominion.model.Supply import *
from dominion import Identifiers


class TestSupply(unittest.TestCase):

    def check_first_set_kingdom_and_treasure_cards(self, supply):
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.CELLAR))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.MARKET))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.MILITIA))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.MINE))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.MOAT))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.REMODEL))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.SMITHY))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.VILLAGE))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.WOODCUTTER))
        self.assertEquals(10, supply.get_number_of_cards(Identifiers.WORKSHOP))

        self.assertEquals(60, supply.get_number_of_cards(Identifiers.COPPER))
        self.assertEquals(40, supply.get_number_of_cards(Identifiers.SILVER))
        self.assertEquals(30, supply.get_number_of_cards(Identifiers.GOLD))

    def test_first_set_two_players(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(14, supply.get_number_of_cards(Identifiers.ESTATE))
        self.assertEquals(8, supply.get_number_of_cards(Identifiers.DUCHY))
        self.assertEquals(8, supply.get_number_of_cards(Identifiers.PROVINCE))

        self.assertEquals(10, supply.get_number_of_cards(Identifiers.CURSE))

    def test_first_set_three_players(self):
        supply = Supply(3, Identifiers.FIRST_GAME)
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(21, supply.get_number_of_cards(Identifiers.ESTATE))
        self.assertEquals(12, supply.get_number_of_cards(Identifiers.DUCHY))
        self.assertEquals(12, supply.get_number_of_cards(Identifiers.PROVINCE))

        self.assertEquals(20, supply.get_number_of_cards(Identifiers.CURSE))

    def test_first_set_four_players(self):
        supply = Supply(4, Identifiers.FIRST_GAME)
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(24, supply.get_number_of_cards(Identifiers.ESTATE))
        self.assertEquals(12, supply.get_number_of_cards(Identifiers.DUCHY))
        self.assertEquals(12, supply.get_number_of_cards(Identifiers.PROVINCE))

        self.assertEquals(30, supply.get_number_of_cards(Identifiers.CURSE))

    def test_take_card_decreases_supply_appropriately(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        supply.take(Identifiers.PROVINCE)
        self.assertEquals(7, supply.get_number_of_cards(Identifiers.PROVINCE))

    def test_cant_take_card_not_in_supply(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        with self.assertRaises(CardNotInSupplyException):
            supply.take(Identifiers.FEAST)

    def test_cant_take_card_not_if_pile_is_empty(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        for _ in range(8):
            supply.take(Identifiers.DUCHY)
        with self.assertRaises(PileEmptyException):
            supply.take(Identifiers.DUCHY)

    def test_no_piiles_are_empty_to_start(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        self.assertEquals(0, supply.get_number_of_empty_piles())

    def test_can_empty_piles(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        for _ in range(10):
            supply.take(Identifiers.MOAT)
            supply.take(Identifiers.REMODEL)
            supply.take(Identifiers.MARKET)
        self.assertEquals(3, supply.get_number_of_empty_piles())
