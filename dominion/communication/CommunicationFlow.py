from CommandGenerator import *
import json

def send_player_info(player, player_number, version):
    player_info_request = CommandGenerator().create_player_info_request(player_number, version)
    json_response = player.send_message_and_await_response(json.dumps(player_info_request))
    try:
        response = json.loads(json_response)
        player.name = response["name"]
    except:
        raise Exception("Message was not JSON: {}".format(json_response))
