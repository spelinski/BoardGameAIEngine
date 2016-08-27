import unittest
from dominion.communication.CommandGenerator import *

class TestCommandGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = CommandGenerator()

    def test_can_create_player_info_request(self):
        message = self.generator.create_player_info_request(2, 1)
        self.assertEquals("player-name-request", message["type"])
        self.assertEquals(1, message["version"])
        self.assertEquals("player2", message["player_number"])
