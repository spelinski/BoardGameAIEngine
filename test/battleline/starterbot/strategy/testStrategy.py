'''
Created 5 Oct 15

@author: Drofsned

'''

import unittest
from battleline.starterbot.strategy.Strategy import Strategy
from battleline.starterbot.model.State import State
from battleline.starterbot.model.Flags import Flags
from battleline.starterbot.model.Card import Card


class TestState(unittest.TestCase):

    def setUp(self):
        self.strategy = Strategy()
        self.mock_state = State()
        self.__stage_mock_state()
        self.flags = range(1, Flags.NUM_FLAGS + 1)
        self.card_list = self.__list_of_three_cards()

    def __stage_mock_state(self):
        self.mock_state.seat = 'north'
        self.mock_state.colors = ['color{}'.format(num) for num in range(1, 7)]
        self.mock_state.hand = [
            Card('color1', number).value for number in range(1, 8)]
        self.mock_state.flags = Flags()

    def test_random_strategy_returns_random_card(self):
        hand = [Card().card_to_text(card) for card in self.mock_state.hand]
        parsed = self.__update_and_parse_reply()
        self.assertEqual('play', parsed[0])
        self.assertIn(int(parsed[1]), self.flags)
        self.assertIn(parsed[2], hand)

    def test_random_strategy_no_moves_all_flags_claimed(self):
        self.mock_state.flag_statuses = ['north'] * Flags.NUM_FLAGS
        self.strategy.decide(self.mock_state)
        self.assertEqual('no moves', self.mock_state.reply)

    def test_random_strategy_ignores_claimed_flags(self):
        self.mock_state.flag_statuses = ['north'] * Flags.NUM_FLAGS
        self.mock_state.flag_statuses[2] = 'unclaimed'
        parsed = self.__update_and_parse_reply()
        self.assertEqual(int(parsed[1]), 3)

    def test_random_strategy_ignores_full_flags(self):
        self.__add_three_cards_to_flags([2, 3, 4, 5, 6, 7, 8, 9])
        parsed = self.__update_and_parse_reply()
        self.assertEqual(1, int(parsed[1]))

    def __update_and_parse_reply(self):
        self.strategy.decide(self.mock_state)
        return self.mock_state.reply.split()

    def __add_three_cards_to_flags(self, flags_list):
        self.mock_state.flags = Flags()
        for flag in flags_list:
            self.mock_state.flags.add_cards(flag, 'north', self.card_list)

    def __list_of_three_cards(self):
        return [Card('puse', num).value for num in range(1, 4)]
