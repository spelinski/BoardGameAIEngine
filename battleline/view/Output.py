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

'color'  can be any of ['color1', 'color2', 'color3', 'color4', 'color5', 'color6']
'tactic' can be any of ['Alexander','Darius','cavalry','shield','traitor','deserter','redeploy','scout','fog','mud']
"""
COLORS = ['color1', 'color2', 'color3', 'color4', 'color5', 'color6']
TACTICS = ['Alexander', 'Darius', 'cavalry', 'shield',
           'traitor', 'deserter', 'redeploy', 'scout', 'fog', 'mud']
ACTIONS = ['draw', 'play', 'claim', 'win']

import os.path


class Output:

    def __init__(self):
        self.filename = "output.txt"
        self.__find_next_filename()

        self.fileHandle = open(self.filename, 'w')
        self.fileHandle.close()

        self.outputString = ""

    def setup_player_postitions(self, playerName, place):
        self.outputstring = "{} is {}".format(playerName, place)
        self.__write()

    def action(self, playerName, action, card="", flagNumber=""):
        self.__set_output_string(playerName, action, card, flagNumber)
        self.__write()

    def __set_output_string(self, playerName, action, card, flagNumber):
        if card = "":
            self.outputString = "{} {}s {}".format(
                playerName, action, flagNumber)
        else:
            self.outputString = "{} {}s {} {} {}".format(
                playerName, action, card.number, card.color, flagNumber)

    def __write(self):
        self.fileHandle = open(self.filename, 'a')
        self.fileHandle.write(self.outputString + "\n")
        self.fileHandle.close()

    def __find_next_filename(self):
        file_index = 1
        while os.path.isfile(self.filename):
            self.filename = "output{}.txt".format(file_index)
            file_index += 1
