import unittest
from itertools import product
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine, TroopCard
from battleline.player.BattlelinePlayer import BattlelinePlayer
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication


def get_engine_with_ordered_cards():
    comm1 = MockPlayerCommunication()
    comm2 = MockPlayerCommunication()
    comm1.add_response("player north PlayerNorth")
    comm2.add_response("player north PlayerSouth")
    engine = BattlelineEngine(BattlelinePlayer(
        comm1, "north"), BattlelinePlayer(comm2, "south"))

    # reinitialize the deck with a non shuffled deck to make things more reliable
    # don't do this in production code, the deck should be shuffled in real
    # code
    engine.troop_deck = Deck(sorted(engine.get_troop_cards(), key=lambda x: (
        x[1], x[0]), reverse=True), shuffleDeck=False)
    return engine


class TestBattlelineUninitializedEngine(unittest.TestCase):

    def setUp(self):
        self.engine = get_engine_with_ordered_cards()

    def test_can_create_engine_with_two_players(self):
        self.assertEquals("PlayerNorth", self.engine.player1.name)
        self.assertEquals("PlayerSouth", self.engine.player2.name)
        self.assertEquals([], self.engine.player1.hand)
        self.assertEquals([], self.engine.player2.hand)

    def test_board_deck_should_have_all_sixty_cards_to_start_with(self):
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        all_troops = [TroopCard(number, color) for color, number in sorted(
            product(colors, range(1, 11)), reverse=True)]
        return sorted(all_troops) == sorted(self.engine.troop_deck.deck)


class TestBattlelineInitializedEngine(unittest.TestCase):

    def setUp(self):
        self.engine = get_engine_with_ordered_cards()
        self.engine.initialize()

    def test_each_player_starts_with_7_cards_after_initialization(self):
        self.assertEquals([TroopCard(1, "BLUE"),
                           TroopCard(3, "BLUE"),
                           TroopCard(5, "BLUE"),
                           TroopCard(7, "BLUE"),
                           TroopCard(9, "BLUE"),
                           TroopCard(1, "GREEN"),
                           TroopCard(3, "GREEN")], self.engine.player1.hand)
        self.assertEquals([TroopCard(2, "BLUE"),
                           TroopCard(4, "BLUE"),
                           TroopCard(6, "BLUE"),
                           TroopCard(8, "BLUE"),
                           TroopCard(10, "BLUE"),
                           TroopCard(2, "GREEN"),
                           TroopCard(4, "GREEN")], self.engine.player2.hand)

    def test_one_turn_plays_a_troop_and_draws_new_one(self):
        # make new copies of the hand
        player1_hand = [card for card in self.engine.player1.hand]
        player2_hand = [card for card in self.engine.player2.hand]

        self.engine.progress_turn()

        self.assertHandsDifferBy1(player1_hand, self.engine.player1.hand)
        self.assertHandsDifferBy1(player2_hand, self.engine.player2.hand)

    def assertHandsDifferBy1(self, old_hand, new_hand):
        self.assertEquals(1, len(set(old_hand) - set(new_hand)))
        self.assertEquals(1, len(set(new_hand) - set(old_hand)))

    def test_players_hands_diminish_if_deck_runs_out(self):
        for i in xrange(23):
            self.engine.progress_turn()
        self.engine.progress_turn()
        self.assertEquals(6, len(self.engine.player1.hand))
        self.assertEquals(6, len(self.engine.player2.hand))

    def test_colors_are_sent_down_to_each_player(self):
        self.assertEquals(["colors color1 color2 color3 color4 color5 color6"],
                          self.engine.player1.communication.messages_received[1:])
        self.assertEquals(["colors color1 color2 color3 color4 color5 color6"],
                          self.engine.player2.communication.messages_received[1:])
