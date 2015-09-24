"""
Dictates the lines that are written to the output file in these cases:
1. Player draws a card 
	'name' draws [1-10] 'color' 
	'name' draws 'tactic'
2. Player plays a card 
	'name' plays [1-10] 'color' [1-10] 
	'name' plays 'tactic' [1-10]
3. Player claims a flag
	'name' claims [1-9]
 4. Player wins
	'name' wins

'color'  can be any of ['blue','red','green','orange','purple','yellow']
'tactic' can be any of ['Alexander','Darius','cavalry','shield','traitor','deserter','redeploy','scout','fog','mud']
"""
COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'yellow']
TACTICS = ['Alexander', 'Darius', 'cavalry', 'shield',
           'traitor', 'deserter', 'redeploy', 'scout', 'fog', 'mud']
ACTIONS = ['draw', 'play', 'claim', 'win']


class Output:
    filename = "output.txt"

    def __init__(self):
        self.outputString = ""
        self.fileHandle = open(self.filename, 'w')
        self.fileHandle.close()

    def write(self):
        self.fileHandle = open(self.filename, 'a')
        self.fileHandle.write(self.outputString + "\n")
        self.fileHandle.close()

    def setOutputString(self, playerName, action, number, color, tactic="", flagNumber=0):
        self.outputString = str(playerName) + " " + action + "s "

        # if it has a number, it is a draw || play troop
        if number != 0:
            self.outputString = self.outputString + str(number) + " " + color
        # if it has a tactic string, it's a draw || play tactic
        elif tactic != "":
            self.outputString = self.outputString + str(tactic)
        # if it has a flag number, it is a claim
        elif flagNumber != 0 and action == ACTIONS[2]:
            self.outputString = self.outputString + str(flagNumber)

    def action(self, playerName, action, number, color, tactic="", flagNumber=0):
        self.setOutputString(playerName, action, number,
                             color, tactic, flagNumber)
        self.write()
