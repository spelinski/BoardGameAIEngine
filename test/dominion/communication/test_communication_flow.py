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

def create_player_with_deck(func, num_of_coppers_in_hand=5, additional_hand_cards=[]):
    player = create_player(func)
    add_coppers_to_hand_and_silvers_to_deck(player, num_of_coppers_in_hand, additional_hand_cards)
    return player

def return_string(json_message):
    return "nope"

def return_invalid_json(json_message):
    return json.dumps({})

def return_invalid_type( json_message):
    return json.dumps({"type": "nope"})

def add_coppers_to_hand_and_silvers_to_deck(player, num_of_coppers, additional_hand_cards=[]):
    for _ in range(num_of_coppers):
        player.add_to_hand(COPPER)
    for card in additional_hand_cards:
        player.add_to_hand(card)
    for _ in range(10):
        player.put_card_on_top_of_deck(SILVER)

def reply_with_player_name(json_message):
        message = json.loads(json_message)
        assert "player-name-request" == message["type"]
        return json.dumps({
                 "type": "player-name-reply",
                 "player_number": message["player_number"],
                 "name": "test-bot",
                 "version": message["version"]
                })

def make_response_function(dictionary):
    def respond(json_message):
        return json.dumps(dictionary)
    return respond

def cleanup_message(top_discard=None):
    d = {
       "type": "play-reply",
       "phase": "cleanup"
       }
    if top_discard:
        d["top_discard"] = top_discard
    return json.dumps(d)


class TestCommunicationFlow(unittest.TestCase):

    def setUp(self):
        self.supply = Supply(2, Identifiers.FIRST_GAME)
        self.hit_cleanup = False

    def empty_supply(self, card):
        while self.supply.get_number_of_cards(card) > 0:
            self.supply.take(card)

    def test_can_handle_player_request(self):
        player = create_player_with_deck(reply_with_player_name)
        send_player_info(player, 1, 1)
        self.assertEquals("test-bot", player.name)

    def test_player_request_aborts_if_not_json(self):
        player = create_player_with_deck(return_string)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_type_not_supplied(self):
        player = create_player_with_deck(return_invalid_json)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: Not Present"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_not_right_message(self):
        player = create_player_with_deck(return_invalid_response)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: nope"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_version_is_lower(self):
        invalid_response = make_response_function({"type": "player-name-reply", "name": "bot", "version": 0})
        player = create_player_with_deck(invalid_response)
        with self.assertRaisesRegexp(Exception, "Version mismatch: 0"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_version_is_absent(self):
        invalid_response = make_response_function({"type": "player-name-reply", "name": "bot"})
        player = create_player_with_deck(invalid_response)
        with self.assertRaisesRegexp(Exception, "Version mismatch: Not Present"):
            send_player_info(player, 1, 1)

    def test_player_request_aborts_if_player_number_is_wrong(self):
        invalid_response = make_response_function({"type": "player-name-reply", "name": "bot", "version": 1, "player_number": "player1"})
        player = create_player_with_deck(invalid_response)
        with self.assertRaisesRegexp(Exception, "Player Number Mismatch: player1"):
            send_player_info(player, 2, 1)

    def test_player_request_aborts_if_player_number_is_absent(self):
        invalid_response = make_response_function({"type": "player-name-reply", "name": "bot", "version": 1})
        player = create_player_with_deck(invalid_response)
        with self.assertRaisesRegexp(Exception, "Player Number Mismatch: Not Present"):
            send_player_info(player, 2, 1)

    def test_player_request_auto_fills_name(self):
        missing_name = make_response_function({"type": "player-name-reply", "player_number": "player2", "version": 1})
        player = create_player_with_deck(missing_name)
        send_player_info(player, 2, 1)
        self.assertEquals("PLAYER2", player.name)

    def test_player_supply_message(self):
        supply = Supply(2, Identifiers.FIRST_GAME)
        def receive( json_message):
            message = json.loads(json_message)
            self.assertEquals("supply-info", message["type"])
            self.assertEquals(supply.supply, message["cards"])

        player = create_player_with_deck(receive)
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
            return cleanup_message(COPPER)
        player = create_player_with_deck(send_and_respond)
        send_turn_request(player, self.supply)
        self.assertEquals(player.get_discard_pile(), [COPPER, COPPER, COPPER, COPPER, COPPER])
        self.assertEquals(player.get_hand(), [SILVER, SILVER, SILVER, SILVER, SILVER])

    def test_play_turn_aborts_if_not_json(self):
        player = create_player_with_deck(return_string)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_turn_request(player, self.supply)

    def test_player_cleans_up_on_exception_for_play_turn(self):
        player = create_player_with_deck(return_string)
        with self.assertRaisesRegexp(Exception, "Message was not JSON: nope"):
            send_turn_request(player, self.supply)
        self.assertEquals([SILVER, SILVER, SILVER, SILVER, SILVER], player.get_hand())
        self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER], player.get_discard_pile())


    def test_play_turn_aborts_if_missing_type(self):
        player = create_player_with_deck(return_invalid_json)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: Not Present"):
            send_turn_request(player, self.supply)

    def test_player_request_aborts_if_not_right_message(self):
        player = create_player_with_deck(return_invalid_type)
        with self.assertRaisesRegexp(Exception, "Message was not correct type: nope"):
            send_turn_request(player, self.supply)

    def test_player_request_aborts_if_phase_missing(self):
        invalid_response=make_response_function({"type": "play-reply"})
        player = create_player_with_deck(invalid_response)
        with self.assertRaisesRegexp(Exception, "Invalid Phase: Not Present"):
            send_turn_request(player, self.supply)

    def test_player_request_aborts_if_phase_is_wrong(self):
        invalid_response=make_response_function({"type": "play-reply", "phase" : "nope"})
        player = create_player_with_deck(invalid_response)
        with self.assertRaisesRegexp(Exception, "Invalid Phase: nope"):
            send_turn_request(player, self.supply)

    def cleanup_with_expected_hand_check(self, expected_hand, top_discard = None):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            self.assertEquals(expected_hand, message["hand"])
            return cleanup_message(top_discard)
        return send_and_respond

    def test_player_can_specify_top_discard_card(self):
        cleanup_func = self.cleanup_with_expected_hand_check([COPPER, COPPER, COPPER, COPPER, COPPER, SILVER, GOLD], SILVER)
        player = create_player_with_deck(cleanup_func, additional_hand_cards= [SILVER, GOLD])
        send_turn_request(player, self.supply)
        self.assertEquals(SILVER, player.get_top_discard_card())

    def test_player_doesnt_have_to_specify_top_discard_card(self):
        cleanup_func = self.cleanup_with_expected_hand_check([COPPER, COPPER, COPPER, COPPER, COPPER, SILVER, GOLD])
        player = create_player_with_deck(cleanup_func, additional_hand_cards= [SILVER, GOLD])
        send_turn_request(player, self.supply)
        self.assertTrue( player.get_top_discard_card() in [COPPER, SILVER,GOLD])

    def test_player_can_specify_top_card_not_in_hand(self):
        cleanup_func = self.cleanup_with_expected_hand_check([COPPER, COPPER, COPPER, COPPER, COPPER, SILVER], GOLD)
        player = create_player_with_deck(cleanup_func, additional_hand_cards= [SILVER])
        send_turn_request(player, self.supply)
        self.assertTrue( player.get_top_discard_card() in [COPPER, SILVER])

    def general_cleanup_function(self, message, expected_cards_played=[], expected_cards_gained=[], top_discard = None, expected_hand=None):
        self.hit_cleanup = True
        self.assertEquals(expected_cards_played, message["cards_played"])
        self.assertEquals(expected_cards_gained, message["cards_gained"])
        if expected_hand is not None:
            self.assertEquals(expected_hand, message["hand"])
        return cleanup_message(top_discard)

    def get_buy_message(self, cards_to_buy=None, played_treasures=None):
        buy_message = {"type": "play-reply", "phase": "buy"}
        if cards_to_buy:
            buy_message["cards_to_buy"] = cards_to_buy
        if played_treasures:
            buy_message["played_treasures"] = played_treasures
        return json.dumps(buy_message)

    def create_buy_response(self, cards_to_buy=None, played_treasures=None, expected_cards_played=[], expected_cards_gained=[], top_discard=None):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["buys"] == 0:
                return self.general_cleanup_function(message, expected_cards_gained=expected_cards_gained, expected_cards_played=expected_cards_played, top_discard=top_discard)
            else:
                return self.get_buy_message(cards_to_buy, played_treasures)
        return send_and_respond

    def test_player_can_buy_cards(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [COPPER], expected_cards_gained=[COPPER])
        player = create_player_with_deck(buy_response_func)
        self.assertEqual(60, self.supply.get_number_of_cards(COPPER))
        send_turn_request(player, self.supply)
        self.assertEqual([COPPER, COPPER,COPPER, COPPER, COPPER, COPPER], player.get_discard_pile())
        self.assertEqual(59, self.supply.get_number_of_cards(COPPER))
        self.assertTrue(self.hit_cleanup)

    def test_player_no_buy_cards_skips_buy(self):
        buy_response_func = self.create_buy_response()
        player = create_player_with_deck(buy_response_func)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)

    def test_player_empty_buy_cards_skips_buy(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [])
        player = create_player_with_deck(buy_response_func)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)

    def test_player_can_buy_card_worth_money(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [MOAT], expected_cards_gained=[MOAT], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], top_discard=COPPER)
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([MOAT, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_put_bought_card_as_top(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [MOAT], expected_cards_gained=[MOAT], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], top_discard=MOAT)
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply)
        self.assertEquals(COPPER, player.get_top_discard_card())

    def test_player_buy_is_consumed_if_card_not_in_supply(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [FEAST], played_treasures=[COPPER, COPPER, COPPER,COPPER], expected_cards_played=[COPPER, COPPER,COPPER,COPPER])
        player = create_player_with_deck(buy_response_func)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_buy_is_consumed_if_card_costs_too_much(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [SILVER], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER])
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())

    def test_player_can_buy_more_expensive_card_with_extra_money(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [SILVER], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], expected_cards_gained=[SILVER])
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply, extra_money=1)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_can_buy_multiple_cards_if_multiple_buys(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [SILVER, COPPER], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], expected_cards_gained=[SILVER, COPPER])
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_not_enough_buys(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [SILVER, COPPER], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], expected_cards_gained=[SILVER])
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply, extra_money=1)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_with_zero_buys(self):
        def send_and_respond(json_message):
            return  self.get_buy_message([COPPER], [COPPER, COPPER])
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        with self.assertRaisesRegexp(Exception, "Player did not have any more buys"):
            send_turn_request(player, self.supply, buys=0)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_invalid_card(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [SILVER, FEAST], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], expected_cards_gained=[SILVER])
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_multiple_cards_if_supply_empty(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [SILVER, COPPER], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], expected_cards_gained=[SILVER])
        player = create_player_with_deck(buy_response_func, 2)
        self.empty_supply(COPPER)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([SILVER, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_if_game_ends(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [VILLAGE, COPPER], played_treasures=[COPPER, COPPER], expected_cards_played=[COPPER, COPPER], expected_cards_gained=[VILLAGE])
        player = create_player_with_deck(buy_response_func, 2)
        self.empty_supply(MOAT)
        self.empty_supply(MARKET)
        for _ in range(9):
            self.supply.take(VILLAGE)
        send_turn_request(player, self.supply, extra_money=1, buys=2)
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([VILLAGE, COPPER, COPPER], player.get_discard_pile())

    def test_player_cant_buy_with_treasures_not_in_hand(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [ COPPER], played_treasures=[SILVER])
        player = create_player_with_deck(buy_response_func, 2)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_cant_buy_with_non_treasures(self):
        buy_response_func = self.create_buy_response(cards_to_buy = [ COPPER], played_treasures=[COPPER, COPPER, MOAT], expected_cards_played=[COPPER,COPPER])
        player = create_player_with_deck(buy_response_func, 2, additional_hand_cards=[MOAT])
        send_turn_request(player, self.supply, buys=1)
        self.assertEquals([MOAT, COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def create_action_message(self, card=None, additional_parameters={}):
        message =  {"type": "play-reply", "phase": "action", "additional_parameters": additional_parameters}
        if card:
            message["card"] = card
        return json.dumps(message)

    def get_action_response_function(self, card=None, additional_parameters={}, expected_hand=None, expected_cards_played=[]):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 0:
                return self.general_cleanup_function(message, expected_cards_played=expected_cards_played, expected_hand=expected_hand)
            else:
                return self.create_action_message(card, additional_parameters)
        return send_and_respond


    def test_player_cant_play_action_with_zero_actions(self):
        def send_and_respond(json_message):
            return self.create_action_message(MOAT)
        player = create_player_with_deck(send_and_respond, 2)
        with self.assertRaisesRegexp(Exception, "Player did not have any more actions"):
            send_turn_request(player, self.supply, actions=0)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())

    def test_player_action_is_consumed_if_card_not_present(self):
        action_response_func = self.get_action_response_function()
        player = create_player_with_deck(action_response_func, 2)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_player_action_is_consumed_if_card_not_in_hand(self):
        action_response_func = self.get_action_response_function(MOAT)
        player = create_player_with_deck(action_response_func, 2)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_moat(self):
        action_response_func = self.get_action_response_function(MOAT, expected_hand=[COPPER, COPPER, SILVER, SILVER], expected_cards_played=[MOAT])
        player = create_player_with_deck(action_response_func, 2, additional_hand_cards=[MOAT])
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

    def test_can_play_village(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if VILLAGE in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": VILLAGE})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 2)
                self.assertEqual(message["cards_played"], [VILLAGE])
                self.assertEqual(message["hand"], [COPPER, COPPER, SILVER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(VILLAGE)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, SILVER, VILLAGE], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_woodcutter(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if WOODCUTTER in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": WOODCUTTER})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["buys"], 2)
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["cards_played"], [WOODCUTTER])
                self.assertEqual(message["hand"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(WOODCUTTER)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, WOODCUTTER], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_cellar(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if CELLAR in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": CELLAR, "additional_parameters": {"cards": [COPPER]}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 1)
                self.assertEqual(message["cards_played"], [CELLAR])
                self.assertEqual(message["hand"], [COPPER, SILVER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(CELLAR)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, SILVER, CELLAR], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_cellar_without_specifying_Cards(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if CELLAR in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": CELLAR})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 1)
                self.assertEqual(message["cards_played"], [CELLAR])
                self.assertEqual(message["hand"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(CELLAR)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, CELLAR], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_cellar_without_specifying_cards_2(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if CELLAR in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": CELLAR, "additional_parameters": {}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 1)
                self.assertEqual(message["cards_played"], [CELLAR])
                self.assertEqual(message["hand"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(CELLAR)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, CELLAR], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_cellar_without_specifying_cards_valid_cards(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if CELLAR in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": CELLAR, "additional_parameters": ""})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 1)
                self.assertEqual(message["cards_played"], [CELLAR])
                self.assertEqual(message["hand"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(CELLAR)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, CELLAR], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_cellar_without_specifying_no_cards_in_dict(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if CELLAR in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": CELLAR, "additional_parameters": {"cards": []}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 1)
                self.assertEqual(message["cards_played"], [CELLAR])
                self.assertEqual(message["hand"], [COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(CELLAR)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, CELLAR], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)


    def test_can_play_cellar_specifying_multiple_cards_stops_at_first_non_hand_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if CELLAR in player.get_hand():
                return json.dumps({"type": "play-reply", "phase": "action", "card": CELLAR, "additional_parameters": {"cards": [COPPER, COPPER, MOAT]}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["actions"], 1)
                self.assertEqual(message["cards_played"], [CELLAR])
                self.assertEqual(message["hand"], [SILVER, SILVER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(CELLAR)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, SILVER, SILVER, CELLAR], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_can_play_workshop(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": WORKSHOP, "additional_parameters": {"desired_card": SMITHY}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [WORKSHOP])
                self.assertEqual(message["hand"], [COPPER, COPPER])
                self.assertEqual(message["cards_gained"], [SMITHY])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(WORKSHOP)
        send_turn_request(player, self.supply)
        self.assertEquals([SMITHY,COPPER, COPPER, WORKSHOP], player.get_discard_pile())
        self.assertEquals(9, self.supply.get_number_of_cards(SMITHY))
        self.assertTrue(self.hit_cleanup)

    def test_workshop_doesnt_gain_if_card_empty(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": WORKSHOP, "additional_parameters": {}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER,WORKSHOP])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(WORKSHOP)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, WORKSHOP], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_workshop_doesnt_gain_if_card_not_in_supply(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": WORKSHOP, "additional_parameters": {"desired_card": FEAST}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, WORKSHOP])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(WORKSHOP)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, WORKSHOP], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_cant_use_workshop_for_card_more_expensive_than_4(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": WORKSHOP, "additional_parameters": {"desired_card": MARKET}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER,WORKSHOP])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(WORKSHOP)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, WORKSHOP], player.get_discard_pile())
        self.assertEquals(10, self.supply.get_number_of_cards(MARKET))
        self.assertTrue(self.hit_cleanup)

    def test_can_play_remodel(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": REMODEL, "additional_parameters": {"card_to_trash": COPPER, "desired_card": MOAT}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [REMODEL])
                self.assertEqual(message["hand"], [COPPER])
                self.assertEqual(message["cards_gained"], [MOAT])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(REMODEL)
        send_turn_request(player, self.supply)
        self.assertEquals([MOAT, COPPER, REMODEL], player.get_discard_pile())
        self.assertEquals(9, self.supply.get_number_of_cards(MOAT))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_remodel_if_no_desired_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": REMODEL, "additional_parameters": { "card_to_trash": COPPER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, REMODEL])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(REMODEL)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, REMODEL], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_remodel_if_desired_card_is_too_high(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": REMODEL, "additional_parameters": { "card_to_trash": COPPER, "desired_card": VILLAGE}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER,REMODEL])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(REMODEL)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, REMODEL], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_remodel_if_desired_card_supply_is_empty(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": REMODEL, "additional_parameters": { "card_to_trash": COPPER, "desired_card": ESTATE}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER,REMODEL])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        for _ in range(14):
            self.supply.take(ESTATE)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(REMODEL)
        send_turn_request(player, self.supply)
        self.assertEquals([COPPER, COPPER, REMODEL], player.get_discard_pile())
        self.assertEquals(10, self.supply.get_number_of_cards(MOAT))
        self.assertTrue(self.hit_cleanup)

    def test_can_play_mine(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": {"card_to_trash": COPPER, "desired_card": SILVER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MINE])
                self.assertEqual(message["hand"], [COPPER, SILVER])
                self.assertEqual(message["cards_gained"], [SILVER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, SILVER, MINE], player.get_discard_pile())
        self.assertEquals(39, self.supply.get_number_of_cards(SILVER))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_no_trashed_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "desired_card": SILVER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE], player.get_discard_pile())
        self.assertEquals(40, self.supply.get_number_of_cards(SILVER))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_no_desired_card(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "card_to_trash": COPPER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE], player.get_discard_pile())
        self.assertEquals(40, self.supply.get_number_of_cards(SILVER))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_card_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "card_to_trash": SILVER, "desired_card": SILVER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE], player.get_discard_pile())
        self.assertEquals(40, self.supply.get_number_of_cards(SILVER))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_card_too_expensive(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "card_to_trash": COPPER, "desired_card": GOLD}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE], player.get_discard_pile())
        self.assertEquals(40, self.supply.get_number_of_cards(SILVER))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_supply_empty(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "card_to_trash": COPPER, "desired_card": SILVER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        for _ in range(40):
            self.supply.take(SILVER)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE], player.get_discard_pile())
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_not_playing_treasure(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "card_to_trash": MOAT, "desired_card": SILVER}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE, MOAT])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        player.add_to_hand(MOAT)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE, MOAT], player.get_discard_pile())
        self.assertEquals(40, self.supply.get_number_of_cards(SILVER))
        self.assertTrue(self.hit_cleanup)

    def test_cant_play_mine_if_not_gaining_treasure(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MINE, "additional_parameters": { "card_to_trash": COPPER, "desired_card": CELLAR}})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [])
                self.assertEqual(message["hand"], [COPPER, COPPER, MINE])
                self.assertEqual(message["cards_gained"], [])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 2)
        player.add_to_hand(MINE)
        send_turn_request(player, self.supply)
        self.assertEquals([ COPPER, COPPER, MINE], player.get_discard_pile())
        self.assertEquals(10, self.supply.get_number_of_cards(CELLAR))
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER], message["options"])
                return json.dumps({"type": "attack-reply", "discard": [COPPER, COPPER]})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 5)
        player.add_to_hand(MILITIA)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, COPPER], other_player.get_hand())
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia_other_players_may_chose_discard(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply", "discard": [COPPER, MOAT]})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, COPPER], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, MOAT], other_player.get_discard_pile() )

    def test_can_play_militia_other_players_cant_pick_cards_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply", "discard": [SILVER, MOAT]})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )

    def test_can_play_militia_other_players_engine_chooses_if_invalid_mesage(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-replys"})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )

    def test_can_play_militia_other_players_engine_chooses_if_invalid_mesage2(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply"})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )

    def test_can_play_militia_other_players_engine_chooses_if_invalid_mesage3(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply", "discard": ""})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )

    def test_can_play_militia_other_players_engine_chooses_if_not_enough_cards(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply", "discard": [COPPER]})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )

    def test_can_play_militia_other_players_engine_chooses_if_too_enough_cards(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply", "discard": [COPPER, COPPER, COPPER]})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertTrue(self.hit_cleanup)
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )

    def test_can_play_militia_when_other_player_has_4(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(1,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER], message["options"])
                return json.dumps({"type": "attack-reply", "discard": [COPPER]})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, COPPER], other_player.get_hand())
        self.assertEquals([COPPER], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia_when_other_player_has_3_skips_request(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.fail()
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 3)
        player.add_to_hand(MILITIA)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, COPPER], other_player.get_hand())
        self.assertEquals([], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia_can_be_blocked_by_moat(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply-reaction", "reaction": MOAT})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertEquals([], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia_cant_use_moat_if_not_in_hand(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(1,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER], message["options"])
                return json.dumps({"type": "attack-reply-reaction", "reaction": MOAT})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, COPPER], other_player.get_hand())
        self.assertEquals([COPPER], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia_cant_use_moat_if_invalid_response(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply-reaction"})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)

    def test_can_play_militia_cant_use_moat_if_invalid_response2(self):
        def send_and_respond(json_message):
            message = json.loads(json_message)
            if message["type"] == "attack-request":
                self.assertEqual(2,message["discard"])
                self.assertEquals([COPPER, COPPER, COPPER, COPPER, MOAT], message["options"])
                return json.dumps({"type": "attack-reply-reaction", "reaction": COPPER})
            if message["actions"] == 1:
                return json.dumps({"type": "play-reply", "phase": "action", "card": MILITIA})
            else:
                self.hit_cleanup = True
                self.assertEqual(message["cards_played"], [MILITIA])
                self.assertEqual(message["extra_money"], 2)
                self.assertEqual(message["hand"], [COPPER, COPPER, COPPER, COPPER])
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player = create_player(send_and_respond)
        other_player = create_player(send_and_respond)
        add_coppers_to_hand_and_silvers_to_deck(player, 4)
        add_coppers_to_hand_and_silvers_to_deck(other_player, 4)
        player.add_to_hand(MILITIA)
        other_player.add_to_hand(MOAT)
        send_turn_request(player, self.supply, other_players=[other_player])
        self.assertEquals([ COPPER, COPPER, COPPER, COPPER, MILITIA], player.get_discard_pile())
        self.assertEquals([COPPER, COPPER, MOAT], other_player.get_hand())
        self.assertEquals([COPPER, COPPER], other_player.get_discard_pile() )
        self.assertTrue(self.hit_cleanup)
