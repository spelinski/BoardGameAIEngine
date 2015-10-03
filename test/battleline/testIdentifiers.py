import unittest
from battleline.Identifiers import *

class TestIdentifiers(unittest.TestCase):
    def test_valid_identifiers(self):
        self.assertTrue(Identifiers.is_player_valid(Identifiers.NORTH))
        self.assertTrue(Identifiers.is_player_valid(Identifiers.SOUTH))
        self.assertFalse(Identifiers.is_player_valid("BLAH"))
