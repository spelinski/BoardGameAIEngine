from random import shuffle

class Deck(object):
    """
    A Deck is modeled as an infinite generator that  begins
    to return None once the deck is empty. Drawing from the 
    deck is performed by calling next() on the deck as
    you would any python generator. 
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
    
    def next(self):
        """
        draw the next card from the deck
        @raise DeckEmptyError if the deck is empty
        """
        if self.is_empty():
            return None
        return self.deck.pop()

    def __iter__(self):
        return self

