"""
Dictates the lines that are written to the output file in these cases:

SETUP POSITIONS
1. Player is North
    'name' is north
2. Player is South
    'name' is south

ACTIONS
1. Player draws a card 
	'name' draws [1-10] 'color' 
2. Player plays a card 
	'name' plays [1-10] 'color' [1-9] 
3. Player claims a flag
	'name' claims [1-9]
 4. Player wins
	'name' wins

5 possible commands:
    <botName> is north
    <botName> draws <cardNumber> <colorString>
    <botName> plays <cardNumber> <colorString> <flagNumber>
    <botName> claims <flagNumber>
    <botName> wins

"""

import os.path
from battleline.Identifiers import Identifiers


class Output:

    def __init__(self):
        self.filename = "output.txt"
        self.__find_next_filename()

        self.fileHandle = open(self.filename, 'w')
        self.fileHandle.close()

        self.outputstring = ""
        self.playerNames = {Identifiers.NORTH: 'player1',
                            Identifiers.SOUTH: 'player2'}

    def setup_player_positions(self, playerName, place):
        self.playerNames[place] = playerName
        self.outputstring = "{} is {}".format(self.playerNames[place], place)
        self.__write()

    def play_action(self, place, card, flagNumber):
        self.outputstring = "{} plays {} {} {}".format(
            self.playerNames[place], str(card.number), card.color, str(flagNumber))
        self.__write()

    def draw_action(self, place, card):
        if card == None:
            self.outputstring = self.playerNames[place] + " plays nothing"
        else:
            self.outputstring = "{} draws {} {}".format(
                self.playerNames[place], str(card.number), card.color)
        self.__write()

    def claim_action(self, place, flagNumber):
        self.outputstring = self.playerNames[
            place] + " claims " + str(flagNumber)
        self.__write()

    def declare_winner(self, place):
        self.outputstring = self.playerNames[place] + " wins"
        self.__write()

    def __write(self):
        self.fileHandle = open(self.filename, 'a')
        self.fileHandle.write(self.outputstring + "\n")
        self.fileHandle.close()

    def __find_next_filename(self):
        file_index = 1
        while os.path.isfile(self.filename):
            self.filename = "output{}.txt".format(file_index)
            file_index += 1
