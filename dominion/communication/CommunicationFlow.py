from CommandGenerator import *
import json

def send_player_info(player, player_number, version):
    player_info_request = CommandGenerator().create_player_info_request(player_number, version)
    json_response = player.send_message_and_await_response(json.dumps(player_info_request))
    response = __get_json_message(json_response)
    __assert_message_type_is_correct(response, "player-name-reply")
    response_version = response["version"] if "version" in response else "Not Present"
    if response_version < version or response_version == "Not Present":
        raise Exception("Version mismatch: {}".format(response_version))
    player_number = response["player_number"] if "player_number" in  response else "Not Present"
    if player_number != player_info_request["player_number"]:
        raise Exception("Player Number Mismatch: {} != {}".format(player_info_request["player_number"],player_number))
    player.name = response["name"] if "name" in response else player_info_request["player_number"].upper()

def send_supply_info(player, supply):
    supply_info_message = CommandGenerator().create_supply_info_message(supply.supply)
    player.send_message(json.dumps(supply_info_message))

def send_turn_request(player, actions=1, buys=1, extra_money=0):
    play_turn_request = CommandGenerator().create_play_turn_request(actions, buys, extra_money, player.hand, [])
    json_response = player.send_message_and_await_response(json.dumps(play_turn_request))
    response = __get_json_message(json_response)
    __assert_message_type_is_correct(response, "play-reply")
    player.cleanup()
    player.draw_cards(5)

def __get_json_message(json_response):
    try:
        return json.loads(json_response)
    except:
        raise Exception("Message was not JSON: {}".format(json_response))

def __assert_message_type_is_correct(response, expected):
    response_type = response["type"] if "type" in response else "Not Present"
    if response_type != expected:
        raise Exception("Message was not correct type: {}".format(response_type))
