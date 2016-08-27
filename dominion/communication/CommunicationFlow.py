from CommandGenerator import *
import json

def send_player_info(player, player_number, version):
    player_info_request = CommandGenerator().create_player_info_request(player_number, version)
    json_response = player.send_message_and_await_response(json.dumps(player_info_request))
    response = __get_json_message(json_response)
    __assert_message_type_is_correct(response, "player-name-reply")
    __assert_field_matches(response, "version", lambda v: v >= version, "Version mismatch")
    __assert_field_matches(response, "player_number", lambda p: p == player_info_request["player_number"], "Player Number Mismatch")
    player.name = response.get("name", player_info_request["player_number"].upper())

def send_supply_info(player, supply):
    supply_info_message = CommandGenerator().create_supply_info_message(supply.supply)
    player.send_message(json.dumps(supply_info_message))

def send_turn_request(player, actions=1, buys=1, extra_money=0):
    play_turn_request = CommandGenerator().create_play_turn_request(actions, buys, extra_money, player.hand, [])
    json_response = player.send_message_and_await_response(json.dumps(play_turn_request))
    response = __get_json_message(json_response)
    __assert_message_type_is_correct(response, "play-reply")
    __assert_field_matches(response, "phase", lambda p: p == "cleanup", "Invalid Phase")
    top_discard = response.get("top_discard", "")
    player.cleanup(top_discard)
    player.draw_cards(5)

def __get_json_message(json_response):
    try:
        return json.loads(json_response)
    except:
        raise Exception("Message was not JSON: {}".format(json_response))

def __assert_message_type_is_correct(response, expected):
    __assert_field_matches(response, "type", lambda t: t == expected, "Message was not correct type")

def __assert_field_matches(response, field, matcher_func, exception_text):
    value = response[field] if field in response else "Not Present"
    if not matcher_func(value) or value == "Not Present":
        raise Exception("{}: {}".format(exception_text, value))
