from Board import Board
from battleline.view.Output import COLORS
class FormationLogic:
    def __init__(self):
        self.playedCardList = []
    def checkAllFlags(self,board):
        #get a list of all played cards
        setPlayedCardList(board)
        #get the best possible formation for an empty set
        bestFormationPossible = self.greatestPossibleFormation([])
        for flag in board.flags:
            for thisSide in 1,2:
                if thisSide == 1:
                    otherSide = 2
                else:
                    otherSide = 1
		        if len(flag.getCards(thisSide)) == 3:
		            #the flag needs to be checked
		            if len(flag.side(otherSide)) == 0:
		                if self.greatestPossibleFormation(flag.getCards(thisSide)) > bestFormationPossible:
		                    flag.claim(thisSide)
		                elif self.greatestPossibleFormation(flag.getCards(thisSide)) > self.greatestPossibleFormation(flag.getCards(otherSide)):
		                    flag.claim(thisSide)
    def setPlayedCardList(self,board):
        for flag in board:
            for card in flag:
                self.playedCardList.append(card)
    def greatestPossibleFormation(self,listOfCards):
		formation = []
        # straight flush > three of a kind > flush > straight > host
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
            listColor = listOfCards[0].color
            largerCardNumber = max(listOfCards[0].number,listOfCards[1].number)
            smallerCardNumber = min(listOfCards[0].number,listOfCards[1].number)
            #can't make a flush when starting with 2 cards of different color
            if listOfCards[0].color != listOfCards[1].color:
                return []
            #if you have a 10 and an 8, the 9 has to be unplayed to get a straight flush
            if largerCardNumber == smallerCardNumber + 2 and (largerCardNumber-1,listColor) not in self.playedCardList:
                listOfCards.append( (largerCardNumber-1,listColor) )
                return listOfCards
            
            #if you have a 9 and an 8, look for a 10 before looking for the 7
            elif largerCardNumber != 10 and (largerCardNumber+1,listColor) not in self.playedCardList:
                listOfCards.append( (largerCardNumber+1,listColor) )
                return listOfCards
            elif smallerCardNumber != 1 and (smallerCardNumber-1,listColor) not in self.playedCardList:
                listOfCards.append( (smallerCardNumber-1,listColor) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            #check the 2 higher numbers in this color
            if (listOfCards[0].number+1,listOfCards[0].color) in self.playedCardList and (listOfCards[0].number+2,listOfCards[0].color) in self.playedCardList:
                listOfCards.append((listOfCards[0].number+1,listOfCards[0].color))
                listOfCards.append((listOfCards[0].number+2,listOfCards[0].color))
                return listOfCards
            #check 1 higher number, 1 lower number in this color
            elif (listOfCards[0].number+1,listOfCards[0].color) in self.playedCardList and (listOfCards[0].number-1,listOfCards[0].color) in self.playedCardList:
                listOfCards.append((listOfCards[0].number+1,listOfCards[0].color))
                listOfCards.append((listOfCards[0].number-1,listOfCards[0].color))
                return listOfCards
            #check 2 lower numbers in this color
            elif (listOfCards[0].number-1,listOfCards[0].color) in self.playedCardList and (listOfCards[0].number-2,listOfCards[0].color) in self.playedCardList:
                listOfCards.append((listOfCards[0].number-1,listOfCards[0].color))
                listOfCards.append((listOfCards[0].number-2,listOfCards[0].color))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            #calculate the highest possible straight flush with remaining cards
            for color in COLORS:
                for number in [8,7,6,5,4,3,2,1]:
                    #check if number, number+1, and number+2 are all not in the list
                    if (number,color) not in self.playedCardList and (number+1,color) not in self.playedCardList and (number+2,color) not in self.playedCardList:
                        return [(number,color),(number+1,color),(number+2,color)]
    def createThreeOfAKind(self,listOfCards):
        if len(listOfCards) == 2:
            listOfColorsAvailable = []
            number = listOfCards[0].number
            #see if there is at least 1 color of this number unplayed
            for color in COLORS:
                if (number,color) not in self.playedCardList:
                    listOfColorsAvailable.append(color)
            if len(listOfColorsAvailable) >= 1:
                listOfCards.append( (number,listOfColorsAvailable[0]) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            listOfColorsAvailable = []
            number = listOfCards[0].number
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
            for number in range(10,1):
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
            listOfNumbersAvailable = []
            color = listOfCards[0].color
            #see if there is at least 1 number of this color unplayed
            for number in range(10,1):
                if (number,color) not in self.playedCardList:
                    listOfNumbersAvailable.append(number)
            if len(listOfNumbersAvailable) >= 1:
                listOfCards.append( (listOfNumbersAvailable[0],color) )
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            listOfNumbersAvailable = []
            color = listOfCards[0].color
            #see if there is at least 2 numbers of this color unplayed
            for number in range(10,1):
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
                for number in range(10,1):
                    if (number,color) not in self.playedCardList:
                        listOfNumbersAvailable.append(number)
                if len(listOfNumbersAvailable) >= 3:
                    return [(listOfNumbersAvailable[0],color),(listOfNumbersAvailable[1],color),(listOfNumbersAvailable[2],color)]
            #if nothing was found, return an empty list
            return []
    def createStraight(self,listOfCards):
        if len(listOfCards) == 2:
            largerCardNumber = max(listOfCards[0].number,listOfCards[1].number)
            smallerCardNumber = min(listOfCards[0].number,listOfCards[1].number)
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
            listOfNeededNumbers = []
            wasItAdded = [False,False,False,False]
            if listOfCards[0].number != 10 and listOfCards[0].number != 9:
                #find a number in any color that is 2 more than this one
                for color in COLORS:
                    if (largerCardNumber+2,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (largerCardNumber+2,color) )
                        wasItAdded[0]= True
                        break;
            if listOfCards[0].number != 10:
                #find a number in any color that is 1 more than this one
                for color in COLORS:
                    if (largerCardNumber+1,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (largerCardNumber+1,color) )
                        wasItAdded[1]= True
                        break;
            if listOfCards[0].number != 1:
                #find a number in any color that is 1 less than this one
                for color in COLORS:
                    if (smallerCardNumber-1,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (smallerCardNumber-1,color) )
                        wasItAdded[2]= True
                        break;
            if listOfCards[0].number != 1 and listOfCards[0].number != 2:
                #find a number in any color that is 2 less than this one
                for color in COLORS:
                    if (smallerCardNumber-2,color) not in self.playedCardList:
                        listOfNeededNumbers.append( (smallerCardNumber-2,color) )
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
    def createHost(self,listOfCards):
        if len(listOfCards) == 2:
        if len(listOfCards) == 1:
        if len(listOfCards) == 0:
        
