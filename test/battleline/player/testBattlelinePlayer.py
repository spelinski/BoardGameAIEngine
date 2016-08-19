import unittest
from battleline.player.BattlelinePlayer import Player, SubprocessPlayer
from battleline.Identifiers import TroopCard, Identifiers
from battleline.model.Board import Board
from MockPlayerCommunication import MockPlayerCommunication
from battleline.model.Play import Play


class TestPlayer(unittest.TestCase):

    def test_player_throws_if_not_implemented(self):
        player = Player()
        with self.assertRaises(NotImplementedError):
            player.compute_turn(Board(), True, None)


class TestSubprocessPlayer(unittest.TestCase):

    def setUp(self):
        self.communication = MockPlayerCommunication()
        self.player = SubprocessPlayer(self.communication)
        self.initial_hand = [
            TroopCard(number=1, color="color1"),
            TroopCard(number=2, color="color1"),
            TroopCard(number=3, color="color1"),
            TroopCard(number=4, color="color1"),
            TroopCard(number=5, color="color1"),
            TroopCard(number=6, color="color1"),
            TroopCard(number=7, color="color1")
        ]
        self.initial_board = Board()

    def test_player_has_name(self):
        self.communication.add_response("player north Player1")
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.assertEquals(self.player.name, "Player1")

    def test_player_name_timeout(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.assertEquals(self.player.name, "north")

    def test_player_has_dirction(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.assertEquals("north", self.player.direction)

    def test_player_has_empty_hand_to_start_with(self):
        self.assertEquals([], self.player.hand)

    def test_communication_contains_starting_request(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.assertEquals(
            ["player north name",
             "colors color1 color2 color3 color4 color5 color6"], self.communication.messages_received)

    def test_player_can_get_next_action(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.communication.clear()
        self.communication.add_response("play 4 color1,7")
        play = self.player.compute_turn(self.initial_board,True, None)
        self.assertEquals(play.card, TroopCard(number=7, color="color1"))
        self.assertEquals(play.flag, 4)

    def test_player_receives_game_state(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.communication.clear()
        self.player.compute_turn(self.initial_board,True, None)

        self.assertEquals(self.communication.messages_received,
                          ["player north hand color1,1 color1,2 color1,3 color1,4 color1,5 color1,6 color1,7",
                           "flag claim-status unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed",
                           "flag 1 cards north",
                           "flag 1 cards south",
                           "flag 2 cards north",
                           "flag 2 cards south",
                           "flag 3 cards north",
                           "flag 3 cards south",
                           "flag 4 cards north",
                           "flag 4 cards south",
                           "flag 5 cards north",
                           "flag 5 cards south",
                           "flag 6 cards north",
                           "flag 6 cards south",
                           "flag 7 cards north",
                           "flag 7 cards south",
                           "flag 8 cards north",
                           "flag 8 cards south",
                           "flag 9 cards north",
                           "flag 9 cards south",
                           "go play-card"
                           ]
                          )

    def test_player_receives_game_state_with_last_move(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.communication.clear()
        self.player.compute_turn(self.initial_board, True,Play(
            card=TroopCard(number=3, color="color4"), flag=4))

        self.assertEquals(self.communication.messages_received,
                          ["player north hand color1,1 color1,2 color1,3 color1,4 color1,5 color1,6 color1,7",
                           "flag claim-status unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed",
                           "flag 1 cards north",
                           "flag 1 cards south",
                           "flag 2 cards north",
                           "flag 2 cards south",
                           "flag 3 cards north",
                           "flag 3 cards south",
                           "flag 4 cards north",
                           "flag 4 cards south",
                           "flag 5 cards north",
                           "flag 5 cards south",
                           "flag 6 cards north",
                           "flag 6 cards south",
                           "flag 7 cards north",
                           "flag 7 cards south",
                           "flag 8 cards north",
                           "flag 8 cards south",
                           "flag 9 cards north",
                           "flag 9 cards south",
                           "opponent play 4 color4,3",
                           "go play-card"
                           ]
                          )

    def test_player_removes_cards_on_turn_finish(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.player.finish_turn(
            TroopCard(number=4, color="color1"), TroopCard(number=2, color="color2"))
        self.assertNotIn(TroopCard(number=4, color="color1"), self.player.hand)
        self.assertIn(TroopCard(number=2, color="color2"), self.player.hand)
        self.assertEquals(7, len(self.player.hand))

    def test_player_hand_diminishes_with_empty_deck(self):
        self.player.new_game(Identifiers.NORTH, self.initial_hand)
        self.player.finish_turn(TroopCard(number=4, color="color1"), None)
        self.assertNotIn(TroopCard(number=4, color="color1"), self.player.hand)
        self.assertEquals(6, len(self.player.hand))
