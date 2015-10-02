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


"""

import os.path

ACTIONS = ['draw', 'play', 'claim', 'win']

class Output:

    def __init__(self):
        self.filename = "output.txt"
        self.__find_next_filename()

        self.fileHandle = open(self.filename, 'w')
        self.fileHandle.close()

        self.outputstring = ""

    def setup_player_positions(self, playerName, place):
        self.outputstring = "{} is {}".format(playerName, place)
        self.__write()

    def action(self, playerName, action, card="", flagNumber=""):
        self.__set_output_string(playerName, action, card, flagNumber)
        self.__write()

    def __set_output_string(self, playerName, action, card, flagNumber):
        if card == "":
            self.outputstring = "{} {}s {}".format(
                playerName, action, flagNumber)
        else:
            self.outputstring = "{} {}s {} {} {}".format(
                playerName, action, card.number, card.color, flagNumber)

    def __write(self):
        self.fileHandle = open(self.filename, 'a')
        self.fileHandle.write(self.outputstring + "\n")
        self.fileHandle.close()

    def __find_next_filename(self):
        file_index = 1
        while os.path.isfile(self.filename):
            self.filename = "output{}.txt".format(file_index)
            file_index += 1
