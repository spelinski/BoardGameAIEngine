import unittest
from dominion.model.Supply import *

def get_number_of_kingdom_cards(supply, card):
    return supply["kingdom"][card]

def get_number_of_treasure_cards(supply, card):
    return supply["treasure"][card]

def get_number_of_victory_cards(supply, card):
    return supply["treasure"][card]

def get_number_of_curse_cards(supply):
    return supply["treasure"]["curse"]

class TestSupply(unittest.TestCase):

    def test_first_set_two_players(self):
        supply = create_supply(2, "first_set")
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Cellar"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Market"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Militia"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Mine"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Moat"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Remodel"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Smithy"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Village"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Woodcutter"))
        self.assertEquals(10, get_number_of_kingdom_cards(supply,"Workshop"))

        self.assertEquals(60, get_number_of_treasure_cards(supply,"Copper"))
        self.assertEquals(40, get_number_of_treasure_cards(supply,"Silver"))
        self.assertEquals(30, get_number_of_treasure_cards(supply,"Gold"))

        self.assertEquals(8, get_number_of_victory_cards(supply,"Estate"))
        self.assertEquals(8, get_number_of_victory_cards(supply,"Duchy"))
        self.assertEquals(8, get_number_of_kingdom_cards(supply,"Province"))

        self.assertEquals(10, get_number_of_curse_cards(supply))
