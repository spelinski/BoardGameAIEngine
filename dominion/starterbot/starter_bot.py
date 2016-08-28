import json
from dominion.CardInfo import *

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
        if message["type"] == "play-turn":
            treasures = [card for card in message["hand"] if is_treasure(card)]
            money = sum(get_worth(treasure) for treasure in treasures)
            available_cards = [card for card,num in self.supply_dict.items() if get_cost(card) <= money and num > 0]
            if not available_cards or message["buys"] == 0:
                self.message =   {"type": "play-reply", "phase": "cleanup"}
            else:
                self.message = {"type": "play-reply", "phase": "buy", "played_treasures": treasures, "cards_to_buy" : [available_cards[0]]}
