from mechanics.Deck import Deck
from collections import namedtuple
from itertools import product

TroopCard = namedtuple("TroopCard", ["color", "number"])
class BattlelineEngine(object):
    """
    An engine that coordinates two players, a board and the decks for battleline
    """

    def __init__(self, player1, player2):
        """
        Constructor
        @param player1 the first player
        @param player2 the second player
        """
        self.player1 = player1
        self.player2 = player2
        self.troop_deck = Deck(self.get_troop_cards())

    def initialize(self):
        """
        Initialize the game
        Deal seven cards to each player
        """
        for i in xrange(7):
            self.player1.add_to_hand(self.troop_deck.draw())
            self.player2.add_to_hand(self.troop_deck.draw())

    def get_troop_cards(self):
        """
        Get the troop cards
        @return A list of all troop cards
        """
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        return [TroopCard(name,number) for name,number in sorted(product(colors, range(1,11)), reverse=True)]
