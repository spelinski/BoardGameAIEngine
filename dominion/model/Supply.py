class Supply(object):
    def __init__(self, number_of_players, set):
        self.supply = self.__create_supply(number_of_players, set)

    def __create_supply(self, number_of_players, set):
        kingdom_cards = ["Cellar", "Market", "Militia", "Mine", "Moat", "Remodel", "Smithy", "Village", "Woodcutter", "Workshop"]
        other_supply_cards = ["Copper", "Silver", "Gold", "Estate", "Duchy", "Province", "Curse"]
        cards = kingdom_cards + other_supply_cards
        return  {card: self.__get_initial_number_of_cards(card, number_of_players) for card in cards}

    def __get_initial_number_of_cards(self, card, number_of_players):
        if self.__is_victory_card(card):
            return self.__get_victory_card_count(card, number_of_players)
        elif card == "Curse":
            return self.__get_curse_card_count(number_of_players)
        elif card == "Copper":
            return 60
        elif card == "Silver":
            return 40
        elif card == "Gold":
            return 30
        else:
            return 10

    def __is_victory_card(self,card):
        return card in ["Estate", "Duchy", "Province"]

    def __get_victory_card_count(self, card, number_of_players):
        victory_cards =  8 if number_of_players == 2 else 12
        victory_cards += (3*number_of_players) if card == "Estate" else 0
        return victory_cards

    def __get_curse_card_count(self, number_of_players):
        return (number_of_players - 1) * 10

    def get_number_of_cards(self, card):
        return self.supply[card]

    def take(self, card):
        self.supply[card] = self.supply[card] - 1
