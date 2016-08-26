import unittest
from dominion import Identifiers
from dominion.CardInfo import *
class TestCardInfo(unittest.TestCase):

    def test_can_check_if_victory_card(self):
        self.assertTrue(is_victory_card(Identifiers.ESTATE))
