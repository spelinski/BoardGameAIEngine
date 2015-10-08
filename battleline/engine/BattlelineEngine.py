from mechanics.Deck import Deck
from BoardLogic import BoardLogic
from itertools import product
from battleline.Identifiers import TroopCard, Identifiers
from CommandParser import ClientCommandParser, InvalidParseError


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
        self.player1.generator.send_colors()
        self.player2.generator.send_colors()

        self.lastMove = None

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
        self.__make_player_turn(self.player1)
        self.__make_player_turn(self.player2)

    def __make_player_turn(self, player):
        self.__send_messages_to_player(player)
        flag, card = self.__get_flag_and_card_from_player(player)
        self.lastMove = flag, card
        if card and flag:
            self.__process_player_turn(player, flag, card)
        self.board_logic.checkAllFlags()

    def __process_player_turn(self, player, flag, card):
        player.remove_from_hand(card)
        self.board_logic.addCard(
            flag - 1, player.direction, card)
        if not self.troop_deck.is_empty():
            player.add_to_hand(self.troop_deck.draw())

    def __send_messages_to_player(self, player):
        player.generator.send_player_hand(player.hand)
        player.generator.send_flag_claim_status(self.board_logic.board.flags)
        player.generator.send_flag_cards(self.board_logic.board.flags)
        if self.lastMove:
            player.generator.send_opponent_play(
                self.lastMove[0], self.lastMove[1])
        player.generator.send_go_play()

    def __get_flag_and_card_from_player(self, player):
        try:
            data = ClientCommandParser().parse(player.communication.get_response())
            flag, card = data["value"]
        except InvalidParseError:
            flag, card = 1, None
        return self.__get_valid_flag(flag, player.direction), self.__get_valid_card(card, player.hand)

    def __get_valid_flag(self, flag, direction):
        if self.board_logic.is_flag_playable(flag - 1, direction):
            return flag
        return next((f for f in xrange(1, 10) if self.board_logic.is_flag_playable(f - 1, direction)), None)

    def __get_valid_card(self, card, hand):
        if card in hand:
            return card
        return hand[0] if hand else None
