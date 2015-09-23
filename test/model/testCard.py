import unittest
from battleline.model.Card import Card

class TestCard(unittest.TestCase):
    def test_card_has_passed_in_value(self):
        self.assertEqual(Card(1,"").getNumber(),1)
        
    def test_card_has_passed_in_color(self):
        self.assertEqual(Card(0,"Blue").getColor(), "Blue")