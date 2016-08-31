import unittest
from mock import Mock
from dominion.model.Supply import *
from dominion.model.Player import *
from dominion.Identifiers import *
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

def add_coppers_to_hand_and_silvers_to_deck(player, num_of_coppers):
    for _ in range(num_of_coppers):
        player.add_to_hand(COPPER)
    for _ in range(10):
        player.put_card_on_top_of_deck(SILVER)

class TestCommunicationFlow(unittest.TestCase):

    def setUp(self):
        self.supply = Supply(2, Identifiers.FIRST_GAME)
        self.hit_cleanup = False

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
            self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER], message["hand"])
            self.assertEquals(1, message["actions"])
            self.assertEquals(1, message["buys"])
            self.assertEquals(0, message["extra_money"])
            self.assertEquals([], message["cards_played"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               "top-discard" : COPPER
               })
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 5)
        send_turn_request(player, self.supply)
        self.assertEquals(player.get_discard_pile(), [COPPER, COPPER, COPPER, COPPER, COPPER])
        self.assertEquals(player.get_hand(), [SILVER, SILVER, SILVER, SILVER, SILVER])

    def test_play_turn_aborts_if_not_json(self):
        player = create_player(return_string)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_turn_request(player, self.supply)

    def test_player_cleans_up_on_exception_for_play_turn(self):
        player = create_player(return_string)
        add_coppers_to_hand_and_silvers_to_deck(player, 5)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_turn_request(player, self.supply)
        self.assertEquals([SILVER, SILVER, SILVER, SILVER, SILVER], player.get_hand())
        self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER], player.get_discard_pile())


    def test_play_turn_aborts_if_missing_type(self):
        player = create_player(return_invalid_json)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: Not Present"):
            send_turn_request(player, self.supply)

    def test_player_request_aborts_if_not_right_message(self):
        player = create_player(return_invalid_type)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: nope"):
            send_turn_request(player, self.supply)

    def test_player_request_aborts_if_phase_missing(self):
        def invalid_message( json_message):
            return json.dumps({"type": "play-reply"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Invalid Phase: Not Present"):
            send_turn_request(player, self.supply)

    def test_player_request_aborts_if_phase_is_wrong(self):
        def invalid_message( json_message):
            return json.dumps({"type": "play-reply", "phase" : "nope"})

        player = create_player(invalid_message)
        with self.assertRaisesRegexp(Exception, "Invalid Phase: nope"):
            send_turn_request(player, self.supply)

    def test_player_can_specify_top_discard_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals([SILVER, COPPER, COPPER, COPPER, COPPER, COPPER], message["hand"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               "top_discard" : SILVER
               })
        player = create_player(send_and_respond)
        player.add_to_hand(SILVER)
        add_coppers_to_hand_and_silvers_to_deck(player, 5)
        send_turn_request(player, self.supply)
        self.assertEquals(SILVER, player.get_top_discard_card())

    def test_player_doesnt_have_to_specify_top_discard_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals([SILVER, COPPER, COPPER, COPPER, COPPER, COPPER], message["hand"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               })
        player = create_player(send_and_respond)
        player.add_to_hand(SILVER)
        add_coppers_to_hand_and_silvers_to_deck(player, 5)
        send_turn_request(player, self.supply)
        self.assertTrue( player.get_top_discard_card() in [COPPER, SILVER])

    def test_player_can_specify_top_card_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals([SILVER, COPPER, COPPER, COPPER, COPPER, COPPER], message["hand"])
            return json.dumps({
               "type": "play-reply",
               "phase": "cleanup",
               "top-discard": GOLD
               })
        player = create_player(send_and_respond)
        player.add_to_hand(SILVER)
        add_coppers_to_hand_and_silvers_to_deck(player, 5)
        send_turn_request(player, self.supply)
        self.assertTrue( player.get_top_discard_card() in [COPPER, SILVER])

    def test_player_can_buy_cards(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                self.assertEquals([], message["cards_played"])
                self.assertEquals(message["cards_gained"], [COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "cards_to_buy": [COPPER]})
        player = create_player(send_and_respond)
        self.assertEqual(60, self.supply.get_number_of_cards(COPPER))

        send_turn_request(player, self.supply)
        self.assertEqual([COPPER], player.get_hand())
        self.assertEqual(59, self.supply.get_number_of_cards(COPPER))
        self.assertTrue(self.hit_cleanup)


    def test_player_no_buy_cards_skips_buy(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy"})
        player = create_player(send_and_respond)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)

    def test_player_empty_buy_cards_skips_buy(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                self.assertEquals([], message["cards_played"])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "cards_to_buy": []})
        player = create_player(send_and_respond)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)


    def test_player_can_buy_card_worth_money(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                self.assertEquals([COPPER, COPPER], message["cards_played"])
                self.assertEquals(message["cards_gained"], [MOAT])
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.MOAT]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([MOAT, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_put_bought_card_as_top(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : MOAT})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.MOAT]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply)
        self.assertEquals(COPPER, player.get_top_discard_card())

    def test_player_buy_is_consumed_if_card_not_in_supply(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "cards_to_buy": [Identifiers.FEAST]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 5)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_buy_is_consumed_if_card_costs_too_much(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.SILVER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())

    def test_player_can_buy_more_expensive_card_with_extra_money(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                self.assertEquals(message["cards_gained"], [SILVER])
                self.assertEquals(message["cards_played"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.SILVER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, extra_money=1)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_can_buy_multiple_cards_if_multiple_buys(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                self.assertEquals(message["cards_gained"], [SILVER, COPPER])
                self.assertEquals(message["cards_played"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [SILVER, COPPER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_not_enough_buys(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.SILVER, Identifiers.COPPER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, extra_money=1)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_with_zero_buys(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.COPPER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        with self.assertRaisesRegexp(Exception, "Player did not have any more buys"):
            send_turn_request(player, self.supply, buys=0)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_invalid_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.SILVER, Identifiers.FEAST]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_supply_empty(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.SILVER, Identifiers.COPPER]})
        for _ in range(60):
            self.supply.take(COPPER)
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_not_supply_empty(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.SILVER, Identifiers.COPPER]})
        for _ in range(60):
            self.supply.take(COPPER)
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())


    def test_player_cant_buy_if_game_ends(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup", "top_discard" : COPPER})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER], "cards_to_buy": [Identifiers.VILLAGE, Identifiers.COPPER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        for _ in range(10):
            self.supply.take(MOAT)
            self.supply.take(MARKET)
        for _ in range(9):
            self.supply.take(VILLAGE)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([VILLAGE, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_with_treasures_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [SILVER], "cards_to_buy": [Identifiers.COPPER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply, buys=1)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_cant_buy_with_non_treasures(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "buy", "played_treasures": [COPPER, COPPER, MOAT], "cards_to_buy": [Identifiers.COPPER]})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, buys=1)
        self.assertEquals([MOAT, COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_cant_play_action_with_zero_actions(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            return json.dumps({"type": "play-reply", "phase": "action", "card": MOAT, "additional_parameters": {}})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        with self.assertRaisesRegexp(Exception, "Player did not have any more actions"):
            send_turn_request(player, self.supply, actions=0)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())

    def test_player_action_is_consumed_if_card_not_present(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "action"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_action_is_consumed_if_card_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 0:
                self.hit_cleanup = True
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MOAT})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_moat(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 0:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MOAT])
                self.assertEqual(message["hand"], [COPPER, COPPER, SILVER, SILVER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
            else:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MOAT})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MOAT)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, SILVER, SILVER, MOAT], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_market(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if MARKET in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": MARKET})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MARKET])
                self.assertEqual(2, message["buys"])
                self.assertEqual(1, message["actions"])
                self.assertEqual(1, message["extra_money"])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MARKET)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, SILVER, MARKET], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_smithy(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if SMITHY in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": SMITHY})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [SMITHY])
                self.assertEqual(message["hand"], [COPPER, COPPER, SILVER, SILVER, SILVER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(SMITHY)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, SILVER, SILVER, SILVER,SMITHY], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)
