class Supply(object):
    def __init__(self, number_of_players, set):
        self.supply = self.create_supply(number_of_players, set)

    def create_supply(self, number_of_players, set):
        kingdom_cards = ["Cellar", "Market", "Militia", "Mine", "Moat", "Remodel", "Smithy", "Village", "Woodcutter", "Workshop"]
        return {"kingdom": {card:10 for card in kingdom_cards},
                "treasure": {"Copper": 60, "Silver" : 40, "Gold" : 30},
                "victory": {card:_get_victory_card_count(number_of_players) for card in ["Estate", "Duchy", "Province"]},
                "curse" : _get_curse_card_count(number_of_players)
                }

    def get_number_of_kingdom_cards(self, card):
        return self.supply["kingdom"][card]

    def get_number_of_treasure_cards(self, card):
        return self.supply["treasure"][card]

    def get_number_of_victory_cards(self, card):
        return self.supply["victory"][card]

    def get_number_of_curse_cards(self):
        return self.supply["curse"]

def _get_victory_card_count(number_of_players):
    return 8 if number_of_players == 2 else 12

def _get_curse_card_count(number_of_players):
    return (number_of_players - 1) * 10
