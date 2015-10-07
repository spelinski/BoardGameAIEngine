import unittest
from itertools import product
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine, TroopCard
from battleline.player.BattlelinePlayer import BattlelinePlayer
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
from battleline.Identifiers import Identifiers


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
        self.assertEquals([TroopCard(1, "color1"),
                           TroopCard(3, "color1"),
                           TroopCard(5, "color1"),
                           TroopCard(7, "color1"),
                           TroopCard(9, "color1"),
                           TroopCard(1, "color2"),
                           TroopCard(3, "color2")], self.engine.player1.hand)
        self.assertEquals([TroopCard(2, "color1"),
                           TroopCard(4, "color1"),
                           TroopCard(6, "color1"),
                           TroopCard(8, "color1"),
                           TroopCard(10, "color1"),
                           TroopCard(2, "color2"),
                           TroopCard(4, "color2")], self.engine.player2.hand)

    def test_one_turn_plays_a_troop_and_draws_new_one(self):
        # make new copies of the hand
        player1_hand = [card for card in self.engine.player1.hand]
        player2_hand = [card for card in self.engine.player2.hand]

        self.engine.player1.communication.add_response("play 1 color1,1")
        self.engine.player2.communication.add_response("play 1 color1,2")
        self.engine.progress_turn()

        self.assertHandsDifferBy1(player1_hand, self.engine.player1.hand)
        self.assertHandsDifferBy1(player2_hand, self.engine.player2.hand)

    def assertHandsDifferBy1(self, old_hand, new_hand):
        self.assertEquals(1, len(set(old_hand) - set(new_hand)))
        self.assertEquals(1, len(set(new_hand) - set(old_hand)))

    def __play_turn(self):
        self.engine.player1.communication.add_response("play 1 color1,1")
        self.engine.player2.communication.add_response("play 1 color1,2")
        self.engine.progress_turn()

    def test_players_hands_diminish_if_deck_runs_out(self):
        for i in xrange(23):
            self.__play_turn()
        self.__play_turn()
        self.assertEquals(6, len(self.engine.player1.hand))
        self.assertEquals(6, len(self.engine.player2.hand))

    def test_colors_are_sent_down_to_each_player(self):
        self.assertEquals(["colors color1 color2 color3 color4 color5 color6"],
                          self.engine.player1.communication.messages_received[1:])
        self.assertEquals(["colors color1 color2 color3 color4 color5 color6"],
                          self.engine.player2.communication.messages_received[1:])

    def test_information_is_sent_down_on_each_turn(self):
        self.__play_turn()

        self.assertEquals(["player north hand color1,1 color1,3 color1,5 color1,7 color1,9 color2,1 color2,3",
                           "flag claim-status unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed",
                           "flag 1 cards north", "flag 1 cards south", "flag 2 cards north", "flag 2 cards south",
                           "flag 3 cards north", "flag 3 cards south", "flag 4 cards north", "flag 4 cards south",
                           "flag 5 cards north", "flag 5 cards south", "flag 6 cards north", "flag 6 cards south",
                           "flag 7 cards north", "flag 7 cards south", "flag 8 cards north", "flag 8 cards south",
                           "flag 9 cards north", "flag 9 cards south", "go play-card"
                           ],
                          self.engine.player1.communication.messages_received[2:])
        self.assertEquals(["player south hand color1,2 color1,4 color1,6 color1,8 color1,10 color2,2 color2,4",
                           "flag claim-status unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed",
                           "flag 1 cards north color1,1", "flag 1 cards south", "flag 2 cards north", "flag 2 cards south",
                           "flag 3 cards north", "flag 3 cards south", "flag 4 cards north", "flag 4 cards south",
                           "flag 5 cards north", "flag 5 cards south", "flag 6 cards north", "flag 6 cards south",
                           "flag 7 cards north", "flag 7 cards south", "flag 8 cards north", "flag 8 cards south",
                           "flag 9 cards north", "flag 9 cards south", "opponent play 1 color1,1", "go play-card"
                           ],
                          self.engine.player2.communication.messages_received[2:])

    def test_invalid_moves_still_produce_a_valid_move(self):
        for i in xrange(4):
            self.__play_turn()
        self.assertEquals([TroopCard(color="color1", number=1),
                           TroopCard(color="color1", number=3),
                           TroopCard(color="color1", number=5)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.NORTH])
        self.assertEquals([TroopCard(color="color1", number=2),
                           TroopCard(color="color1", number=4),
                           TroopCard(color="color1", number=6)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.SOUTH])
        self.assertEquals([TroopCard(color="color1", number=7)],
                          self.engine.board_logic.board.get_flag(2).sides[Identifiers.NORTH])
        self.assertEquals([TroopCard(color="color1", number=8)],
                          self.engine.board_logic.board.get_flag(2).sides[Identifiers.SOUTH])

    def test_invalid_moves_with_flag_and_card(self):

        self.engine.player1.communication.add_response("play 1 blah,1")
        self.engine.player2.communication.add_response("play 1 color1,11")
        self.engine.progress_turn()

        self.engine.player1.communication.add_response("")
        self.engine.player1.communication.add_response("")
        self.engine.progress_turn()

        self.assertEquals([TroopCard(color="color1", number=1),
                           TroopCard(color="color1", number=3)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.NORTH])
        self.assertEquals([TroopCard(color="color1", number=2),
                           TroopCard(color="color1", number=4)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.SOUTH])

    def test_opponent_does_not_get_move_if_invalid(self):
        self.engine.player1.hand = []
        self.__play_turn()
        self.assertEquals(["player south hand color1,2 color1,4 color1,6 color1,8 color1,10 color2,2 color2,4",
                           "flag claim-status unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed",
                           "flag 1 cards north", "flag 1 cards south", "flag 2 cards north", "flag 2 cards south",
                           "flag 3 cards north", "flag 3 cards south", "flag 4 cards north", "flag 4 cards south",
                           "flag 5 cards north", "flag 5 cards south", "flag 6 cards north", "flag 6 cards south",
                           "flag 7 cards north", "flag 7 cards south", "flag 8 cards north", "flag 8 cards south",
                           "flag 9 cards north", "flag 9 cards south", "go play-card"
                           ],
                          self.engine.player2.communication.messages_received[2:])

    def test_unplayed_cards_after_initialization(self):
        expected_cards = set(self.engine.get_troop_cards())
        self.assertEquals(expected_cards, set(self.engine.get_unplayed_cards()))
        self.__play_turn()
        expected_cards = expected_cards - set([TroopCard(color="color1", number=1), TroopCard(color="color1", number=2)])
        self.assertEquals(expected_cards, set(self.engine.get_unplayed_cards()))
