'''
Created 4 Oct 15

@author: Drofsned

'''

import unittest
from battleline.starterbot.model.State import State
from battleline.starterbot.model.Flags import Flags
from battleline.starterbot.model.Card import Card


class TestState(unittest.TestCase):

    def setUp(self):
        self.state = State()
        self.state.seat = 'north'
        self.card_list = self.__list_of_three_cards()
        self.flags_list = self.__test_list_dict()

    def test_State_NAME_is_mybot(self):
        self.assertEqual('random_starterbot', State.NAME)

    def test_get_full_flags_no_flags_full(self):
        self.__add_three_cards_to_flags(self.flags_list['test empty'])
        self.assertEqual(
            self.flags_list['test empty'], self.state.get_full_flags())

    def test_get_full_flags_flag_1_full(self):
        self.__add_three_cards_to_flags(self.flags_list['test one'])
        self.assertEqual(
            self.flags_list['test one'], self.state.get_full_flags())

    def test_get_full_flags_flag_1_3_9_full(self):
        self.__add_three_cards_to_flags(self.flags_list['test three'])
        self.assertEqual(
            self.flags_list['test three'], self.state.get_full_flags())

    def __list_of_three_cards(self):
        return [Card('puse', num).value for num in range(1, 4)]

    def __test_list_dict(self):
        return {'test empty': [], 'test one': [1], 'test three': [1, 3, 9]}

    def __add_three_cards_to_flags(self, flags_list):
        self.state.flags = Flags()
        for flag in flags_list:
            self.state.flags.add_cards(flag, 'north', self.card_list)
