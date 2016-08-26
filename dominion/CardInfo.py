from dominion import Identifiers

def is_victory_card(card):
    return card in [Identifiers.ESTATE, Identifiers.DUCHY, Identifiers.PROVINCE]

def get_victory_points(card):
    if card == Identifiers.ESTATE: return 1
    if card == Identifiers.DUCHY: return 3
    if card == Identifiers.PROVINCE: return 6
    if card == Identifiers.CURSE: return -1
    return 0

def get_worth(card):
    if card == Identifiers.COPPER: return 1
    if card == Identifiers.SILVER: return 2
    if card == Identifiers.GOLD: return 3
    return 0

def get_cost(card):
    if card in [Identifiers.CURSE, Identifiers.COPPER]: return 0
    if card in [Identifiers.MOAT, Identifiers.CELLAR, Identifiers.ESTATE]: return 2
    if card in [Identifiers.SILVER, Identifiers.VILLAGE, Identifiers.WOODCUTTER, Identifiers.WORKSHOP] : return 3
    if card in [Identifiers.REMODEL, Identifiers.SMITHY, Identifiers.MILITIA] : return 4
    if card in [Identifiers.MINE, Identifiers.MARKET, Identifiers.DUCHY] : return 5
    if card in [Identifiers.GOLD]: return 6
    if card in [Identifiers.PROVINCE] : return 8
