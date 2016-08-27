import unittest
from mock import Mock
import json

from dominion.communication.CommunicationFlow import *

def create_player(send_and_wait_func):
    player = Mock()
    player.send_message_and_await_response = send_and_wait_func
    return player

class TestCommunicationFlow(unittest.TestCase):

    def test_can_handle_player_request(self):

        def send_message_and_await_response( json_message):
            message = json.loads(json_message)
            self.assertEquals("player-name-request", message["type"])
            return json.dumps({
                     "type": "player-name-reply",
                     "player_number": message["player_number"],
                     "name": "test-bot",
                     "version": message["version"]
                    })

        player = create_player(send_message_and_await_response)
        send_player_info(player, 1, 1)
        self.assertEquals("test-bot", player.name)

    def test_player_request_aborts_if_not_json(self):
        def invalid_message( json_message):
            return "nope"

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_type_not_supplied(self):
        def invalid_message( json_message):
            return json.dumps({})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: Not Present"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_not_right_message(self):
        def invalid_message( json_message):
            return json.dumps({"type": "nope"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: nope"):
            send_player_info(player, 1, 1)
