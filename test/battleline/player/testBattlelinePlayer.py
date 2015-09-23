import unittest
from battleline.player.BattlelinePlayer import BattlelinePlayer, HandFullError
from MockPlayerCommunication import MockPlayerCommunication
class TestBattlelinePlayer(unittest.TestCase):

    def setUp(self):
        self.communication = MockPlayerCommunication()
        self.player = BattlelinePlayer("Player1", self.communication)


    def test_battleline_player_has_name(self):
        self.assertEquals(self.player.name, "Player1")

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
        self.assertRaisesRegexp(HandFullError, "Cannot exceed hand limit of 7", self.player.add_to_hand, 2)

    def test_communication_does_not_contain_message_to_begin_with(self):
        self.assertEquals([], self.communication.messages_received)

    def test_sending_a_message_translates_to_communication(self):
        self.communication.add_response("This is a response")
        self.assertEquals("This is a response", self.player.send_message("Command"))
        self.assertEquals(["Command"], self.communication.messages_received)
        self.assertEquals("", self.player.send_message("Command"))
