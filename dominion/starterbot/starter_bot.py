import json

class StarterBot(object):

    def __init__(self):
        self.supply_dict = {}

    def get_response(self):
        return json.dumps(self.message)


    def send_message(self, json_message):
        message = json.loads(json_message)
        if message["type"] == "supply-info":
            self.supply_dict = message["cards"]
        if message["type"] == "player-name-request":
            self.message =  {"type": "player-name-reply", "player_number": message["player_number"],
                    "name" : "starter-bot", "version": 1}
        else:
            self.message =  {"type": "play-reply", "phase": "cleanup"}
