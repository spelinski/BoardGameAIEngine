import unittest
from battleline.player.BattlelinePlayer import BattlelinePlayer, HandFullError, InvalidMoveError
from MockPlayerCommunication import MockPlayerCommunication


class TestBattlelinePlayer(unittest.TestCase):

    def setUp(self):
        self.communication = MockPlayerCommunication()
        self.communication.add_response("player north Player1")
        self.player = BattlelinePlayer(self.communication, "north")

    def test_battleline_player_has_name(self):
        self.assertEquals(self.player.name, "Player1")

    def test_battleline_player_has_dirction(self):
        self.assertEquals("north", self.player.direction)
        self.communication.add_response("player south Player1")
        self.player = BattlelinePlayer(self.communication, "south")
        self.assertEquals("south", self.player.direction)

    def test_battleline_player_has_empty_hand_to_start_with(self):
        self.assertEquals([], self.player.hand)

    def test_can_add_to_player_hand(self):
        self.player.add_to_hand(1)
        self.assertEquals([1], self.player.hand)
        self.player.add_to_hand(2)
        self.assertEquals([1, 2], self.player.hand)

    def test_can_not_exceed_hand_limit_of_seven(self):
        for i in xrange(7):
            self.player.add_to_hand(1)
        self.assertRaisesRegexp(
            HandFullError, "Cannot exceed hand limit of 7", self.player.add_to_hand, 2)

    def test_communication_contains_starting_request(self):
        self.assertEquals(["player north name"],
                          self.communication.messages_received)

    def test_sending_a_message_translates_to_communication(self):
        self.communication.add_response("This is a response")
        self.player.send_message("Command")
        self.assertEquals("This is a response", self.player.get_response())
        self.assertEquals(
            ["Command"], self.communication.messages_received[1:])
        self.assertEquals("", self.player.get_response())

    def test_exception_is_thrown_if_card_does_not_exist_in_player_hand(self):
        self.assertRaisesRegexp(
            InvalidMoveError, "Invalid Move - Player did not have card in hand", self.player.remove_from_hand, 1)

    def test_can_remove_card_from_hand(self):
        self.player.add_to_hand(1)
        self.player.add_to_hand(2)
        self.player.remove_from_hand(1)
        self.assertEquals([2], self.player.hand)
