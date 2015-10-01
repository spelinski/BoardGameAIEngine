from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.view.Output import COLORS
from collections import namedtuple
TroopCard = namedtuple("TroopCard", ["number", "color"])



class BoardLogic:
    def __init__(self):
        self.playedCardList = []
        self.formationLogic = FormationLogic()
        self.board = Board()
        self.PLAYER_NORTH = self.board.flags[0].PLAYER_NORTH
        self.PLAYER_SOUTH = self.board.flags[0].PLAYER_SOUTH

    def addCard(self,flag,player,card):
        self.board.flags[flag].add_card(player,card)
        self.playedCardList.append(card)
        self.checkAllFlags(player)

    def checkAllFlags(self,latestPlayer):
        # get the best possible formation for an empty set because there should
        # be a lot of those requested
        bestFormationPossible = self.formationLogic.greatestPossibleFormation([], self.playedCardList)
        unclaimedFlags = (flag for flag in self.board.flags if not flag.is_claimed())
        for flag in unclaimedFlags:
            for player in [self.PLAYER_NORTH, self.PLAYER_SOUTH]:
                if player == self.PLAYER_NORTH:
                    enemy = self.PLAYER_SOUTH
                else:
                    enemy = self.PLAYER_NORTH
                playerCards = flag.get_cards(player)
                enemyCards = flag.get_cards(enemy)
                if len(flag.get_cards(player)) == 3:
                    # the flag needs to be checked
                    if len(enemyCards) == 0:
                        if self.formationLogic.getTheBetterFormation(playerCards, bestFormationPossible) == playerCards:
                            flag.claim(player)
                    else:
                        bestEnemyFormation = self.formationLogic.greatestPossibleFormation(enemyCards,self.playedCardList)
                        if self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation ) == playerCards:
                            flag.claim(player)
                        if self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation ) == bestEnemyFormation and self.formationLogic.getTheBetterFormation(bestEnemyFormation, playerCards) == playerCards:
                            #the latestPlayer loses
                            if latestPlayer == self.PLAYER_NORTH:
                                flag.claim(self.PLAYER_SOUTH)
                            else:
                                flag.claim(self.PLAYER_NORTH)

