import unittest
import json
from dominion.events.EventListener import *
from dominion.model.Player import *
from mechanics.Notification import *

class TestEventListener(unittest.TestCase):

    def setUp(self):
        self.players = [self.create_player(),self.create_player()]
        self.listener = EventListener(1, self.players)

    def create_player(self):
        player = Player()
        def receive_message(json_message):
            player.received_message = json.loads(json_message)
        player.send_message = receive_message
        return player

    def test_can_respond_to_shuffle_event(self):
        self.listener.notify(Notification("shuffle-deck"))
        for player in self.players:
            self.assertEquals({"type": "player-shuffled", "player_number": 1}, player.received_message)
