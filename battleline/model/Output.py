# Dictates the lines that are written to the output file in these cases:
# 1. Player draws a card
#		'name' draws [1-10] 'color'
#		'name' draws 'tactic'
# 2. Player plays a card
#		'name' plays [1-10] 'color' [1-10]
#		'name' plays 'tactic' [1-10]
# 3. Player claims a flag
#		'name' claims [1-10]
# 4. Player wins
#		'name' wins
#
# 'color'  can be any of ['blue','red','green','orange','purple','yellow']
# 'tactic' can be any of ['Alexander','Darius','cavalry','shield','traitor','deserter','redeploy','scout','fog','mud']

COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'yellow']
TACTICS = ['Alexander', 'Darius', 'cavalry', 'shield',
           'traitor', 'deserter', 'redeploy', 'scout', 'fog', 'mud']
ACTIONS = ['draw', 'play', 'claim', 'win']


class Output:
    filename = "output.txt"

    def __init__(self):
        self.fileHandle = open(self.filename, 'w')

    def __del__(self):
        self.fileHandle.close()

    def action(self, playerName, action, number, color, tactic="", flagNumber=0):
        outputString = str(playerName) + " " + action + "s "

        # if it has a number, it is a draw || play troop
        if number != 0:
            outputString = outputString + str(number) + " " + color
        # if it has a tactic string, it's a draw || play tactic
        elif tactic != "":
            outputString = outputString + str(tactic)
        # if it has a flag number, it is a claim
        elif flagNumber != 0 and action == ACTIONS[2]:
            outputString = outputString + str(flagNumber)

        self.fileHandle.write(outputString + "\n")
        return True
