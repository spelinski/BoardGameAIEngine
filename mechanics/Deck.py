from random import shuffle
from Notification import *
class Deck(object):
    """
    A Deck is modeled as an infinite generator that  begins
    to return None once the deck is empty. Drawing from the
    deck is performed by calling next() on the deck as
    you would any python generator.
    """

    def __init__(self, listOfCards=[], shuffleDeck=True):
        """
        Constructor
        @param listOfCards list of the cards that start in the deck
        @param shuffleDeck go ahead and shuffle the deck (default True)
        @raise TypeError if the first parameter is not a list
        """

        if not isinstance(listOfCards, list):
            raise TypeError
        #need a new copy of a list if not valid
        self.deck = listOfCards if listOfCards else []
        self.notifier = None
        if shuffleDeck:
            self.shuffle()
        self.replenisher = None


    def shuffle(self):
        shuffle(self.deck)
        if self.notifier:
            self.notifier.notify(Notification("shuffle-deck"))

    def set_shuffle_notification(self, notifier):
        self.notifier = notifier

    def is_empty(self):
        return self.deck == []

    def add(self, card):
        """
        Add a card to the deck
        @param the card to add to the deck
        """
        self.deck.append(card)

    def get_cards(self):
        """
        Get a list  (copy) of cards in the deck
        """
        return list(self.deck)

    def draw(self):
        """providing a better named function for decks"""
        return self.next()

    def next(self):
        """
        draw the next card from the deck
        @return None if the deck is empty, or a card from the deck if it is not
                the deck will shuffle in the replenisher.
        """
        if self.is_empty():
            self.__replenish()
        if self.is_empty():
            return None
        return self.deck.pop()

    def __replenish(self):
        if self.replenisher:
            while self.replenisher:
                self.deck.append(next(self.replenisher))
            self.shuffle()

    def __nonzero__(self):
        return not self.is_empty()

    def set_replenisher(self, replenisher):
        """
        Set a collection to replenish from if this deck is empty
        @param replenisher the iterable to replenish from if we draw from an empty deck
               the replenisher must support a next() method
        """
        self.replenisher = replenisher


    def __iter__(self):
        return self
