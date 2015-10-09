'''
Created on Sep 30, 2015

@author: rohk
'''
import unittest
from battleline.engine.CommandGenerator import CommandGenerator
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
from battleline.model.Flag import Flag
from battleline.Identifiers import Identifiers, TroopCard


def create_list_of_expected_flag_send_strings(flagList):
    expectedStringListNorth = []
    expectedStringListSouth = []
    for direction in [Identifiers.NORTH, Identifiers.SOUTH]:
        for i, flag in enumerate(flagList, start=1):
            expectedString = "flag " + str(i) + " cards " + direction
            if flag.get_cards(direction):
                expectedString += " " + Identifiers.COLORS[0] + ",1"
            if direction == "north":
                expectedStringListNorth.append(expectedString)
            else:
                expectedStringListSouth.append(expectedString)
    return expectedStringListNorth, expectedStringListSouth


class TestCommandGenerator(unittest.TestCase):

    def setUp(self):
        self.mockCommunication = MockPlayerCommunication()
        self.localCommandGenerator = CommandGenerator(
            self.mockCommunication, Identifiers.NORTH)

    def test_send_player_north_name(self):
        self.localCommandGenerator.send_player_direction_name()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "player north name")

    def test_send_player_south_name(self):
        self.localCommandGenerator.playerDirection = Identifiers.SOUTH
        self.localCommandGenerator.send_player_direction_name()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "player south name")

    def test_send_colors(self):
        self.localCommandGenerator.send_colors()
        colorString = "colors"
        for color in Identifiers.COLORS:
            colorString += " " + color
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), colorString)

    def test_send_player_hand_north(self):
        hand = [TroopCard(number, Identifiers.COLORS[0])
                for number in range(1, 8)]
        self.localCommandGenerator.send_player_hand(hand)
        cardString = "player north hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), cardString)

    def test_send_player_hand_south(self):
        self.localCommandGenerator.playerDirection = Identifiers.SOUTH
        hand = [TroopCard(number, Identifiers.COLORS[0])
                for number in range(1, 8)]
        self.localCommandGenerator.send_player_hand(hand)
        cardString = "player south hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), cardString)

    def test_send_flag_claim_status_no_claims(self):
        claimStatusString = "flag claim-status"
        flagList = [Flag() for _ in range(9)]
        claimStatusString += ''.join([" unclaimed" for _ in range(9)])
        self.localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), claimStatusString)

    def test_send_flag_claim_status_north_claim(self):
        claimStatusString = "flag claim-status"
        flagList = [Flag() for _ in range(9)]
        claimStatusString += ''.join([" unclaimed" for _ in range(8)])
        flagList[8].claim("north")
        claimStatusString += " north"
        self.localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), claimStatusString)

    def test_send_flag_claim_status_south_claim(self):
        claimStatusString = "flag claim-status"
        flagList = [Flag() for _ in range(9)]
        claimStatusString += ''.join([" unclaimed" for _ in range(8)])
        flagList[8].claim("south")
        claimStatusString += " south"
        self.localCommandGenerator.send_flag_claim_status(flagList)
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), claimStatusString)

    def test_send_flag_cards_no_cards(self):
        flagList = [Flag() for _ in xrange(9)]
        self.localCommandGenerator.send_flag_cards(flagList)
        expectedStringListNorth, expectedStringListSouth = create_list_of_expected_flag_send_strings(
            flagList)
        for i, _ in enumerate(flagList):
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), expectedStringListNorth[i])
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), expectedStringListSouth[i])

    def test_send_flag_cards_one_card_north(self):
        flagList = [Flag() for _ in xrange(9)]
        flagList[8].add_card("north", TroopCard(1, Identifiers.COLORS[0]))
        self.localCommandGenerator.send_flag_cards(flagList)
        expectedStringListNorth, expectedStringListSouth = create_list_of_expected_flag_send_strings(
            flagList)
        for i, _ in enumerate(flagList):
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), expectedStringListNorth[i])
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), expectedStringListSouth[i])

    def test_send_flag_cards_one_card_south(self):
        flagList = [Flag() for _ in xrange(9)]
        flagList[8].add_card("south", TroopCard(1, Identifiers.COLORS[0]))
        self.localCommandGenerator.send_flag_cards(flagList)
        expectedStringListNorth, expectedStringListSouth = create_list_of_expected_flag_send_strings(
            flagList)
        for i, _ in enumerate(flagList):
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), expectedStringListNorth[i])
            self.assertEqual(
                self.mockCommunication.messages_received.pop(0), expectedStringListSouth[i])

    def test_send_opponent_play(self):
        self.localCommandGenerator.send_opponent_play(
            2, TroopCard(2, Identifiers.COLORS[0]))
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "opponent play 2 " + Identifiers.COLORS[0] + ",2")

    def test_send_go_play(self):
        self.localCommandGenerator.send_go_play()
        self.assertEqual(
            self.mockCommunication.messages_received.pop(), "go play-card")
