import unittest
from dominion.model.Supply import *



class TestSupply(unittest.TestCase):

    def check_first_set_kingdom_and_treasure_cards(self, supply):
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Cellar"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Market"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Militia"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Mine"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Moat"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Remodel"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Smithy"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Village"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Woodcutter"))
        self.assertEquals(10, supply.get_number_of_kingdom_cards("Workshop"))

        self.assertEquals(60, supply.get_number_of_treasure_cards("Copper"))
        self.assertEquals(40, supply.get_number_of_treasure_cards("Silver"))
        self.assertEquals(30, supply.get_number_of_treasure_cards("Gold"))

    def test_first_set_two_players(self):
        supply = Supply(2, "First Game")
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(14, supply.get_number_of_victory_cards("Estate"))
        self.assertEquals(8, supply.get_number_of_victory_cards("Duchy"))
        self.assertEquals(8, supply.get_number_of_victory_cards("Province"))

        self.assertEquals(10, supply.get_number_of_curse_cards())

    def test_first_set_three_players(self):
        supply = Supply(3, "First Game")
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(21, supply.get_number_of_victory_cards("Estate"))
        self.assertEquals(12, supply.get_number_of_victory_cards("Duchy"))
        self.assertEquals(12, supply.get_number_of_victory_cards("Province"))

        self.assertEquals(20, supply.get_number_of_curse_cards())

    def test_first_set_three_players(self):
        supply = Supply(4, "First Game")
        self.check_first_set_kingdom_and_treasure_cards(supply)

        self.assertEquals(24, supply.get_number_of_victory_cards("Estate"))
        self.assertEquals(12, supply.get_number_of_victory_cards("Duchy"))
        self.assertEquals(12, supply.get_number_of_victory_cards("Province"))

        self.assertEquals(30, supply.get_number_of_curse_cards())
