'''
Created 4 Oct 15

@author: Drofsned

'''

from battleline.starterbot.model.Flags import Flags


class State(object):
    NAME = 'random_starterbot'

    def __init__(self):
        self.reply = ''
        self.seat = ''
        self.colors = ()
        self.hand = []
        self.flags = Flags()
        self.flag_statuses = ['unclaimed'] * Flags.NUM_FLAGS
        self.opponents_last_play = {}

    def update_flag_cards(self, flag, seat, cards):
        self.flags.add_cards(flag, seat, cards)

    def get_full_flags(self):
        return [flag + 1 for flag in range(Flags.NUM_FLAGS) if len(self.flags.sides[self.seat][flag]) == 3]
