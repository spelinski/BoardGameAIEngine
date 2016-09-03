from mechanics.Deck import Deck
from dominion.CardInfo import *

class Player(object):

    def __init__(self):
        self.discard_pile = Deck()
        self.hand = []
        self.deck = Deck()
        self.deck.set_replenisher(self.discard_pile)
        self.played = []
        self.turns = 0

    def set_communication(self, comm):
        self.comm = comm

    def close_communication(self):
        if self.comm:
            self.comm.close()

    def send_message_and_await_response(self, message):
        self.comm.send_message(message)
        return self.comm.get_response()

    def send_message(self, message):
        self.comm.send_message(message)

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

    def put_card_on_top_of_deck(self, card):
        self.deck.add(card)

    def get_hand(self):
        return list(self.hand)

    def get_deck_cards(self):
        return self.deck.get_cards()

    def __get_cards_to_discard(self):
        return self.hand+self.played

    def cleanup(self, top_discard = ""):
        for card in self.__get_cards_to_discard():
            if card != top_discard:
                self.discard(card)
        for card in self.__get_cards_to_discard():
            self.discard(card)
        assert self.hand == []
        assert self.played == []

    def discard(self, card):
        if card not in self.hand and card not in self.played:
            raise CardNotInHandException(card)
        self.discard_pile.add(card)
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.played:
            self.played.remove(card)


    def trash(self, card):
        if card not in self.hand:
            raise CardNotInHandException(card)
        self.hand.remove(card)

    def play_card(self, card):
        if card not in self.hand:
            raise CardNotInHandException(card)
        self.hand.remove(card)
        self.played.append(card)

    def get_played_cards(self):
        return list(self.played)

    def get_number_of_turns_taken(self):
        return self.turns

    def mark_turn_taken(self):
        self.turns += 1

    def get_score(self):
        all_cards = self.get_hand() + self.get_deck_cards() + self.get_discard_pile()
        return sum([get_victory_points(card) for card in all_cards])


class CardNotInHandException(Exception):

    def __init__(self, card):
        """Create an Exception that the player is trying to take a card that isn't in the hand
        @param card the card that was expected to be in the hand
        """
        self.card = card

    def __str__(self):
        return "{} is not in the hand.".format(self.card)
