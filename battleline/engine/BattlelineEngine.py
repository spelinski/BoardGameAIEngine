from battleline.model.Deck import Deck

class BattlelineEngine(object):
    """
    An engine that coordinates two players, a board and the decks for battleline
    """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.deck = Deck()
        for i in xrange(7):
            self.player1.add_to_hand(self.deck.draw())
            self.player2.add_to_hand(self.deck.draw())
