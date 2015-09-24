import unittest
from battleline.player.BattlelinePlayer import BattlelinePlayer, HandFullError
class TestBattlelinePlayer(unittest.TestCase):

    def setUp(self):
        self.player = player = BattlelinePlayer("Player1")

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
