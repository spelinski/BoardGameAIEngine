'''
Created on Sep 30, 2015

@author: rohk
'''
import unittest
from battleline.engine.CommandGenerator import CommandGenerator
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
from battleline.model.Flag import Flag
from battleline.Identifiers import Identifiers, TroopCard


class TestCommandGenerator(unittest.TestCase):

    def setUp(self):
        self.mockCommunication = MockPlayerCommunication()

    def test_send_player_north_name(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        localCommandGenerator.send_player_direction_name()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "player north name")

    def test_send_player_south_name(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.SOUTH)
        localCommandGenerator.send_player_direction_name()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "player south name")

    def test_send_colors(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        localCommandGenerator.send_colors()
        colorString = "colors"
        for color in Identifiers.COLORS:
            colorString += " " + color
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), colorString)

    def test_send_player_hand_north(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        hand = [TroopCard(number, Identifiers.COLORS[0])
                for number in range(1, 8)]
        localCommandGenerator.send_player_hand(hand)
        cardString = "player north hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), cardString)

    def test_send_player_hand_south(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.SOUTH)
        hand = [TroopCard(number, Identifiers.COLORS[0])
                for number in range(1, 8)]
        localCommandGenerator.send_player_hand(hand)
        cardString = "player south hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), cardString)

    def test_send_flag_claim_status_no_claims(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        claimStatusString = "flag claim-status"
        flagList = []
        for _ in range(1, 10):
            claimStatusString += " unclaimed"
            flagList.append(Flag())
        localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), claimStatusString)

    def test_send_flag_claim_status_north_claim(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        claimStatusString = "flag claim-status"
        flagList = []
        for _ in range(1, 9):
            claimStatusString += " unclaimed"
            flagList.append(Flag())
        tempFlag = Flag()
        tempFlag.claim("Player North")
        flagList.append(tempFlag)
        claimStatusString += " north"
        localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), claimStatusString)

    def test_send_flag_claim_status_south_claim(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        claimStatusString = "flag claim-status"
        flagList = []
        for _ in range(1, 9):
            claimStatusString += " unclaimed"
            flagList.append(Flag())
        tempFlag = Flag()
        tempFlag.claim("Player South")
        flagList.append(tempFlag)
        claimStatusString += " south"
        localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), claimStatusString)

    def test_send_flag_cards_no_cards(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        flagList = [Flag() for _ in xrange(10)]
        localCommandGenerator.send_flag_cards(flagList)
        for i, _ in enumerate(flagList, start=1):
            flagString = "flag " + str(i) + " cards"
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), flagString + " north")
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), flagString + " south")

    def test_send_flag_cards_one_card(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        flagList = [Flag() for _ in xrange(9)]
        lastFlag = Flag()
        lastFlag.add_card("Player North", TroopCard(1, Identifiers.COLORS[0]))
        localCommandGenerator.send_flag_cards(flagList)
        for i, _ in enumerate(flagList, start=1):
            flagString = "flag " + str(i) + " cards"
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), flagString + " north")
            if i == 10:
                flagString += " " + Identifiers.COLORS[0] + ",1"
                self.assertEqual(
                    self.mockCommunication.messages_received.pop(0), flagString + " south")
            else:
                self.assertEqual(
                    self.mockCommunication.messages_received.pop(0), flagString + " south")

    def test_send_opponent_play(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        localCommandGenerator.send_opponent_play(
            2, TroopCard(2, Identifiers.COLORS[0]))
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "opponent play 2 " + Identifiers.COLORS[0] + ",2")

    def test_send_go_play(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)
        localCommandGenerator.send_go_play()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "go play-card")
