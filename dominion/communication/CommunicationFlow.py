from CommandGenerator import *
import json

def send_player_info(player, player_number, version):
    player_info_request = CommandGenerator().create_player_info_request(player_number, version)
    json_response = player.send_message_and_await_response(json.dumps(player_info_request))
    try:
        response = json.loads(json_response)
    except:
        raise Exception("Message was not JSON: {}".format(json_response))
    response_type = response["type"] if "type" in response else "Not Present"
    if response_type != "player-name-reply":
        raise Exception("Message was not correct type: {}".format(response_type))
    response_version = response["version"] if "version" in response else "Not Present"
    if response_version < version or response_version == "Not Present":
        raise Exception("Version mismatch: {}".format(response_version))
    player_number = response["player_number"] if "player_number" in  response else "Not Present"
    if player_number != player_info_request["player_number"]:
        raise Exception("Player Number Mismatch: {} != {}".format(player_info_request["player_number"],player_number))
    player.name = response["name"]
