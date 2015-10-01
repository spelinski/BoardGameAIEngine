'''
Created on Sep 30, 2015

@author: rohk
'''
import unittest
from battleline.engine.CommandGenerator import CommandGenerator
from communcation.PlayerCommunication import PlayerCommunication
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
from collections import namedtuple
from itertools import product

TroopCard = namedtuple("TroopCard", ["number", "color"])

class TestCommandGenerator(unittest.TestCase):

    def setUp(self):
        self.mockCommunication = MockPlayerCommunication()

    def test_send_player_north_name(self):
        self.workingBotPath = "test/mockBot/mockBot.py"
        self.localPlayerCommunication = PlayerCommunication(self.workingBotPath)
        self.localCommandGenerator = CommandGenerator(self.localPlayerCommunication, "north")
        self.assertEqual(self.localCommandGenerator.sendPlayerDirectionName(), "player north mockBot\n")
        self.localPlayerCommunication.close()
    
    def test_send_player_south_name(self):
        self.workingBotPath = "test/mockBot/mockBot.py"
        self.localPlayerCommunication = PlayerCommunication(self.workingBotPath)
        self.localCommandGenerator = CommandGenerator(self.localPlayerCommunication, "south")
        self.assertEqual(self.localCommandGenerator.sendPlayerDirectionName(), "player south mockBot\n")
        self.localPlayerCommunication.close()
    
    def test_send_colors(self):
        self.localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        self.localCommandGenerator.sendColors()
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        colorString = "colors"
        for color in colors:
            colorString += " " + color
        self.assertEqual(self.mockCommunication.messages_received.pop(), colorString)
    
    def test_send_player_hand_north(self):
        self.localCommandGenerator = CommandGenerator(self.mockCommunication, "north")
        colors = ["RED"]
        hand = [TroopCard(number, color) for color, number in product(colors, range(1, 8))]
        self.localCommandGenerator.sendPlayerHand(hand)
        cardString = "player north hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(self.mockCommunication.messages_received.pop(), cardString)
    
    def test_send_player_hand_south(self):
        self.localCommandGenerator = CommandGenerator(self.mockCommunication, "south")
        colors = ["RED"]
        hand = [TroopCard(number, color) for color, number in product(colors, range(1, 8))]
        self.localCommandGenerator.sendPlayerHand(hand)
        cardString = "player south hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.assertEqual(self.mockCommunication.messages_received.pop(), cardString)


"""

flag claim-status <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south> <unclaimed|north|south>
   - claim status for every flag, from left-to-right.  Unclaimed indicates that nobody has claimed yet, and 1 or 2 indicates which player has claimed it

flag <1-9> cards <north|south> <card1>, <card2>, <card3>
  - Indicates on a per flag, per side basis, which cards are on the flag.
  - All three cards are optional
  - Each card is defined the same way player cards are defined

opponent play <1|9> <card>
  - Indicates the opponent move from the last turn.
  - The flag index is given
  - The card is the same format as what would be shown in a hand

Action Requests
---------------

go play-card
   - The bot must respond with the message play <1-9> <card>
   - The card is in the same format as the player hand in <color,number>
   - If the card was not in the players hand, or if it was not a valid move (such as the flag was full or claimed already),
        a move will be picked at random by the server
"""