import json

class StarterBot(object):

    def __init__(self):
        self.supply_dict = {}

    def send_and_respond(self, json_message):
        message = json.loads(json_message)
        if message["type"] == "player-name-request":
            return {"type": "player-name-reply", "player_number": message["player_number"],
                    "name" : "starter-bot", "version": 1}
        else:
            return {"type": "play-reply", "phase": "cleanup"}

    def send(self, json_message):
        if message["type"] == "supply-info":
            self.supply_dict = message["cards"]
