from mechanics.Deck import Deck
from BoardLogic import BoardLogic
from itertools import product
from battleline.Identifiers import TroopCard, Identifiers

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
        self.board_logic = BoardLogic(self)
        self.last_move = None

    def initialize(self):
        """
        Initialize the game
        Deal seven cards to each player
        """
        initial_cards = [next(self.troop_deck) for _ in range(14)]
        self.player1.new_game(Identifiers.NORTH, initial_cards[::2])
        self.player2.new_game(Identifiers.SOUTH, initial_cards[1::2]) 

    def get_troop_cards(self):
        """
        Get the troop cards
        @return A list of all troop cards
        """
        return [TroopCard(number, color) for color, number in product(Identifiers.COLORS, range(1, 11))]

    def get_unplayed_cards(self):
        """
        get all cards that have not been played yet
        @return all unplayed cards
        """
        return self.troop_deck.deck + self.player1.hand + self.player2.hand

    def progress_turn(self):
        """
        Perform one turn
        """
        self.compute_player_turn(self.player1)
        self.compute_player_turn(self.player2)

    def compute_player_turn(self, player):
        card, flag = player.compute_turn(self.board_logic.board,self.last_move)
        flag = self.compute_played_flag(flag, player.direction)
        card = self.compute_played_card(card, player.hand)
        self.board_logic.addCard(flag - 1, player.direction, card)
        player.finish_turn(card,next(self.troop_deck)) 
        self.board_logic.checkAllFlags()
        self.last_move = (card,flag)

    def compute_played_flag(self, flag, direction):
        if self.board_logic.is_flag_playable(flag - 1, direction):
            return flag
        return next((f for f in xrange(1, 10) if self.board_logic.is_flag_playable(f - 1, direction)), None)

    def compute_played_card(self, card, hand):
        if card in hand:
            return card
        return hand[0] if hand else None

