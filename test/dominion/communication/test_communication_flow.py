import unittest
from mock import Mock
import json

from dominion.communication.CommunicationFlow import *

class TestCommunicationFlow(unittest.TestCase):

    def test_can_handle_player_request(self):
        player = Mock()
        def send_message_and_await_response( json_message):
            message = json.loads(json_message)
            self.assertEquals("player-name-request", message["type"])
            return {
                     "type": "player-name-reply",
                     "player_number": message["player_number"],
                     "name": "test-bot",
                     "version": message["version"]
                    }

        player.send_message_and_await_response = send_message_and_await_response
        send_player_info(player, 1, 1)
        self.assertEquals("test-bot", player.name)
