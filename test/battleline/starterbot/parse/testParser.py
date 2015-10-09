'''
Created 2 Oct 15

@author: Drofsned

'''
import unittest
from battleline.starterbot.parse.Parser import Parser
from battleline.starterbot.model.State import State
from battleline.starterbot.model.Flags import Flags
from battleline.starterbot.model.Card import Card


class TestParsing(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
        self.test_message = self.__get_test_messages()
        self.expected = self.__get_expected()

    def test_parser_response_empty_txt(self):
        self.assertEqual('', self.parser.response())

    def test_reply_false_to_unknown_message(self):
        self.assertFalse(self.parser.process('watch me whip'))

    def test_reply_true_go_command(self):
        self.assertTrue(self.parser.process('go play-cards'))

    def test_reply_true_name_request(self):
        self.assertTrue(self.parser.process('player north name'))

    def test_reply_false_colors_message(self):
        self.assertFalse(self.parser.process('colors a b c d e f g'))

    def test_reply_false_player_hand_message(self):
        self.assertFalse(self.parser.process(
            'player north hand ' + ' '.join(['color1,{}'.format(x) for x in range(1, 8)])))

    def test_reply_false_flag_message(self):
        self.assertFalse(self.parser.process('flag 1 cards north'))

    def test_reply_false_flag_claim_status(self):
        self.assertFalse(self.parser.process(
            'flag claim-status ' + ' '.join(['unclaimed'] * 9)))

    def test_run_test_list(self):
        for test in self.test_message.keys():
            self.__run_test(test)

    def __run_test(self, key):
        self.parser.process(self.test_message[key])
        self.assertEqual(self.expected[key], self.__result(key))

    def __get_test_messages(self):
        return {
            'respond_north_and_name': 'player north name',
            'respond_south_and_name': 'player south name',
            'read_and_set_colors': 'colors a b c d e f',
            'read_and_set_player_hand': 'player north hand ' + ' '.join(['color1,{}'.format(x) for x in range(1, 8)]),
            'read_and_set_flag_claim_status': 'flag claim-status ' + ' '.join(['unclaimed'] * 9),
            'read_and_set_flag_messages_no_cards': 'flag 1 cards north',
            'read_and_set_flag_messages_one_card': 'flag 1 cards north color1,1',
            'read_and_set_flag_messages_three_cards': 'flag 2 cards south color1,1 color2,2 color3,3',
            'read_and_set_opponent_last_play': 'opponent play 1 color1,1'
        }

    def __get_expected(self):
        return {
            'respond_north_and_name': 'player north {}'.format(State.NAME),
            'respond_south_and_name': 'player south {}'.format(State.NAME),
            'read_and_set_colors': ('a', 'b', 'c', 'd', 'e', 'f'),
            'read_and_set_player_hand': [Card('color1', number).value for number in range(1, 8)],
            'read_and_set_flag_claim_status': ['unclaimed'] * 9,
            'read_and_set_flag_messages_no_cards': [],
            'read_and_set_flag_messages_one_card': [Card('color1', 1).value],
            'read_and_set_flag_messages_three_cards': [Card('color1', 1).value, Card('color2', 2).value, Card('color3', 3).value],
            'read_and_set_opponent_last_play': {'flag': 1, 'card': Card('color1', 1).value}
        }

    def __result(self, key):
        if key == 'respond_north_and_name':
            return self.parser.state.reply
        elif key == 'respond_south_and_name':
            return self.parser.state.reply
        elif key == 'read_and_set_colors':
            return self.parser.state.colors
        elif key == 'read_and_set_player_hand':
            return self.parser.state.hand
        elif key == 'read_and_set_flag_claim_status':
            return self.parser.state.flag_statuses
        elif key == 'read_and_set_flag_messages_no_cards':
            return self.parser.state.flags.north[0]
        elif key == 'read_and_set_flag_messages_one_card':
            return self.parser.state.flags.north[0]
        elif key == 'read_and_set_flag_messages_three_cards':
            return self.parser.state.flags.south[1]
        elif key == 'read_and_set_opponent_last_play':
            return self.parser.state.opponents_last_play
