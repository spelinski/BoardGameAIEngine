'''
Created 4 Oct 15

@author: Drofsned

'''

import unittest
from battleline.starterbot.model.Flags import Flags
from battleline.starterbot.model.Card import Card


class TestState(unittest.TestCase):

    def setUp(self):
        self.flags = Flags()
        self.flag_set = [[] for _ in range(Flags.NUM_FLAGS)]
        self.card_list = [Card('puse', 1).value]

    def test_flags_NUM_FLAGS(self):
        self.assertEqual(9, Flags.NUM_FLAGS)

    def test_init_flags_has_north_flags(self):
        self.assertEqual(self.flag_set, self.flags.north)

    def test_init_flags_has_south_flags(self):
        self.assertEqual(self.flag_set, self.flags.south)

    def test_flags_add_a_cards_north(self):
        self.flags.add_cards(1, 'north', self.card_list)
        self.assertEqual(self.card_list, self.flags.north[0])

    def test_flags_add_a_cards_south(self):
        self.flags.add_cards(1, 'south', self.card_list)
        self.assertEqual(self.card_list, self.flags.south[0])
