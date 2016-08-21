from mechanics.Deck import Deck

class Player(object):

    def __init__(self):
        self.discard_pile = Deck()
        self.hand = []
        self.deck = Deck()
        self.deck.set_replenisher(self.discard_pile)

    def gain_card(self, card):
        self.discard_pile.add(card)

    def get_discard_pile(self):
        return self.discard_pile.get_cards()

    def get_top_discard_card(self):
        return self.discard_pile.get_cards()[-1] if self.discard_pile else None

    def draw_cards(self, num_to_draw):
        for _ in range(num_to_draw):
            card = self.deck.draw()
            if card is None:
                break
            self.add_to_hand(card)

    def add_to_hand(self, card):
        self.hand.append(card)

    def get_hand(self):
        return [card for card in self.hand]

    def get_deck_cards(self):
        return self.deck.get_cards()

    def cleanup(self):
        for card in self.get_hand():
            self.discard(card)
        assert self.hand == []

    def discard(self, card):
        if card not in self.hand:
            raise CardNotInHandException(card)
        self.discard_pile.add(card)
        self.hand.remove(card)


class CardNotInHandException(Exception):

    def __init__(self, card):
        """Create an Exception that the player is trying to take a card that isn't in the hand
        @param card the card that was expected to be in the hand
        """
        self.card = card

    def __str__(self):
        return "{} is not in the hand.".format(self.card)
