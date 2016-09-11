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

    def test_play_turn_request(self):
        message = self.generator.create_play_turn_request(1, 2, 3, ["copper", "copper"], ["moat"], ["silver"])
        self.assertEquals("play-turn", message["type"])
        self.assertEquals(1, message["actions"])
        self.assertEquals(2, message["buys"])
        self.assertEquals(3, message["extra_money"])
        self.assertEquals(["copper", "copper"], message["hand"])
        self.assertEquals(["moat"], message["cards_played"])
        self.assertEquals(["silver"], message["cards_gained"])

    def test_play_action_request(self):
        message = self.generator.create_attack_request_discard(2, ["copper", "copper", "copper", "copper", "copper"])
        self.assertEquals("attack-request", message["type"])
        self.assertEquals(2, message["discard"])
        self.assertEquals(["copper", "copper", "copper", "copper", "copper"], message["options"])

    def test_player_shuffled_message(self):
        message = self.generator.create_player_shuffled_message(3)
        self.assertEquals("player-shuffled", message["type"])
        self.assertEquals(3, message["player_number"])

    def test_game_info_mesasge(self):
        message = self.generator.create_game_info_message([1,2,3,4,5,6])
        self.assertEquals("game-info", message["type"])
        self.assertEquals([1,2,3,4,5,6], message["kingdom_cards"])
