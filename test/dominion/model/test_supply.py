import unittest
from dominion.model.Supply import *



class TestSupply(unittest.TestCase):

    def check_first_set_kingdom_and_treasure_cards(self, supply):
        self.assertEquals(10, supply.get_number_of_cards("Cellar"))
        self.assertEquals(10, supply.get_number_of_cards("Market"))
        self.assertEquals(10, supply.get_number_of_cards("Militia"))
        self.assertEquals(10, supply.get_number_of_cards("Mine"))
        self.assertEquals(10, supply.get_number_of_cards("Moat"))
        self.assertEquals(10, supply.get_number_of_cards("Remodel"))
        self.assertEquals(10, supply.get_number_of_cards("Smithy"))
        self.assertEquals(10, supply.get_number_of_cards("Village"))
        self.assertEquals(10, supply.get_number_of_cards("Woodcutter"))
        self.assertEquals(10, supply.get_number_of_cards("Workshop"))

        self.assertEquals(60, supply.get_number_of_cards("Copper"))
        self.assertEquals(40, supply.get_number_of_cards("Silver"))
        self.assertEquals(30, supply.get_number_of_cards("Gold"))

    def test_first_set_two_players(self):
        supply = Supply(2, "First Game")
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(14, supply.get_number_of_cards("Estate"))
        self.assertEquals(8, supply.get_number_of_cards("Duchy"))
        self.assertEquals(8, supply.get_number_of_cards("Province"))

        self.assertEquals(10, supply.get_number_of_cards("Curse"))

    def test_first_set_three_players(self):
        supply = Supply(3, "First Game")
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(21, supply.get_number_of_cards("Estate"))
        self.assertEquals(12, supply.get_number_of_cards("Duchy"))
        self.assertEquals(12, supply.get_number_of_cards("Province"))

        self.assertEquals(20, supply.get_number_of_cards("Curse"))

    def test_first_set_three_players(self):
        supply = Supply(4, "First Game")
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(24, supply.get_number_of_cards("Estate"))
        self.assertEquals(12, supply.get_number_of_cards("Duchy"))
        self.assertEquals(12, supply.get_number_of_cards("Province"))

        self.assertEquals(30, supply.get_number_of_cards("Curse"))

    def test_take_card_decreases_supply_appropriately(self):
        supply = Supply(2, "First Game")
        supply.take("Province")
        self.assertEquals(7, supply.get_number_of_cards("Province"))

    def test_cant_take_card_not_in_supply(self):
        supply = Supply(2, "First Game")
        with self.assertRaises(CardNotInSupplyException):
            supply.take("Feast")

    def test_cant_take_card_not_if_pile_is_empty(self):
        supply = Supply(2, "First Game")
        for _ in range(8):
            supply.take("Duchy")
        with self.assertRaises(PileEmptyException):
            supply.take("Duchy")

    def test_no_piiles_are_empty_to_start(self):
        supply = Supply(2, "First Game")
        self.assertEquals(0, supply.get_number_of_empty_piles())

    def test_can_empty_piles(self):
        supply = Supply(2, "First Game")
        for _ in range(10):
            supply.take("Moat")
            supply.take("Remodel")
            supply.take("Market")
        self.assertEquals(3, supply.get_number_of_empty_piles())
