import unittest
from mechanics.Deck import Deck
from mechanics.Deck import DeckEmptyError
from collections import namedtuple

class TestDeck(unittest.TestCase):
    def test_deck_is_not_empty_by_default(self):
        Card = namedtuple('Card', 'number,color')
        listOfCards = [Card(number=1,color="Blue")]
        self.assertFalse(Deck(listOfCards).is_empty())
        
    def test_can_draw_card_from_deck(self):
        Card = namedtuple('Card', 'number,color')
        listOfCards = [Card(number=1,color="Blue")]
        drawnCard = Deck(listOfCards).draw()
        self.assertGreater(drawnCard.number,0)
        self.assertGreater(len(drawnCard.color), 0)        
        
    def test_can_draw_different_cards_from_deck(self):
        Card = namedtuple('Card', 'number,color')
        listOfCards = [Card(number=1,color="Blue"),Card(number=2,color="Blue")]
        localDeck = Deck(listOfCards)
        self.assertNotEqual(localDeck.draw(), localDeck.draw())
        
    def test_deck_is_empty_after_drawing_all_cards(self):
        Card = namedtuple('Card', 'number,color')
        listOfCards = [Card(number=1,color="Blue"),Card(number=2,color="Blue")]
        localDeck = Deck(listOfCards)
        localDeck.draw()
        localDeck.draw()
        self.assertTrue(localDeck.is_empty())
        
    def test_error_thrown_when_drawing_from_empty_deck(self):
        Card = namedtuple('Card', 'number,color')
        listOfCards = [Card(number=1,color="Blue")]
        localDeck = Deck(listOfCards)
        localDeck.draw()
        self.assertRaisesRegexp(DeckEmptyError, "Attempted to draw on an empty Deck", localDeck.draw)
            
        
        
    