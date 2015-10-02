'''
Created on Sep 30, 2015

@author: rohk
'''
from battleline.Identifiers import Identifiers


class CommandGenerator(object):
    '''
    classdocs
    '''

    def __init__(self, playerCommunication, direction):
        '''
        Constructor
        '''
        self.playerDirection = direction
        self.playerCommunication = playerCommunication

    def send_player_direction_name(self):
        self.playerCommunication.send_message(
            "player " + self.playerDirection + " name")

    def send_colors(self):
        msg = "colors"
        for color in Identifiers.COLORS:
            msg += " " + color
        self.playerCommunication.send_message(msg)

    def send_player_hand(self, hand):
        msg = "player " + self.playerDirection + " hand"
        for card in hand:
            msg += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(msg)

    def send_flag_claim_status(self, listOfFlags):
        msg = "flag claim-status"
        for flag in listOfFlags:
            msg += " " + self.__who_has_claimed_parsed(flag)
        self.playerCommunication.send_message(msg)

    def send_opponent_play(self, flagIndex, card):
        self.playerCommunication.send_message(
            "opponent play " + str(flagIndex) + " " + card.color + "," + str(card.number))

    def send_go_play(self):
        self.playerCommunication.send_message("go play-card")

    def send_flag_cards(self, listOfFlags):
        i = 1
        for flag in listOfFlags:
            self.__send_flag_cards_north(flag, i)
            self.__send_flag_cards_south(flag, i)
            ++i

    def __send_flag_cards_north(self, flag, number):
        msg = "flag " + str(number) + " cards north"
        for card in flag.get_cards("Player North"):
            msg += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(msg)

    def __send_flag_cards_south(self, flag, number):
        msg = "flag " + str(number) + " cards south"
        for card in flag.get_cards("Player South"):
            msg += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(msg)

    def __who_has_claimed_parsed(self, flag):
        if flag.claimed == "Player North":
            return Identifiers.NORTH
        elif flag.claimed == "Player South":
            return Identifiers.SOUTH
        return "unclaimed"
