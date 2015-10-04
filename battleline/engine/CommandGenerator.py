"""
Created on Sep 30, 2015

@author: rohk
"""
from battleline.Identifiers import Identifiers


class CommandGenerator(object):
    """
    Generates command strings and send them to the bot given
    """

    def __init__(self, playerCommunication, direction):
        """
        Constructor
        @param playerCommunication communication to the bot to send commands to
        @param direction the direction that bot is on the board either north or south
        """
        self.playerDirection = direction
        self.playerCommunication = playerCommunication

    def send_player_direction_name(self):
        """
        sends the bot the player direction command
        there should be a response from the bot to be gotten and checked
        """
        self.playerCommunication.send_message(
            "player " + self.playerDirection + " name")

    def send_colors(self):
        """
        Sends the bot what colors are being used for the game
        """
        msg = "colors"
        for color in Identifiers.COLORS:
            msg += " " + color
        self.playerCommunication.send_message(msg)

    def send_player_hand(self, hand):
        """
        Sends the bot what's in it's hand
        @param hand list of cards in the bot's hand
        """
        msg = "player " + self.playerDirection + " hand"
        for card in hand:
            msg += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(msg)

    def send_flag_claim_status(self, listOfFlags):
        """
        Tells the bot what the claim status of all the flags are
        @param listOfFlags list of all the flags in the game in order from 1-9
        """
        msg = "flag claim-status"
        for flag in listOfFlags:
            msg += " " + self.__who_has_claimed_parsed(flag)
        self.playerCommunication.send_message(msg)

    def send_opponent_play(self, flagIndex, card):
        """
        Tell the bot what flag and card the other bot played during it's turn
        @param flagIndex index of the flag that was played on
        @param card the card that was played
        """
        self.playerCommunication.send_message(
            "opponent play " + str(flagIndex) + " " + card.color + "," + str(card.number))

    def send_go_play(self):
        """
        Tell the bot to play a card
        there should be a response from the bot to be gotten and checked
        """
        self.playerCommunication.send_message("go play-card")

    def send_flag_cards(self, listOfFlags):
        """
        Tell the bot all the cards on each flag
        @param listOfFlags list of all the flags in the game in order from 1-9
        """
        for i, flag in enumerate(listOfFlags, start=1):
            self.__send_flag_cards_north(flag, i)
            self.__send_flag_cards_south(flag, i)

    def __send_flag_cards_north(self, flag, number):
        """
        Send the cards on the north side of a single flag
        @param flag the flag to send the cards of
        @param number the flag numer bewteen 1-9
        """
        msg = "flag " + str(number) + " cards north"
        for card in flag.get_cards("Player North"):
            msg += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(msg)

    def __send_flag_cards_south(self, flag, number):
        """
        Send the cards on the south side of a single flag
        @param flag the flag to send the cards of
        @param number the flag numer bewteen 1-9
        """
        msg = "flag " + str(number) + " cards south"
        for card in flag.get_cards("Player South"):
            msg += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(msg)

    def __who_has_claimed_parsed(self, flag):
        """
        Parses out who has claimed the flag
        @param flag the flag to parse the claimant of
        """
        if flag.claimed == "Player North":
            return Identifiers.NORTH
        elif flag.claimed == "Player South":
            return Identifiers.SOUTH
        return "unclaimed"
