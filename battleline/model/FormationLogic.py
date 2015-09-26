from Board import Board
from battleline.view.Output import COLORS
from Formation import Formation
class FormationLogic:
    def __init__(self):
        self.playedCardList = []
    def checkAllFlags(self,board):
        #get a list of all played cards
        self.setPlayedCardList(board)
        #get the best possible formation for an empty set because there should be a lot of those requested
        bestFormationPossible = self.greatestPossibleFormation([])
        for flag in board.flags:
            for player in [flag.PLAYER_ONE_ID,flag.PLAYER_TWO_ID]:
                if player == flag.PLAYER_ONE_ID:
                    enemy = flag.PLAYER_TWO_ID
                else:
                    player = flag.PLAYER_ONE_ID
                #thisSideBestFormation = self.greatestPossibleFormation(flag.get_cards(thisSide))
                if len(flag.get_cards(player)) == 3:
                    playerCards  = flag.get_cards(player)
                    enemyCards = flag.get_cards(enemy)
		            #the flag needs to be checked
                    if len(enemyCards) == 0:
                        if self.getTheBetterFormation(playerCards, bestFormationPossible) == playerCards:
                            flag.claim(player)
                    elif self.getTheBetterFormation( playerCards, self.greatestPossibleFormation(enemyCards) ) == playerCards:
                        flag.claim(player)
                elif len(flag.get_cards(enemy)) == 3:
                    playerCards  = flag.get_cards(player)
                    enemyCards = flag.get_cards(enemy)
		            #the flag needs to be checked
                    if len(playerCards) == 0:
                        if self.getTheBetterFormation(enemyCards, bestFormationPossible) == enemyCards:
                            flag.claim(enemy)
                    elif self.getTheBetterFormation( enemyCards, self.greatestPossibleFormation(playerCards) ) == enemyCards:
                        flag.claim(enemy)

    def getTheBetterFormation(self,formation1,formation2):
        print "1: " + str(formation1)
        print "2: " + str(formation2)
        listOfFunctions = [self.isStraightFlush,self.isThreeOfAKind,self.isFlush,self.isStraight,self.isHost]
        for function in listOfFunctions:
            if function(formation1):
                if function(formation2):
                    return self.compareMaximums(formation1,formation2)
                else:
                    return formation1
            if function(formation2):
                return formation2
    def compareMaximums(self,formation1,formation2):
        return formation1 if Formation(formation1).get_max_number() >  Formation(formation2).get_max_number() else formation2


    def isStraightFlush(self,formation):
        f = Formation(formation)
        return f.is_wedge()

    def isThreeOfAKind(self,formation):
        f = Formation(formation)
        return f.is_phalanx()

    def isFlush(self,formation):
        if len(formation) < 3:
            return False
        n1,c1 = formation[0]
        n2,c2 = formation[1]
        n3,c3 = formation[2]
        nmin = min(min(n1,n2),n3)
        if c1 != c2 or c1 != c3:
            return False
        return True
    def isStraight(self,formation):
        if len(formation) < 3:
            return False
        n1,c1 = formation[0]
        n2,c2 = formation[1]
        n3,c3 = formation[2]
        nmin = min(min(n1,n2),n3)
        if nmin+1 != n1 and nmin+1 != n2 and nmin+1 != n3:
            return False
        if nmin+2 != n1 and nmin+2 != n2 and nmin+2 != n3:
            return False
        return True
    def isHost(self,formation):
        if len(formation) < 3:
            return False
        return True
    def setPlayedCardList(self,board):
        for flag in board.flags:
            for player in flag.PLAYER_ONE_ID,flag.PLAYER_TWO_ID:
                for card in flag.get_cards(player):
                    self.playedCardList.append(card)
    def greatestPossibleFormation(self,listOfCards):
        if len(listOfCards) == 3:
            return listOfCards
        formation = []
        #straight flush > three of a kind > flush > straight > host
        formation = self.createStraightFlush(listOfCards)
        if formation == []:
            formation = self.createThreeOfAKind(listOfCards)
        if formation == []:
            formation = self.createFlush(listOfCards)
        if formation == []:
            formation = self.createStraight(listOfCards)
        if formation == []:
            formation = self.createHost(listOfCards)
        return formation
    """
    Begin the creation functions. Each tries to create a formation of its type. It will return [] if it can't create one
    They all take a list of cards that are present on the flag. They use the playedCardList variable to see what has already been played

    createStraightFlush
    createThreeOfAKind
    createFlush
    createStraight
    createHost
    """
    def createStraightFlush(self,listOfCards):
        if len(listOfCards) == 2:
            firstNumber,firstColor   = listOfCards[0]
            secondNumber,secondColor = listOfCards[1]

            largerCardNumber = max(firstNumber,secondNumber)
            smallerCardNumber = min(firstNumber,secondNumber)
            #can't make a flush when starting with 2 cards of different color
            if firstColor != secondColor:
                return []
            #if you have a 10 and an 8, the 9 has to be unplayed to get a straight flush
            if largerCardNumber == smallerCardNumber + 2 and (largerCardNumber-1,firstColor) not in self.playedCardList:
                listOfCards.append( (largerCardNumber-1,firstColor) )
                return listOfCards

            #if you have a 9 and an 8, look for a 10 before looking for the 7
            elif largerCardNumber != 10 and (largerCardNumber+1,firstColor) not in self.playedCardList:
                listOfCards.append( (largerCardNumber+1,firstColor) )
                return listOfCards
            elif smallerCardNumber != 1 and (smallerCardNumber-1,firstColor) not in self.playedCardList:
                listOfCards.append( (smallerCardNumber-1,firstColor) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number,color = listOfCards[0]
            #check the 2 higher numbers in this color
            if (number+1,color) not in self.playedCardList and (number+2,color) not in self.playedCardList:
                listOfCards.append( (number+1,color) )
                listOfCards.append( (number+2,color) )
                return listOfCards
            #check 1 higher number, 1 lower number in this color
            elif (number+1,color) not in self.playedCardList and (number-1,color) not in self.playedCardList:
                listOfCards.append( (number+1,color) )
                listOfCards.append( (number-1,color) )
                return listOfCards
            #check 2 lower numbers in this color
            elif (number-1,color) not in self.playedCardList and (number-2,color) not in self.playedCardList:
                listOfCards.append( (number-1,color) )
                listOfCards.append( (number-2,color) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            #calculate the highest possible straight flush with remaining cards
            for number in [8,7,6,5,4,3,2,1]:
                for color in COLORS:
                    #check if number, number+1, and number+2 are all not in the list
                    if (number,color) not in self.playedCardList and (number+1,color) not in self.playedCardList and (number+2,color) not in self.playedCardList:
                        return [(number,color),(number+1,color),(number+2,color)]
            return []
    def createThreeOfAKind(self,listOfCards):
        if len(listOfCards) == 2:
            firstNumber,firstColor   = listOfCards[0]
            secondNumber,secondColor = listOfCards[1]

            listOfColorsAvailable = []
            if firstNumber != secondNumber:
                return []
            #see if there is at least 1 color of this number unplayed
            for color in COLORS:
                if (firstNumber,color) not in self.playedCardList:
                    listOfColorsAvailable.append(color)
            if len(listOfColorsAvailable) >= 1:
                listOfCards.append( (firstNumber,listOfColorsAvailable[0]) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number,color = listOfCards[0]
            listOfColorsAvailable = []
            #see if there are at least 2 colors of this number unplayed
            for color in COLORS:
                if (number,color) not in self.playedCardList:
                    listOfColorsAvailable.append(color)
            if len(listOfColorsAvailable) >= 2:
                listOfCards.append( (number,listOfColorsAvailable[0]) )
                listOfCards.append( (number,listOfColorsAvailable[1]) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            #calculate the highest possible three of a kind with remaining cards
            for number in range(10,1,-1):
                listOfColorsAvailable = []
                #see if there are at least 3 colors of this number unplayed
                for color in COLORS:
                    if (number,color) not in self.playedCardList:
                        listOfColorsAvailable.append(color)
                if len(listOfColorsAvailable) >= 3:
                    return [(number,listOfColorsAvailable[0]),(number,listOfColorsAvailable[1]),(number,listOfColorsAvailable[2])]
            #if nothing was found, return an empty list
            return []
    def createFlush(self,listOfCards):
        if len(listOfCards) == 2:
            firstNumber,firstColor   = listOfCards[0]
            secondNumber,secondColor = listOfCards[1]
            listOfNumbersAvailable = []
            #see if there is at least 1 number of this color unplayed
            for number in range(10,1,-1):
                if (number,firstColor) not in self.playedCardList:
                    listOfNumbersAvailable.append(number)
            if len(listOfNumbersAvailable) >= 1:
                listOfCards.append( (listOfNumbersAvailable[0],firstColor) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number,color = listOfCards[0]
            listOfNumbersAvailable = []
            #see if there is at least 2 numbers of this color unplayed
            for number in range(10,1,-1):
                if (number,color) not in self.playedCardList:
                    listOfNumbersAvailable.append(number)
            if len(listOfNumbersAvailable) >= 2:
                listOfCards.append( (listOfNumbersAvailable[0],color) )
                listOfCards.append( (listOfNumbersAvailable[1],color) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            #calculate the highest possible flush with remaining cards
            for color in COLORS:
                listOfNumbersAvailable = []
                #see if there are at least 3 numbers of this color unplayed
                for number in range(10,1,-1):
                    if (number,color) not in self.playedCardList:
                        listOfNumbersAvailable.append(number)
                if len(listOfNumbersAvailable) >= 3:
                    return [(listOfNumbersAvailable[0],color),(listOfNumbersAvailable[1],color),(listOfNumbersAvailable[2],color)]
            #if nothing was found, return an empty list
            return []
    def createStraight(self,listOfCards):
        if len(listOfCards) == 2:
            firstNumber,firstColor   = listOfCards[0]
            secondNumber,secondColor = listOfCards[1]
            largerCardNumber = max(firstNumber,secondNumber)
            smallerCardNumber = min(firstNumber,secondNumber)
            listOfNeededNumbers = []
            if largerCardNumber != 10:
                #find a number in any color that is 1 more than the larger one
                for color in COLORS:
                    if (largerCardNumber+1,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (largerCardNumber+1,color) )
                        break;
            if smallerCardNumber != 1:
                #find a number in any color that is 1 less than the smaller one
                for color in COLORS:
                    if (smallerCardNumber-1,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (smallerCardNumber-1,color) )
                        break;
            if len(listOfNeededNumbers) != 0:
                listOfCards.append( listOfNeededNumbers[0] )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number,color = listOfCards[0]
            listOfNeededNumbers = []
            wasItAdded = [False,False,False,False]
            if number != 10 and number != 9:
                #find a number in any color that is 2 more than this one
                for color in COLORS:
                    if (number+2,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (number+2,color) )
                        wasItAdded[0]= True
                        break;
            if number != 10:
                #find a number in any color that is 1 more than this one
                for color in COLORS:
                    if (number+1,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (number+1,color) )
                        wasItAdded[1]= True
                        break;
            if number != 1:
                #find a number in any color that is 1 less than this one
                for color in COLORS:
                    if (number-1,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (number-1,color) )
                        wasItAdded[2]= True
                        break;
            if number != 1 and number != 2:
                #find a number in any color that is 2 less than this one
                for color in COLORS:
                    if (number-2,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (number-2,color) )
                        wasItAdded[3]= True
                        break;
            #if any adjacent pair of wasItAdded are both true, return the first 2 elements in the list
            if (wasItAdded[0] and wasItAdded[1]) or (wasItAdded[1] and wasItAdded[2]) or (wasItAdded[2] and wasItAdded[3]):
                listOfCards.append( listOfNeededNumbers[0] )
                listOfCards.append( listOfNeededNumbers[1] )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            listOfAvailableTroops = []
            canItBeUsed=[False,False,False,False,False,False,False,False,False,False]
            for number in range(10,0,-1):
                for color in COLORS:
                    if (number,color) not in self.playedCardList:
                        canItBeUsed[number-1]=True
                        listOfAvailableTroops.append( (number,color) )
                        break
            if ((canItBeUsed[9] and canItBeUsed[8] and canItBeUsed[7])
               or (canItBeUsed[8] and canItBeUsed[7] and canItBeUsed[6])
               or (canItBeUsed[7] and canItBeUsed[6] and canItBeUsed[5])
               or (canItBeUsed[6] and canItBeUsed[5] and canItBeUsed[4])
               or (canItBeUsed[5] and canItBeUsed[4] and canItBeUsed[3])
               or (canItBeUsed[4] and canItBeUsed[3] and canItBeUsed[2])
               or (canItBeUsed[3] and canItBeUsed[2] and canItBeUsed[1])
               or (canItBeUsed[2] and canItBeUsed[1] and canItBeUsed[0])):
                listOfCards = [listOfAvailableTroops[0],listOfAvailableTroops[1],listOfAvailableTroops[2]]
                return listOfCards
            else:
                return []
    def createHost(self,listOfCards):
        if len(listOfCards) == 3:
            return listOfCards
        neededCards = 3 - len(listOfCards)
        listOfAvailableTroops = []
        for number in range(10,0,-1):
            for color in COLORS:
                if (number,color) not in self.playedCardList:
                    listOfAvailableTroops.append( (number,color) )
                    if len(listOfAvailableTroops) == neededCards:
                        listOfCards.append( listOfAvailableTroops[0] )
                        if neededCards >= 2:
                             listOfCards.append( listOfAvailableTroops[1] )
                        if neededCards >= 3:
                             listOfCards.append( listOfAvailableTroops[2] )
                        return listOfCards
        #if it gets complete out of the loop, then there aren't enough cards left to make a host.
        return []
