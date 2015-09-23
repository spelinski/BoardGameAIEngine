from random import shuffle


class Deck(object):
    """
    Deck object
    """

    def __init__(self, listOfCards, shuffleDeck=True):
        """
        Constructor
        @param listOfCards list of the cards that start in the deck
        @param shuffleDeck go ahead and shuffle the deck (default True)
        @raise TypeError if the first parameter is not a list
        """
        if not isinstance(listOfCards, list):
            raise TypeError
        self.deck = listOfCards
        if shuffleDeck:
            self.shuffle()

    def shuffle(self):
        shuffle(self.deck)

    def is_empty(self):
        return self.deck == []

    def draw(self):
        """
        draw the next card from the deck
        @raise DeckEmptyError if the deck is empty
        """
        if self.is_empty():
            raise DeckEmptyError("draw")
        return self.deck.pop()


class DeckEmptyError(Exception):

    def __init__(self, attemptedAction):
        """Create an Exception that the index is not valid
        @param attemptedAction what was trying to be done on an empty deck
        """
        self.attemptedAction = attemptedAction

    def __str__(self):
        return "Attempted to {} on an empty Deck".format(self.attemptedAction)
