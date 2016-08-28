from dominion import Identifiers
from dominion.CardInfo import is_victory_card

class Supply(object):
    """
    The common supply that players can gain/buy cards from
    """

    def __init__(self, number_of_players, set):
        """
            Constructor
            @param number_of_players  the number of players in the game
            @param set the set of cards to choose.  Valid picks are "First Game"
        """
        assert set == Identifiers.FIRST_GAME
        self.supply = self.__create_supply(number_of_players, set)

    def __create_supply(self, number_of_players, set):
        kingdom_cards = [Identifiers.CELLAR, Identifiers.MARKET, Identifiers.MILITIA, Identifiers.MINE, Identifiers.MOAT,
                         Identifiers.REMODEL, Identifiers.SMITHY, Identifiers.VILLAGE, Identifiers.WOODCUTTER, Identifiers.WORKSHOP]
        other_supply_cards = [Identifiers.COPPER, Identifiers.SILVER, Identifiers.GOLD,
                              Identifiers.ESTATE, Identifiers.DUCHY, Identifiers.PROVINCE,
                              Identifiers.CURSE]
        cards = kingdom_cards + other_supply_cards
        return  {card: self.__get_initial_number_of_cards(card, number_of_players) for card in cards}

    def __get_initial_number_of_cards(self, card, number_of_players):
        if is_victory_card(card):
            return self.__get_victory_card_count(card, number_of_players)
        elif card == Identifiers.CURSE:
            return self.__get_curse_card_count(number_of_players)
        elif card == Identifiers.COPPER:
            return 60
        elif card == Identifiers.SILVER:
            return 40
        elif card == Identifiers.GOLD:
            return 30
        else:
            return 10


    def __get_victory_card_count(self, card, number_of_players):
        victory_cards =  8 if number_of_players == 2 else 12
        victory_cards += (3*number_of_players) if card == Identifiers.ESTATE else 0
        return victory_cards

    def __get_curse_card_count(self, number_of_players):
        return (number_of_players - 1) * 10

    def get_number_of_cards(self, card):
        """
           Get the number of cards left in the supply
           @param card to get from the supply
           @return the number of cards in the supply for the particular card
        """
        return self.supply[card]

    def take(self, card):
        """ Take a card from the pile
           @param card the card we want to take
           @raise CardNotInSupplyException if the card is invalid
           @raise PileEmptyException if the pile is empty
        """
        if card not in self.supply: raise CardNotInSupplyException(card)
        if self.supply[card] == 0: raise PileEmptyException(card)
        self.supply[card] = self.supply[card] - 1

    def get_number_of_empty_piles(self):
        """Return the number of empty piles
        @return the number of empty piles in the supply
        """
        return len([key for key,value in self.supply.items() if value == 0])

    def is_game_over(self):
        return self.get_number_of_empty_piles() >= 3 or self.get_number_of_cards(Identifiers.PROVINCE) == 0

class CardNotInSupplyException(Exception):

    def __init__(self, card):
        """Create an Exception that the player is trying to take a card that isn't in the supply
        @param card the card we tried to take
        """
        self.card = card

    def __str__(self):
        return "{} is not in the supply.".format(self.card)

class PileEmptyException(Exception):

    def __init__(self, card):
        """Create an Exception that the player is trying to take a card from an empty pile
        @param card the card we tried to take
        """
        self.card = card

    def __str__(self):
        return "{}'s pile is empty'.".format(self.card)
