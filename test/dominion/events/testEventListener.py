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
        player.received_message = None
        def receive_message(json_message):
            player.received_message = json.loads(json_message)
        player.send_message = receive_message
        return player

    def test_can_respond_to_shuffle_event(self):
        self.listener.notify(Notification("shuffle-deck"))
        for player in self.players:
            self.assertEquals({"type": "player-shuffled", "player_number": 1}, player.received_message)

    def test_can_respond_to_gained(self):
        self.listener.notify(Notification("gained-cards", cards=range(3)))
        for player in self.players:
            self.assertEquals({"type": "player-gained", "player_number": 1, "gained": range(3)}, player.received_message)

    def test_can_respond_to_played(self):
        self.listener.notify(Notification("played-cards", cards=range(4)))
        for player in self.players:
            self.assertEquals({"type": "player-played", "player_number": 1, "played": range(4)}, player.received_message)

    def test_can_respond_to_trashed(self):
        self.listener.notify(Notification("trashed-cards", cards=range(2)))
        for player in self.players:
            self.assertEquals({"type": "player-trashed", "player_number": 1, "trashed": range(2)}, player.received_message)

    def test_can_respond_to_discard(self):
        self.listener.notify(Notification("discard-card", card="ace-of-spades"))
        for player in self.players:
            self.assertEquals({"type": "player-top-discard", "player_number": 1, "card": "ace-of-spades"}, player.received_message)

    def test_can_respond_to_revealed(self):
        self.listener.notify(Notification("revealed-cards", cards=range(2)))
        for player in self.players:
            self.assertEquals({"type": "player-reveal", "player_number": 1, "cards": range(2)}, player.received_message)

    def test_wrong_notification_doesnt_get_sent(self):
        self.listener.notify(Notification(""))
        for player in self.players:
            self.assertIsNone(player.received_message)
