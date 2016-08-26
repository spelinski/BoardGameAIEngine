from dominion import Identifiers

def is_victory_card(card):
    return card in [Identifiers.ESTATE, Identifiers.DUCHY, Identifiers.PROVINCE]
