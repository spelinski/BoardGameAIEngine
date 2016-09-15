import unittest
from dominion.model.Supply import *
from dominion.Identifiers import *


class TestSupply(unittest.TestCase):

    def check_first_set_kingdom_and_treasure_cards(self, supply):
        self.assertEquals(10, supply.get_number_of_cards(CELLAR))
        self.assertEquals(10, supply.get_number_of_cards(MARKET))
        self.assertEquals(10, supply.get_number_of_cards(MILITIA))
        self.assertEquals(10, supply.get_number_of_cards(MINE))
        self.assertEquals(10, supply.get_number_of_cards(MOAT))
        self.assertEquals(10, supply.get_number_of_cards(REMODEL))
        self.assertEquals(10, supply.get_number_of_cards(SMITHY))
        self.assertEquals(10, supply.get_number_of_cards(VILLAGE))
        self.assertEquals(10, supply.get_number_of_cards(WOODCUTTER))
        self.assertEquals(10, supply.get_number_of_cards(WORKSHOP))

        self.assertEquals(60, supply.get_number_of_cards(COPPER))
        self.assertEquals(40, supply.get_number_of_cards(SILVER))
        self.assertEquals(30, supply.get_number_of_cards(GOLD))

    def test_first_set_two_players(self):
        supply = Supply(2, FIRST_GAME)
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(14, supply.get_number_of_cards(ESTATE))
        self.assertEquals(8, supply.get_number_of_cards(DUCHY))
        self.assertEquals(8, supply.get_number_of_cards(PROVINCE))

        self.assertEquals(10, supply.get_number_of_cards(CURSE))

    def test_first_set_three_players(self):
        supply = Supply(3, FIRST_GAME)
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(21, supply.get_number_of_cards(ESTATE))
        self.assertEquals(12, supply.get_number_of_cards(DUCHY))
        self.assertEquals(12, supply.get_number_of_cards(PROVINCE))

        self.assertEquals(20, supply.get_number_of_cards(CURSE))

    def test_first_set_four_players(self):
        supply = Supply(4, FIRST_GAME)
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(24, supply.get_number_of_cards(ESTATE))
        self.assertEquals(12, supply.get_number_of_cards(DUCHY))
        self.assertEquals(12, supply.get_number_of_cards(PROVINCE))

        self.assertEquals(30, supply.get_number_of_cards(CURSE))

    def test_take_card_decreases_supply_appropriately(self):
        supply = Supply(2, FIRST_GAME)
        supply.take(PROVINCE)
        self.assertEquals(7, supply.get_number_of_cards(PROVINCE))

    def test_cant_take_card_not_in_supply(self):
        supply = Supply(2, FIRST_GAME)
        with self.assertRaisesRegexp(CardNotInSupplyException, "feast is not in the supply"):
            supply.take(FEAST)

    def test_cant_take_card_not_if_pile_is_empty(self):
        supply = Supply(2, FIRST_GAME)
        for _ in range(8):
            supply.take(DUCHY)
        with self.assertRaisesRegexp(PileEmptyException, "duchy's pile is empty"):
            supply.take(DUCHY)

    def test_no_piles_are_empty_to_start(self):
        supply = Supply(2, FIRST_GAME)
        self.assertEquals(0, supply.get_number_of_empty_piles())

    def test_can_get_empty_piles(self):
        supply = Supply(2, FIRST_GAME)
        for _ in range(10):
            supply.take(MOAT)
            supply.take(REMODEL)
            supply.take(MARKET)
        self.assertEquals(3, supply.get_number_of_empty_piles())

    def test_filter_can_get_a_copy(self):
        supply = Supply(2, FIRST_GAME)
        filtered_supply = supply.filter([lambda card,num: card == COPPER])
        filtered_supply.take(COPPER)
        self.assertEquals(59, filtered_supply.get_number_of_cards(COPPER))
        self.assertEquals(60, supply.get_number_of_cards(COPPER))
        self.assertEquals([COPPER], filtered_supply.get_cards())

    def test_can_get_kingdom_cards(self):
        supply = Supply(2, FIRST_GAME)
        self.assertEquals((CELLAR, MARKET, MILITIA, MINE, MOAT, REMODEL, SMITHY, VILLAGE, WOODCUTTER, WORKSHOP), supply.get_kingdom_cards())
