from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.Identifiers import Identifiers
from collections import namedtuple
TroopCard = namedtuple("TroopCard", ["number", "color"])

COLORS = Identifiers.COLORS


class BoardLogic:

    def __init__(self):
        self.playedCardList = []
        self.formationLogic = FormationLogic()
        self.board = Board()
        self.winner = None

    def addCard(self, flag, player, card):
        self.board.flags[flag].add_card(player, card)
        self.playedCardList.append(card)
        self.checkAllFlags(player)
        self.__check_winning_conditions()

    def is_flag_playable(self, flag_index, direction):
        return self.board.flags[flag_index].is_playable(direction)

    def __check_winning_conditions(self):
        self.__check_for_envelopment()
        self.__check_for_breakthrough()

    def __check_for_envelopment(self):
        for player in [Identifiers.NORTH, Identifiers.SOUTH]:
            numClaimedFlags = len(filter( lambda flag: flag.is_claimed_by_player(player), self.board.flags))
            if numClaimedFlags == 5:
                self.winner = player

    def __check_for_breakthrough(self):
        pass

    def is_game_over(self):
        return self.winner != None

    def get_game_winner(self):
        return self.winner

    def checkAllFlags(self, latestPlayer):
        # get the best possible formation for an empty set because there should
        # be a lot of those requested
        bestFormationPossible = self.formationLogic.greatestPossibleFormation(
            [], self.playedCardList)
        unclaimedFlags = (
            flag for flag in self.board.flags if not flag.is_claimed())
        for flag in unclaimedFlags:
            for player in [Identifiers.NORTH, Identifiers.SOUTH]:
                if player == Identifiers.NORTH:
                    enemy = Identifiers.SOUTH
                else:
                    enemy = Identifiers.NORTH
                playerCards = flag.get_cards(player)
                enemyCards = flag.get_cards(enemy)
                if len(flag.get_cards(player)) == 3:
                    # the flag needs to be checked
                    if len(enemyCards) == 0:
                        if self.formationLogic.getTheBetterFormation(playerCards, bestFormationPossible) == playerCards:
                            flag.claim(player)
                    else:
                        bestEnemyFormation = self.formationLogic.greatestPossibleFormation(
                            enemyCards, self.playedCardList)
                        if self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation) == playerCards:
                            flag.claim(player)
                        if self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation) == bestEnemyFormation and self.formationLogic.getTheBetterFormation(bestEnemyFormation, playerCards) == playerCards:
                            # the latestPlayer loses
                            if latestPlayer == Identifiers.NORTH:
                                flag.claim(Identifiers.SOUTH)
                            else:
                                flag.claim(Identifiers.NORTH)
