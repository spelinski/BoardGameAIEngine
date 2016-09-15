from dominion.Identifiers import *

def is_victory_card(card):
    return card in VICTORY_CARDS

def is_treasure(card):
    return card in TREASURE_CARDS

def is_action_card(card):
    return card in ALL_ACTION_CARDS

def get_victory_points(card):
    if card == ESTATE: return 1
    if card == DUCHY: return 3
    if card == PROVINCE: return 6
    if card == CURSE: return -1
    return 0

def get_worth(card):
    if card == COPPER: return 1
    if card == SILVER: return 2
    if card == GOLD: return 3
    return 0

def get_cost(card):
    if card in [CURSE, COPPER]: return 0
    if card in [MOAT, CELLAR, ESTATE]: return 2
    if card in [SILVER, VILLAGE, WOODCUTTER, WORKSHOP] : return 3
    if card in [REMODEL, SMITHY, MILITIA] : return 4
    if card in [MINE, MARKET, DUCHY] : return 5
    if card in [GOLD]: return 6
    if card in [PROVINCE] : return 8
    raise ValueError("card not recognized")

def get_extra_actions(card):
    if card == VILLAGE: return 2
    if card in [CELLAR, MARKET]: return 1
    return 0

def get_extra_buys(card):
    if card == MARKET: return 1
    if card == WOODCUTTER: return 1
    return 0

def get_extra_cards(card):
    if card == MARKET: return 1
    if card == SMITHY: return 3
    if card == VILLAGE: return 1
    if card == MOAT: return 2
    return 0

def get_extra_treasure(card):
    if card == MARKET: return 1
    if card == MILITIA: return 2
    if card == WOODCUTTER: return 2
    return 0
