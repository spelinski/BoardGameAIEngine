import json
from dominion.CardInfo import *
from sys import stdin, stdout
class StarterBot(object):

    def __init__(self):
        self.supply_dict = {}

    def get_response(self):
        return json.dumps(self.message)


    def send_message(self, json_message):
        self.message= ""
        message = json.loads(json_message)
        if message["type"] == "supply-info":
            self.supply_dict = message["cards"]
        if message["type"] == "player-name-request":
            self.message =  {"type": "player-name-reply", "player_number": message["player_number"],
                    "name" : "starter-bot", "version": 1}
        if message["type"] == "attack-request":
            return {"type": "attack-reply", "discard": message["options"][:message["discards"]]}
        if message["type"] == "play-turn":
            treasures = [card for card in message["hand"] if is_treasure(card)]
            money = sum(get_worth(treasure) for treasure in treasures)
            available_cards = [card for card,num in self.supply_dict.items() if get_cost(card) <= money and num > 0]
            if not available_cards or message["buys"] == 0:
                self.message =   {"type": "play-reply", "phase": "cleanup"}
            else:
                self.message = {"type": "play-reply", "phase": "buy", "played_treasures": treasures, "cards_to_buy" : [available_cards[0]]}


if __name__ == "__main__":
    bot = StarterBot()
    while not stdin.closed:
        message = stdin.readline().strip()
        if len(message) == 0:
            continue
        bot.send_message(message)
        if bot.message:
            stdout.write(bot.get_response() + "\n")
            stdout.flush()
