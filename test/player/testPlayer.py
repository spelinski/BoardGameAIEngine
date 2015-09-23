import unittest
from player.Player import Player
class TestPlayer(unittest.TestCase):

    def test_player_can_be_given_a_name(self):
        player = Player("Player 1")
        self.assertEquals("Player 1", player.name)

    def test_take_turn_is_unimplemented(self):
        with self.assertRaises(NotImplementedError):
            Player("").take_turn()
