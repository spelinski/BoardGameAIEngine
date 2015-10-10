import unittest
from mechanics.Deck import Deck, DeckEmptyError


class TestDeck(unittest.TestCase):

    def test_deck_is_not_empty_by_default(self):
        listOfCards = [1]
        self.assertFalse(Deck(listOfCards, False).is_empty())

    def test_can_draw_card_from_deck(self):
        listOfCards = [1]
        drawnCard = Deck(listOfCards, False).draw()
        self.assertEqual(drawnCard, 1)

    def test_can_draw_different_cards_from_deck(self):
        listOfCards = [1, 2]
        localDeck = Deck(listOfCards, False)
        self.assertNotEqual(localDeck.draw(), localDeck.draw())

    def test_deck_is_empty_after_drawing_all_cards(self):
        listOfCards = [1, 2]
        localDeck = Deck(listOfCards, False)
        localDeck.draw()
        localDeck.draw()
        self.assertTrue(localDeck.is_empty())

    def test_returns_none_when_drawing_from_empty_deck(self):
        listOfCards = [1]
        localDeck = Deck(listOfCards, False)
        self.assertIsNotNone(localDeck.draw())
        self.assertIsNone(localDeck.draw())

    def test_deck_shuffle_does_not_change_actual_cards(self):
        listOfCards = list(range(1, 10))
        localDeck = Deck(listOfCards, False)
        localDeck.shuffle()
        self.assertEqual(set(localDeck.deck), set(listOfCards))

    def test_raise_type_error_if_no_list(self):
        self.assertRaisesRegexp(TypeError, "", Deck, "")
