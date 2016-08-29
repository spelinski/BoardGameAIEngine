import unittest
from mock import Mock
from dominion.Identifiers import *
from dominion.engine.DominionEngine import *
from dominion.model.Player import *

class TestDominionEngine(unittest.TestCase):

    def test_game_engine_deals_starting_hand(self):
        player = Player()
        def send_message_and_await_response(json_message):
            message = json.loads(json_message)
            return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                    "name" : "nothing-bot", "version": 1})
        player.send_message_and_await_response = send_message_and_await_response
        player.send_message = lambda msg: None

        players = [player]
        engine = DominionEngine(players, FIRST_GAME)

        self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER, COPPER, COPPER, ESTATE, ESTATE, ESTATE], sorted(player.get_hand() + player.get_deck_cards()))

    def test_game_ends_if_no_player_can_make_a_move(self):
        player = Player()

        def send_message_and_await_response(json_message):
            message = json.loads(json_message)
            if message["type"] == "player-name-request":
                 return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                        "name" : "nothing-bot", "version": 1})
            else:
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player.send_message_and_await_response = send_message_and_await_response
        player.send_message = lambda msg: None

        players = [player]
        engine = DominionEngine(players, FIRST_GAME)
        engine.run_until_game_end()

        self.assertEquals(3, player.get_score())
        self.assertEquals(100, player.get_number_of_turns_taken())

    def test_game_ends_if_invalid_messages(self):
        player = Player()

        def send_message_and_await_response(json_message):
            message = json.loads(json_message)
            if message["type"] == "player-name-request":
                 return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                        "name" : "nothing-bot", "version": 1})
            else:
                return ""
        player.send_message_and_await_response = send_message_and_await_response
        player.send_message = lambda msg: None

        players = [player]
        engine = DominionEngine(players, FIRST_GAME)
        engine.run_until_game_end()

        self.assertEquals(3, player.get_score())
        self.assertEquals(100, player.get_number_of_turns_taken())

    def test_engine_exits_early_if_invalid_response_to_player_name(self):
        player = Player()
        player.send_message_and_await_response = lambda msg: ""
        player.send_message = lambda msg: None

        with self.assertRaisesRegexp(Exception, "Player 1 did not respond correctly"):
            engine = DominionEngine([player], FIRST_GAME)
