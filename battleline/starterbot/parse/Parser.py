'''
Created 2 Oct 15

@author: Drofsned

'''

from battleline.starterbot.model.Card import Card
from battleline.starterbot.model.State import State
from battleline.starterbot.strategy.Strategy import Strategy


class Parser(object):

    def __init__(self):
        self.state = State()
        self.strategy = Strategy()

    def process(self, message):
        return self.__needs_reply(message)

    def response(self):
        return self.state.reply

    def __needs_reply(self, message):
        if self.__is_player_name_request(message):
            return self.__reply_to_name_request(message)

        elif self.__is_hand_message(message):
            return self.__parse_hand(message)

        elif self.__is_colors_message(message):
            return self.__parse_colors(message)

        elif self.__is_flag_claim_message(message):
            return self.__parse_flag_claim(message)

        elif self.__is_flag_message(message):
            return self.__parse_flag_message(message)

        elif self.__is_opponent_message(message):
            return self.__parse_opponent(message)

        elif self.__is_go_command(message):
            return self.__decide()

        return False

    def __is_player_name_request(self, message):
        return message.split()[0] == 'player' and message.split()[2] == 'name'

    def __reply_to_name_request(self, message):
        self.state.seat = message.split()[1]
        self.state.reply = 'player {} {}'.format(
            message.split()[1], State.NAME)
        return True

    def __is_hand_message(self, message):
        return message.split()[0] == 'player' and message.split()[2] == 'hand'

    def __parse_hand(self, message):
        self.state.hand = [Card().text_to_card(card)
                           for card in message.split()[3:]]
        return False

    def __is_colors_message(self, message):
        return message.startswith('colors')

    def __parse_colors(self, message):
        self.state.colors = tuple(message.split()[1:])
        return False

    def __is_flag_claim_message(self, message):
        return message.split()[0] == 'flag' and message.split()[1] == 'claim-status'

    def __parse_flag_claim(self, message):
        self.state.flag_statuses = message.split()[2:]
        return False

    def __is_flag_message(self, message):
        return message.split()[0] == 'flag' and message.split()[2] == 'cards'

    def __parse_flag_message(self, message):
        self.state.update_flag_cards(
            *self.__make_flag_seat_cards_list(message))
        return False

    def __make_flag_seat_cards_list(self, message):
        return [int(message.split()[1]), message.split()[3], self.__make_card_list(message.split())]

    def __make_card_list(self, parsed):
        return [Card().text_to_card(card) for card in parsed[4:]]

    def __is_opponent_message(self, message):
        return message.startswith('opponent')

    def __parse_opponent(self, message):
        self.state.opponents_last_play = self.__make_last_play_dict(
            message.split()[2], message.split()[3])
        return False

    def __make_last_play_dict(self, flag, card):
        return {'flag': int(flag), 'card': Card().text_to_card(card)}

    def __is_go_command(self, message):
        return message.startswith('go')

    def __decide(self):
        self.strategy.decide(self.state)
        return True
