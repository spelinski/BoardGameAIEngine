'''
Created on Sep 30, 2015

@author: rohk
'''

class CommandGenerator(object):
    '''
    classdocs
    '''


    def __init__(self, playerCommunication, direction):
        '''
        Constructor
        '''
        self.playerDirection = direction
        self.playerCommunication = playerCommunication
    
    def sendPlayerDirectionName(self):
        self.playerCommunication.send_message("player " + self.playerDirection + " name")
        return self.playerCommunication.get_response()
    
    def sendColors(self):
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        colorString = "colors"
        for color in colors:
            colorString += " " + color
        self.playerCommunication.send_message(colorString)
    
    def sendPlayerHand(self, hand):
        cardString = "player " + self.playerDirection + " hand"
        for card in hand:
            cardString += " " + card.color + "," + str(card.number)
        self.playerCommunication.send_message(cardString)