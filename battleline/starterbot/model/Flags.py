'''
Created 4 Oct 15

@author: Drofsned

'''
from battleline.starterbot.model.Card import Card


class Flags(object):
    NUM_FLAGS = 9

    def __init__(self):
        self.north = self.__init_flags()
        self.south = self.__init_flags()
        self.sides = {'north': self.north, 'south': self.south}

    def __init_flags(self):
        return [[] for _ in range(self.NUM_FLAGS)]

    def add_cards(self, flag, seat, cards):
        self.sides[seat][flag - 1] = cards
