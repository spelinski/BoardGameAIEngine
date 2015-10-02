'''
Created on Sep 30, 2015

@author: rohk
'''


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
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        colorString = "colors"
        for color in colors:
            colorString += " " + color
        self.playerCommunication.send_message(colorString)

    def send_player_hand(self, hand):
        cardString = "player " + self.playerDirection + " hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(cardString)

    def send_flag_claim_status(self, listOfFlags):
        flagClaimString = "flag claim-status"
        for flag in listOfFlags:
            flagClaimString += " " + self.__who_has_claimed_parsed(flag)
        self.playerCommunication.send_message(flagClaimString)

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
        flagCardNorthString = "flag " + str(number) + " cards north"
        for card in flag.get_cards("Player North"):
            flagCardNorthString += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(flagCardNorthString)

    def __send_flag_cards_south(self, flag, number):
        flagCardNorthString = "flag " + str(number) + " cards south"
        for card in flag.get_cards("Player South"):
            flagCardNorthString += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(flagCardNorthString)

    def __who_has_claimed_parsed(self, flag):
        if flag.who_has_claimed() == "Player North":
            return "north"
        elif flag.who_has_claimed() == "Player South":
            return "south"
        return "unclaimed"
