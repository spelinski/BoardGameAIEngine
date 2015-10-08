from collections import namedtuple
"""
Global Identifiers

'color'  can be any of ['color1', 'color2', 'color3', 'color4', 'color5', 'color6']
"""
TroopCard = namedtuple("TroopCard", ["number", "color"])


def get_card_string(card):
    return "{},{}".format(card.color, card.number)


class Identifiers(object):
    COLORS = ('color1', 'color2', 'color3', 'color4', 'color5', 'color6')
    TACTICS = ('Alexander', 'Darius', 'cavalry', 'shield',
               'traitor', 'deserter', 'redeploy', 'scout', 'fog', 'mud')
    NORTH = 'north'
    SOUTH = 'south'

    @classmethod
    def is_player_valid(cls, player):
        return player in [Identifiers.NORTH, Identifiers.SOUTH]
