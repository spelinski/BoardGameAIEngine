import unittest
from mechanics.Deck import Deck
from mock import Mock

class TestDeck(unittest.TestCase):

    def test_empty_deck_is_empty(self):
        self.assertTrue(Deck().is_empty())

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
        self.assertNotEqual(next(localDeck), next(localDeck))

    def test_deck_is_empty_after_drawing_all_cards(self):
        listOfCards = [1, 2]
        localDeck = Deck(listOfCards, False)
        next(localDeck)
        next(localDeck)
        self.assertTrue(localDeck.is_empty())

    def test_returns_none_when_drawing_from_empty_deck(self):
        listOfCards = [1]
        localDeck = Deck(listOfCards, False)
        self.assertIsNotNone(next(localDeck))
        self.assertIsNone(next(localDeck))

    def test_deck_shuffle_does_not_change_actual_cards(self):
        listOfCards = list(range(1, 10))
        localDeck = Deck(listOfCards, False)
        localDeck.shuffle()
        self.assertEqual(set(localDeck.deck), set(listOfCards))

    def test_raise_type_error_if_no_list(self):
        self.assertRaisesRegexp(TypeError, "", Deck, "")

    def test_can_replenish_deck(self):
        replenisher = Deck([2])
        deck = Deck([1])
        deck.set_replenisher(replenisher)
        self.assertEqual(1, deck.draw())
        self.assertEqual(2, deck.draw())
        self.assertIsNone(deck.draw())

    def test_deck_is_empty_before_replenish(self):
        replenisher = Deck([2])
        deck = Deck([1])
        deck.set_replenisher(replenisher)
        self.assertEqual(1, deck.draw())
        self.assertTrue(deck.is_empty())

    def test_deck_replenisher_is_empty_after_after_replenish(self):
        replenisher = Deck([2,3,4])
        deck = Deck([1])
        deck.set_replenisher(replenisher)
        self.assertEqual(1, deck.draw())
        deck.draw()
        self.assertTrue(replenisher.is_empty())

    def test_can_add_to_deck(self):
        deck = Deck([1])
        deck.add(2)
        self.assertEqual([1,2], deck.get_cards())
        self.assertEqual(2, deck.draw())
        self.assertEqual(1, deck.draw())


    def test_getting_cards_returns_copy(self):
        deck = Deck([1,2,3], shuffleDeck=False)
        cards = deck.get_cards()
        self.assertEquals([1,2,3], cards)
        deck.draw()
        self.assertEquals([1,2,3], cards)

    def test_notification_of_shuffle(self):
        deck = Deck([1,2], shuffleDeck = False)
        listener = Mock()
        listener.hit_function = False
        def notify(notification):
            self.assertEquals(notification.type, "shuffle-deck")
            listener.hit_function = True
        listener.notify = notify
        deck.add_shuffle_listener(listener)
        deck.shuffle()
        self.assertTrue(listener.hit_function)
