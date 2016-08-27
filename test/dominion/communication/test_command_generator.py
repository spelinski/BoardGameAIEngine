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

    def test_can_create_supply_message(self):
        message = self.generator.create_supply_info_message({"copper" : 15, "curse" : 0})
        self.assertEquals("supply-info", message["type"])
        self.assertEquals(2, len(message["cards"]))
        self.assertEquals(15, message["cards"]["copper"])
        self.assertEquals(0, message["cards"]["curse"])
