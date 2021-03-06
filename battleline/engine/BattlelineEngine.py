from mechanics.Deck import Deck
from BoardLogic import BoardLogic
from itertools import product
from battleline.Identifiers import TroopCard, Identifiers
from battleline.model.Play import Play


class BattlelineEngine(object):

    """
    An engine that coordinates two players, a board and the decks for battleline
    """

    def __init__(self, player1, player2, output):
        """
        Constructor
        @param player1 the first player
        @param player2 the second player
        """
        self.player1 = player1
        self.player2 = player2
        self.troop_deck = Deck(self.get_troop_cards())
        self.output_handler = output
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

        self.output_handler.setup_player_positions(
            self.player1.name, Identifiers.NORTH)
        self.output_handler.setup_player_positions(
            self.player2.name, Identifiers.SOUTH)

        for i in range(0, 14, 2):
            self.output_handler.draw_action(
                self.player1.direction, initial_cards[i])
            self.output_handler.draw_action(
                self.player2.direction, initial_cards[i + 1])

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

    def get_winning_player(self):
        """
        get winning player
        @return the player name that wins, otherwise None
        """
        return self.board_logic.winner

    def get_winning_player_name(self):
        """
        get the winning player name
        @return the inning player name
        """
        if self.get_winning_player() == Identifiers.NORTH: return self.player1.name
        if self.get_winning_player() == Identifiers.SOUTH: return self.player2.name
        return None

    def run_until_game_end(self):
        """
        Run until the game ends
        """
        while self.get_winning_player() is None:
            self.progress_turn()

    def progress_turn(self):
        """
        Perform one turn
        """
        self.compute_player_turn(self.player1)
        if self.get_winning_player() is None:
            self.compute_player_turn(self.player2)

    def compute_player_turn(self, player):
        """
        For a given player, coordinate with the player to compute its next turn.
        :param player: The player who is taking a turn.
        """
        flags_open = self.board_logic.is_any_flag_playable(player.direction)
        play = player.compute_turn(self.board_logic.board, flags_open, self.last_move)
        real_play = self.compute_real_play(player, play)
        if real_play.flag is not None:
            self.board_logic.addCard(
                real_play.flag - 1, player.direction, real_play.card)

            cardToBeDrawn = next(self.troop_deck)
            player.finish_turn(real_play.card, cardToBeDrawn)
            self.output_handler.draw_action(player.direction, cardToBeDrawn)
            self.last_move = real_play
        self.board_logic.checkAllFlags(player.direction)

    def compute_real_play(self, player, play):
        """
        Compute the "real" play based on an attempted play by player. In the case of
        an invalid move taken by a player, a move will be chosen at random from the set
        of valid moves.
        :param player: The player who is attempting to play
        :param play: The play attempted by the player
        :return: A valid play
        """
        flag = self.compute_played_flag(play.flag, player.direction)
        card = self.compute_played_card(play.card, player.hand)
        return Play(flag=flag, card=card)

    def compute_played_flag(self, flag, direction):
        """
        Compute the "real" played flag based on an attempted play by the player.
        :param flag: The flag that is being attempted.
        :param direction: The direction the player was facing.
        :return: A guaranteed valid flag.
        """
        if self.board_logic.is_flag_playable(flag - 1, direction):
            return flag
        return self.board_logic.get_first_playable_flag(direction)

    def compute_played_card(self, card, hand):
        """
        Compute the "real" played card based on an attempted play by the player.
        :param card: The card that is being attempted.
        :param hand: The players current hand
        :return: A guaranteed valid card.
        """
        if card in hand:
            return card
        return hand[0] if hand else None
