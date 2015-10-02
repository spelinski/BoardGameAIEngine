'''
Created on Sep 30, 2015

@author: rohk
'''
import unittest
from battleline.engine.CommandGenerator import CommandGenerator
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
from collections import namedtuple
from itertools import product
from battleline.model.Flag import Flag

TroopCard = namedtuple("TroopCard", ["number", "color"])


class TestCommandGenerator(unittest.TestCase):

    def setUp(self):
        self.mockCommunication = MockPlayerCommunication()

    def test_send_player_north_name(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, "north")
        localCommandGenerator.send_player_direction_name()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "player north name")

    def test_send_player_south_name(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, "south")
        localCommandGenerator.send_player_direction_name()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "player south name")

    def test_send_colors(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, "north")
        localCommandGenerator.send_colors()
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        colorString = "colors"
        for color in colors:
            colorString += " " + color
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), colorString)

    def test_send_player_hand_north(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, "north")
        colors = ["RED"]
        hand = [TroopCard(number, color)
                for color, number in product(colors, range(1, 8))]
        localCommandGenerator.send_player_hand(hand)
        cardString = "player north hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), cardString)

    def test_send_player_hand_south(self):
        localCommandGenerator = CommandGenerator(
            self.mockCommunication, "south")
        colors = ["RED"]
        hand = [TroopCard(number, color)
                for color, number in product(colors, range(1, 8))]
        localCommandGenerator.send_player_hand(hand)
        cardString = "player south hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), cardString)
    
    def test_send_flag_claim_status_no_claims(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        claimStatusString = "flag claim-status"
        flagList = []
        for _ in range(1,10):
            claimStatusString += " unclaimed"
            flagList.append(Flag())
        localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(self.mockCommunication.messages_received.pop(), claimStatusString)
    
    def test_send_flag_claim_status_north_claim(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        claimStatusString = "flag claim-status"
        flagList = []
        for _ in range(1,9):
            claimStatusString += " unclaimed"
            flagList.append(Flag())
        tempFlag = Flag()
        tempFlag.claim("Player North")
        flagList.append(tempFlag)
        claimStatusString += " north"
        localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(self.mockCommunication.messages_received.pop(), claimStatusString)
        
    def test_send_flag_claim_status_south_claim(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        claimStatusString = "flag claim-status"
        flagList = []
        for _ in range(1,9):
            claimStatusString += " unclaimed"
            flagList.append(Flag())
        tempFlag = Flag()
        tempFlag.claim("Player South")
        flagList.append(tempFlag)
        claimStatusString += " south"
        localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(self.mockCommunication.messages_received.pop(), claimStatusString)
    
    def test_send_flag_cards_no_cards(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        flagList = []
        for _ in range(1,10):
            flagList.append(Flag())
        localCommandGenerator.send_flag_cards(flagList)
        i = 1
        for _ in flagList:
            flagString = "flag " + str(i) + " cards"
            self.assertEqual(self.mockCommunication.messages_received.pop(), flagString + " south")
            self.assertEqual(self.mockCommunication.messages_received.pop(), flagString + " north")
            ++i
            
    def test_send_flag_cards_one_card(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        flagList = []
        for _ in range(1,9):
            flagList.append(Flag())
        lastFlag = Flag()
        lastFlag.add_card("Player North",TroopCard(1,"RED"))
        localCommandGenerator.send_flag_cards(flagList)
        i = 1
        for _ in flagList:
            flagString = "flag " + str(i) + " cards"
            self.assertEqual(self.mockCommunication.messages_received.pop(), flagString + " south")
            if i == 10:
                flagString += " RED,1"
                self.assertEqual(self.mockCommunication.messages_received.pop(), flagString + " north")
            else:
                self.assertEqual(self.mockCommunication.messages_received.pop(), flagString + " north")
            ++i
    
    def test_send_opponent_play(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        localCommandGenerator.send_opponent_play(2, TroopCard(2,"RED"))
        self.assertEqual(self.mockCommunication.messages_received.pop(), "opponent play 2 RED,2")
    
    def test_send_go_play(self):
        localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        localCommandGenerator.send_go_play()
        self.assertEqual(self.mockCommunication.messages_received.pop(), "go play-card")
