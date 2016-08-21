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
        return self.hand

    def get_deck_cards(self):
        return self.deck.get_cards()

    def cleanup(self):
        for card in self.hand:
            self.discard_pile.add(card)
        self.hand = []
