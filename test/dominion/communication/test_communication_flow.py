import unittest
from mock import Mock
from dominion.model.Supply import *
from dominion.model.Player import *
import json

from dominion.communication.CommunicationFlow import *

def create_player(func):
    player = Player()
    player.send_message_and_await_response = func
    player.send_message = func
    return player

def return_string(json_message):
    return "nope"

def return_invalid_json(json_message):
    return json.dumps({})

def return_invalid_type( json_message):
    return json.dumps({"type": "nope"})

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
        player = create_player(return_string)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_type_not_supplied(self):
        player = create_player(return_invalid_json)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: Not Present"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_not_right_message(self):
        player = create_player(return_invalid_message)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: nope"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_version_is_lower(self):
        def invalid_message( json_message):
            return json.dumps({"type": "player-name-reply", "name": "bot", "version": 0})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Version mismatch: 0"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_version_is_absent(self):
        def invalid_message( json_message):
            return json.dumps({"type": "player-name-reply", "name": "bot"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Version mismatch: Not Present"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_player_number_is_wrong(self):
        def invalid_message( json_message):
            return json.dumps({"type": "player-name-reply", "name": "bot", "version": 1, "player_number": "player1"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Player Number Mismatch: player1"):
            send_player_info(player, 2, 1)

    def test_player_request_aborts_if_player_number_is_absent(self):
        def invalid_message( json_message):
            return json.dumps({"type": "player-name-reply", "name": "bot", "version": 1})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Player Number Mismatch: Not Present"):
            send_player_info(player, 2, 1)

    def test_player_request_auto_fills_name(self):
        def missing_name( json_message):
            return json.dumps({"type": "player-name-reply", "player_number": "player2", "version": 1})

        player = create_player(missing_name)
        send_player_info(player, 2, 1)
        self.assertEquals("PLAYER2", player.name)

    def test_player_supply_message(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        def receive( json_message):
            message = json.loads(json_message)
            self.assertEquals("supply-info", message["type"])
            self.assertEquals(supply.supply, message["cards"])

        player = create_player(receive)
        send_supply_info(player, supply)

    def test_player_can_cleanup(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals("play-turn", message["type"])
            self.assertEquals(["copper", "copper", "copper", "copper", "copper"], message["hand"])
            self.assertEquals(1, message["actions"])
            self.assertEquals(1, message["buys"])
            self.assertEquals(0, message["extra_money"])
            self.assertEquals([], message["cards_played"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               "top-discard" : "copper"
               })
        player = create_player(send_and_respond)
        for _ in range(5):
            player.add_to_hand("copper")
            player.put_card_on_top_of_deck("silver")
        send_turn_request(player)
        self.assertEquals(player.get_discard_pile(), ["copper", "copper", "copper", "copper", "copper"])
        self.assertEquals(player.get_hand(), ["silver", "silver", "silver", "silver", "silver"])

    def test_play_turn_aborts_if_not_json(self):
        player = create_player(return_string)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_turn_request(player)

    def test_play_turn_aborts_if_missing_type(self):
        player = create_player(return_invalid_json)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: Not Present"):
            send_turn_request(player)

    def test_player_request_aborts_if_not_right_message(self):
        player = create_player(return_invalid_type)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: nope"):
            send_turn_request(player)

    def test_player_request_aborts_if_phase_missing(self):
        def invalid_message( json_message):
            return json.dumps({"type": "play-reply"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Invalid Phase: Not Present"):
            send_turn_request(player)

    def test_player_request_aborts_if_phase_is_wrong(self):
        def invalid_message( json_message):
            return json.dumps({"type": "play-reply", "phase" : "nope"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Invalid Phase: nope"):
            send_turn_request(player)

    def test_player_can_specify_top_discard_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals(["silver", "copper", "copper", "copper", "copper", "copper"], message["hand"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               "top_discard" : "silver"
               })
        player = create_player(send_and_respond)
        player.add_to_hand("silver")
        for _ in range(5):
            player.add_to_hand("copper")
            player.put_card_on_top_of_deck("gold")
        send_turn_request(player)
        self.assertEquals("silver", player.get_top_discard_card())

    def test_player_doesnt_have_to_specify_top_discard_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals(["silver", "copper", "copper", "copper", "copper", "copper"], message["hand"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               })
        player = create_player(send_and_respond)
        player.add_to_hand("silver")
        for _ in range(5):
            player.add_to_hand("copper")
            player.put_card_on_top_of_deck("gold")
        send_turn_request(player)
        self.assertTrue( player.get_top_discard_card() in ["copper", "silver"])

    def test_player_can_specify_top_card_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals(["silver", "copper", "copper", "copper", "copper", "copper"], message["hand"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               "top-discard": "gold"
               })
        player = create_player(send_and_respond)
        player.add_to_hand("silver")
        for _ in range(5):
            player.add_to_hand("copper")
            player.put_card_on_top_of_deck("gold")
        send_turn_request(player)
        self.assertTrue( player.get_top_discard_card() in ["copper", "silver"])
