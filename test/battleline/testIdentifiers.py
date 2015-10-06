import unittest
from battleline.Identifiers import *


class TestIdentifiers(unittest.TestCase):

    def test_valid_identifiers(self):
        self.assertTrue(Identifiers.is_player_valid(Identifiers.NORTH))
        self.assertTrue(Identifiers.is_player_valid(Identifiers.SOUTH))
        self.assertFalse(Identifiers.is_player_valid("BLAH"))

    def test_get_card_string(self):
        self.assertEquals("RED,1", get_card_string(TroopCard(color="RED", number=1)))
        self.assertEquals("BLUE,10", get_card_string(TroopCard(color="BLUE", number=10)))
