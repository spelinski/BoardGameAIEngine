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
        player1.communication.send_message("player 1 hand red 1 blue 5 white 2 green 10 red 3 green 3 white 6")
        player2.communication.send_message("player 2 hand red 7 blue 4 white 8 green 1 red 2 green 4 white 9")
