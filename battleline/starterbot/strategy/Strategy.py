'''
Created 5 Oct 15

@author: Drofsned

'''
from random import shuffle
from battleline.starterbot.model.Flags import Flags
from battleline.starterbot.model.Card import Card


class Strategy(object):

    def decide(self, state):
        if self.__choose_random(state):
            self.__random_strategy(state)
        else:
            self.__no_moves_strategy(state)

    def __choose_random(self, state):
        return True

    def __random_strategy(self, state):
        if self.__able_to_play_a_card(state):
            flags = self.__unclaimed_minus_full_flags(state)

            shuffle(state.hand)
            shuffle(flags)

            state.reply = self.__random_reply_text(flags, state.hand)
        else:
            self.__no_moves_strategy(state)

    def __no_moves_strategy(self, state):
        state.reply = 'no moves'

    def __able_to_play_a_card(self, state):
        return len(state.hand) > 0 and len(self.__unclaimed_flags(state)) > 0 and len(self.__full_flags(state)) < Flags.NUM_FLAGS

    def __unclaimed_flags(self, state):
        return [i for i, status in enumerate(state.flag_statuses, start=1) if status == "unclaimed"]

    def __full_flags(self, state):
        return state.get_full_flags()

    def __random_reply_text(self, flags, cards):
        return 'play {} {}'.format(self.__get_first(flags), Card().card_to_text(self.__get_first(cards)))

    def __get_first(self, list):
        return list[0]

    def __unclaimed_minus_full_flags(self, state):
        return [flag for flag in self.__unclaimed_flags(state) if flag not in self.__full_flags(state)]
