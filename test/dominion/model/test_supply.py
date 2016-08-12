import unittest
from dominion.model.self.supply import *



class TestSupply(unittest.TestCase):

    def SetUp(self):
        self.self.supply = self.supply(2, "First Game")

    def check_first_set_kingdom_and_treasure_cards(self):
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Cellar"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Market"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Militia"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Mine"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Moat"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Remodel"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Smithy"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Village"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Woodcutter"))
        self.assertEquals(10, self.supply.get_number_of_kingdom_cards("Workshop"))

        self.assertEquals(60, self.supply.get_number_of_treasure_cards("Copper"))
        self.assertEquals(40, self.supply.get_number_of_treasure_cards("Silver"))
        self.assertEquals(30, self.supply.get_number_of_treasure_cards("Gold"))

    def test_first_set_two_players(self):
        self.check_first_set_kingdom_and_treasure_cards(self.supply)

        self.assertEquals(14, self.supply.get_number_of_victory_cards("Estate"))
        self.assertEquals(8, self.supply.get_number_of_victory_cards("Duchy"))
        self.assertEquals(8, self.supply.get_number_of_victory_cards("Province"))

        self.assertEquals(10, self.supply.get_number_of_curse_cards())

    def test_first_set_three_players(self):
        self.check_first_set_kingdom_and_treasure_cards(self.supply)

        self.assertEquals(21, self.supply.get_number_of_victory_cards("Estate"))
        self.assertEquals(12, self.supply.get_number_of_victory_cards("Duchy"))
        self.assertEquals(12, self.supply.get_number_of_victory_cards("Province"))

        self.assertEquals(20, self.supply.get_number_of_curse_cards())

    def test_first_set_three_players(self):
        self.check_first_set_kingdom_and_treasure_cards(self.supply)

        self.assertEquals(24, self.supply.get_number_of_victory_cards("Estate"))
        self.assertEquals(12, self.supply.get_number_of_victory_cards("Duchy"))
        self.assertEquals(12, self.supply.get_number_of_victory_cards("Province"))

        self.assertEquals(30, self.supply.get_number_of_curse_cards())

    def take_card_decreases_supply_appropriately(self):
