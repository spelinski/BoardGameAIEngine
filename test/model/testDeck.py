import unittest
from battleline.model.Deck import Deck

class TestDeck(unittest.TestCase):
    def test_deck_is_not_empty_by_default(self):
        self.assertFalse(Deck().is_empty())
        
    def test_can_draw_card_with_number_from_deck(self):
        self.assertGreater(Deck().draw().getNumber(),0)
        
    def test_can_draw_card_with_color_from_deck(self):
        self.assertGreater(len(Deck().draw().getColor()), 0)
        
    def test_can_draw_different_cards_from_deck(self):
        localDeck = Deck()
        self.assertNotEqual(localDeck.draw(), localDeck.draw())