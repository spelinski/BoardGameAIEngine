import json
from dominion.CardInfo import *
from dominion.Identifiers import *
from sys import stdin, stdout
class InteractiveBot(object):

    def __init__(self, num):
        self.num = num
        self.supply_dict = {}

    def get_response(self):
        return json.dumps(self.message)


    def send_message(self, json_message):
        message = json.loads(json_message)
        if message["type"] == "supply-info":
            self.print_message( "Supply: " + ''.join(["{},{} ".format(k,v) for k,v in message["cards"].items()]))
        if message["type"] == "player-name-request":
            self.message =  {"type": "player-name-reply", "player_number": message["player_number"],
                    "name" : "Interactive", "version": 1}
        if message["type"] == "attack-request":
            return {"type": "attack-reply", "discard": message["options"][:message["discards"]]}
        if message["type"] == "play-turn":
            self.print_message("Hand: {} Actions: {} Buys:{} ExtraMoney:{}".format(message["hand"], message["actions"], message["buys"], message["extra_money"]))
            if message["buys"] == 0:
                self.message =  {"type": "play-reply", "phase": "cleanup"}
            else:
                self.wait_for_turn_message(message["hand"])

    def print_message(self, message):
        print "PLAYER {}: {}".format(self.num, message)

    def wait_for_turn_message(self,  hand):
        self.print_message( "Please Play Turn")
        msg = raw_input()
        if msg == "cleanup":
            self.message =  {"type": "play-reply", "phase": "cleanup"}
        if msg == "buy":
            treasures = [card for card in hand if is_treasure(card)]
            self.print_message("Buy Cards with treasures: {}".format(treasures))
            cards = raw_input().split(" ")
            self.message = {"type": "play-reply", "phase": "buy", "played_treasures": treasures, "cards_to_buy" : cards}
        if msg == "action":
            available_actions = [card for card in hand if is_action_card(card)]
            if not available_actions:
                self.message =  {"type": "play-reply", "phase": "cleanup"}
            else:
                self.print_message("Which action card: {}".format(available_actions))
                card = raw_input()
                if card in [SMITHY, MILITIA,WOODCUTTER, MARKET, MOAT, VILLAGE]:
                    self.message = {"type": "play-reply", "phase": "action", "card": card, "additional_parameters": {}}
                if card == MINE:
                    treasures = [t for t in hand if is_treasure(t)]
                    self.print_message("Pick card to trash {}".format(treasures))
                    trash = raw_input()
                    self.print_message("Pick desired card")
                    desired = raw_input()
                    self.message = {"type": "play-reply", "phase": "action", "card": card, "additional_parameters": {"card_to_trash":trash, "desired_card":desired}}
                if card == REMODEL:
                    self.print_message("Pick card to trash {}".format(hand))
                    trash = raw_input()
                    self.print_message("Pick desired card")
                    desired = raw_input()
                    self.message = {"type": "play-reply", "phase": "action", "card": card, "additional_parameters": {"card_to_trash":trash, "desired_card":desired}}
                if card == CELLAR:
                    self.print_message( "CELLAR")
                    self.print_message("Pick cards to discard {}".format(hand))
                    cards = raw_input().split(" ")
                    self.message = {"type": "play-reply", "phase": "action", "card": card, "additional_parameters": {"cards":cards}}
                if card == WORKSHOP:
                    self.print_message("Pick card you want")
                    desired = raw_input()
                    self.message = {"type": "play-reply", "phase": "action", "card": card, "additional_parameters": {"desired_card":desired}}

        if msg == "exit":
            print "Exit"
            exit()

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
>>>>>>> Adding Interactive Bot
