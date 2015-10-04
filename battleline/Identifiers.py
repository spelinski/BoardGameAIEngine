from collections import namedtuple
"""
Global Identifiers

'color'  can be any of ['color1', 'color2', 'color3', 'color4', 'color5', 'color6']
'tactic' can be any of ['Alexander','Darius','cavalry','shield','traitor','deserter','redeploy','scout','fog','mud']
"""
TroopCard = namedtuple("TroopCard", ["number", "color"])

class Identifiers(object):
    COLORS = ('color1', 'color2', 'color3', 'color4', 'color5', 'color6')
    TACTICS = ('Alexander', 'Darius', 'cavalry', 'shield',
           'traitor', 'deserter', 'redeploy', 'scout', 'fog', 'mud')
    NORTH = 'north'
    SOUTH = 'south'