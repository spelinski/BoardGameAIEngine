from Board import Board
from battleline.Identifiers import Identifiers, TroopCard
from Formation import Formation
import itertools


class FormationLogic:

    def __init__(self):
        pass

    def getTheBetterFormation(self, formation1, formation2):
        return formation1 if Formation(formation1).is_greater_strength_than(Formation(formation2)) else formation2


    def is_equivalent_in_strength(self, formation1, formation2):
        return Formation(formation1).is_equivalent_in_strength(Formation(formation2))

    def get_best_formation(self, current_formation, unplayed_cards):
        return self.__get_best_option([[card] for card in current_formation], unplayed_cards)

    def __get_best_option(self, options, unplayed_cards):

        max_strength_formation = [TroopCard(color=color, number=number)
                                  for color, number in itertools.product([Identifiers.COLORS], [1, 1, 0])]
        for a in self.__get_options(options, 0, unplayed_cards):
            next_unplayed_cards = self.__filter_out(unplayed_cards, a)
            for b in self.__get_options(options, 1, next_unplayed_cards):
                still_unplayed_cards = self.__filter_out(next_unplayed_cards, b)
                for c in self.__get_options(options, 2, still_unplayed_cards):
                    formation = [a, b, c]
                    if Formation(formation).is_greater_strength_than(Formation(max_strength_formation)):
                        max_strength_formation = formation
        return sorted(max_strength_formation, key=lambda x: (
            x[1], x[0]), reverse=True)

    def __filter_out(self, list, item):
        return [c for c in list if c.color != item.color or c.number != item.number]

    def __get_options(self, options, index, unplayed_cards):
        return options[index - 1] if len(options) > index else unplayed_cards

    def greatestPossibleFormation(self, listOfCards, playedCardList):
        if len(listOfCards) == 3:
            return listOfCards
        formation = []
        # straight flush > three of a kind > flush > straight > host
        formation = self.createStraightFlush(listOfCards, playedCardList)
        if formation == []:
            formation = self.createThreeOfAKind(listOfCards, playedCardList)
        if formation == []:
            formation = self.createFlush(listOfCards, playedCardList)
        if formation == []:
            formation = self.createStraight(listOfCards, playedCardList)
        if formation == []:
            formation = self.createHost(listOfCards, playedCardList)
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

    def createStraightFlush(self, currentCards, playedCardList):
        listOfCards = currentCards[:]
        if len(listOfCards) == 2:
            firstNumber, firstColor = listOfCards[0]
            secondNumber, secondColor = listOfCards[1]

            largerCardNumber = max(firstNumber, secondNumber)
            smallerCardNumber = min(firstNumber, secondNumber)
            # can't make a flush when starting with 2 cards of different color
            if firstColor != secondColor:
                return []
            # if you have a 10 and an 8, the 9 has to be unplayed to get a
            # straight flush
            if largerCardNumber == smallerCardNumber + 2 and (largerCardNumber - 1, firstColor) not in playedCardList:
                listOfCards.append((largerCardNumber - 1, firstColor))
                return listOfCards

            # if you have a 9 and an 8, look for a 10 before looking for the 7
            elif largerCardNumber != 10 and (largerCardNumber + 1, firstColor) not in playedCardList:
                listOfCards.append((largerCardNumber + 1, firstColor))
                return listOfCards
            elif smallerCardNumber != 1 and (smallerCardNumber - 1, firstColor) not in playedCardList:
                listOfCards.append((smallerCardNumber - 1, firstColor))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number, color = listOfCards[0]
            # check the 2 higher numbers in this color
            if (number + 1, color) not in playedCardList and (number + 2, color) not in playedCardList:
                listOfCards.append((number + 1, color))
                listOfCards.append((number + 2, color))
                return listOfCards
            # check 1 higher number, 1 lower number in this color
            elif (number + 1, color) not in playedCardList and (number - 1, color) not in playedCardList:
                listOfCards.append((number + 1, color))
                listOfCards.append((number - 1, color))
                return listOfCards
            # check 2 lower numbers in this color
            elif (number - 1, color) not in playedCardList and (number - 2, color) not in playedCardList:
                listOfCards.append((number - 1, color))
                listOfCards.append((number - 2, color))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            # calculate the highest possible straight flush with remaining
            # cards
            for number in [8, 7, 6, 5, 4, 3, 2, 1]:
                for color in Identifiers.COLORS:
                    # check if number, number+1, and number+2 are all not in
                    # the list
                    if (number, color) not in playedCardList and (number + 1, color) not in playedCardList and (number + 2, color) not in playedCardList:
                        return [(number, color), (number + 1, color), (number + 2, color)]
            return []

    def createThreeOfAKind(self, currentCards, playedCardList):
        listOfCards = currentCards[:]
        if len(listOfCards) == 2:
            firstNumber, firstColor = listOfCards[0]
            secondNumber, secondColor = listOfCards[1]

            listOfColorsAvailable = []
            if firstNumber != secondNumber:
                return []
            # see if there is at least 1 color of this number unplayed
            for color in Identifiers.COLORS:
                if (firstNumber, color) not in playedCardList:
                    listOfColorsAvailable.append(color)
            if len(listOfColorsAvailable) >= 1:
                listOfCards.append((firstNumber, listOfColorsAvailable[0]))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number, color = listOfCards[0]
            listOfColorsAvailable = []
            # see if there are at least 2 colors of this number unplayed
            for color in Identifiers.COLORS:
                if (number, color) not in playedCardList:
                    listOfColorsAvailable.append(color)
            if len(listOfColorsAvailable) >= 2:
                listOfCards.append((number, listOfColorsAvailable[0]))
                listOfCards.append((number, listOfColorsAvailable[1]))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            # calculate the highest possible three of a kind with remaining
            # cards
            for number in range(10, 1, -1):
                listOfColorsAvailable = []
                # see if there are at least 3 colors of this number unplayed
                for color in Identifiers.COLORS:
                    if (number, color) not in playedCardList:
                        listOfColorsAvailable.append(color)
                if len(listOfColorsAvailable) >= 3:
                    return [(number, listOfColorsAvailable[0]), (number, listOfColorsAvailable[1]), (number, listOfColorsAvailable[2])]
            # if nothing was found, return an empty list
            return []

    def createFlush(self, currentCards, playedCardList):
        listOfCards = currentCards[:]
        if len(listOfCards) == 2:
            firstNumber, firstColor = listOfCards[0]
            secondNumber, secondColor = listOfCards[1]
            listOfNumbersAvailable = []
            if firstColor != secondColor:
                return []
            # see if there is at least 1 number of this color unplayed
            for number in range(10, 1, -1):
                if (number, firstColor) not in playedCardList:
                    listOfNumbersAvailable.append(number)
            if len(listOfNumbersAvailable) >= 1:
                listOfCards.append((listOfNumbersAvailable[0], firstColor))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 1:
            number, color = listOfCards[0]
            listOfNumbersAvailable = []
            # see if there is at least 2 numbers of this color unplayed
            for number in range(10, 1, -1):
                if (number, color) not in playedCardList:
                    listOfNumbersAvailable.append(number)
            if len(listOfNumbersAvailable) >= 2:
                listOfCards.append((listOfNumbersAvailable[0], color))
                listOfCards.append((listOfNumbersAvailable[1], color))
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            # calculate the highest possible flush with remaining cards
            for color in Identifiers.COLORS:
                listOfNumbersAvailable = []
                # see if there are at least 3 numbers of this color unplayed
                for number in range(10, 1, -1):
                    if (number, color) not in playedCardList:
                        listOfNumbersAvailable.append(number)
                if len(listOfNumbersAvailable) >= 3:
                    return [(listOfNumbersAvailable[0], color), (listOfNumbersAvailable[1], color), (listOfNumbersAvailable[2], color)]
            # if nothing was found, return an empty list
            return []

    def createStraight(self, currentCards, playedCardList):
        listOfCards = currentCards[:]
        if len(listOfCards) == 2:
            firstNumber, firstColor = listOfCards[0]
            secondNumber, secondColor = listOfCards[1]
            largerCardNumber = max(firstNumber, secondNumber)
            smallerCardNumber = min(firstNumber, secondNumber)
            listOfNeededNumbers = []
            if largerCardNumber == smallerCardNumber + 2:
                # find a number in any color that is 1 more than the larger one
                for color in Identifiers.COLORS:
                    if (largerCardNumber - 1, color) not in playedCardList:
                        return [listOfCards[0], listOfCards[1], (largerCardNumber - 1, color)]
            elif largerCardNumber == smallerCardNumber + 1:
                # look for a number 1 larger than largerCardNumber, or 1
                # smaller than smallerCardNumber
                if largerCardNumber != 10:
                    # find a number in any color that is 1 more than the larger
                    # one
                    for color in Identifiers.COLORS:
                        if (largerCardNumber + 1, color) not in playedCardList:
                            return [listOfCards[0], listOfCards[1], (largerCardNumber + 1, color)]
                if smallerCardNumber != 1:
                    # find a number in any color that is 1 less than the smaller
                    # one
                    for color in Identifiers.COLORS:
                        if (smallerCardNumber - 1, color) not in playedCardList:
                            return [listOfCards[0], listOfCards[1], (smallerCardNumber - 1, color)]
            return []

        if len(listOfCards) == 1:
            number, color = listOfCards[0]
            listOfNeededNumbers = []
            wasItAdded = [False, False, False, False]
            if number != 10 and number != 9:
                # find a number in any color that is 2 more than this one
                for color in Identifiers.COLORS:
                    if (number + 2, color) not in playedCardList:
                        listOfNeededNumbers.append((number + 2, color))
                        wasItAdded[0] = True
                        break
            if number != 10:
                # find a number in any color that is 1 more than this one
                for color in Identifiers.COLORS:
                    if (number + 1, color) not in playedCardList:
                        listOfNeededNumbers.append((number + 1, color))
                        wasItAdded[1] = True
                        break
            if number != 1:
                # find a number in any color that is 1 less than this one
                for color in Identifiers.COLORS:
                    if (number - 1, color) not in playedCardList:
                        listOfNeededNumbers.append((number - 1, color))
                        wasItAdded[2] = True
                        break
            if number != 1 and number != 2:
                # find a number in any color that is 2 less than this one
                for color in Identifiers.COLORS:
                    if (number - 2, color) not in playedCardList:
                        listOfNeededNumbers.append((number - 2, color))
                        wasItAdded[3] = True
                        break
            # if any adjacent pair of wasItAdded are both true, return the
            # first 2 elements in the list
            if (wasItAdded[0] and wasItAdded[1]) or (wasItAdded[1] and wasItAdded[2]) or (wasItAdded[2] and wasItAdded[3]):
                listOfCards.append(listOfNeededNumbers[0])
                listOfCards.append(listOfNeededNumbers[1])
                return listOfCards
            else:
                return []
        if len(listOfCards) == 0:
            listOfAvailableTroops = []
            canItBeUsed = [False, False, False, False,
                           False, False, False, False, False, False]
            for number in range(10, 0, -1):
                for color in Identifiers.COLORS:
                    if (number, color) not in playedCardList:
                        canItBeUsed[number - 1] = True
                        listOfAvailableTroops.append((number, color))
                        break
            if ((canItBeUsed[9] and canItBeUsed[8] and canItBeUsed[7])
                    or (canItBeUsed[8] and canItBeUsed[7] and canItBeUsed[6])
                    or (canItBeUsed[7] and canItBeUsed[6] and canItBeUsed[5])
                    or (canItBeUsed[6] and canItBeUsed[5] and canItBeUsed[4])
                    or (canItBeUsed[5] and canItBeUsed[4] and canItBeUsed[3])
                    or (canItBeUsed[4] and canItBeUsed[3] and canItBeUsed[2])
                    or (canItBeUsed[3] and canItBeUsed[2] and canItBeUsed[1])
                    or (canItBeUsed[2] and canItBeUsed[1] and canItBeUsed[0])):
                listOfCards = [listOfAvailableTroops[
                    0], listOfAvailableTroops[1], listOfAvailableTroops[2]]
                return listOfCards
            else:
                return []

    def createHost(self, currentCards, playedCardList):
        listOfCards = currentCards[:]
        if len(listOfCards) == 3:
            return listOfCards
        neededCards = 3 - len(listOfCards)
        listOfAvailableTroops = []
        for number in range(10, 0, -1):
            for color in Identifiers.COLORS:
                if (number, color) not in playedCardList:
                    listOfAvailableTroops.append((number, color))
                    if len(listOfAvailableTroops) == neededCards:
                        listOfCards.append(listOfAvailableTroops[0])
                        if neededCards >= 2:
                            listOfCards.append(listOfAvailableTroops[1])
                        if neededCards >= 3:
                            listOfCards.append(listOfAvailableTroops[2])
                        return listOfCards
        # if it gets complete out of the loop, then there aren't enough cards
        # left to make a host.
        return []
