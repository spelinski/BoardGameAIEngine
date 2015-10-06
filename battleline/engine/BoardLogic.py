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

    def addCard(self, flag, player, card):
        self.board.flags[flag].add_card(player, card)
        self.playedCardList.append(card)
        self.checkAllFlags(player)

    def is_flag_playable(self, flag_index, direction):
        return self.board.flags[flag_index].is_playable(direction)

    def checkAllFlags(self, latestPlayer):
        # get the best possible formation for an empty set because there should
        # be a lot of those requested
        unclaimedFlags = (
            flag for flag in self.board.flags if not flag.is_claimed())
        for flag in unclaimedFlags:
            for player in [Identifiers.NORTH, Identifiers.SOUTH]:
                if len(flag.get_cards(player)) == 3:
                    self.__try_to_claim_flag(flag, player, latestPlayer)

    def __try_to_claim_flag(self, flag, player, latestPlayer):
        enemy = self.__get_enemy(player)
        playerCards = flag.get_cards(player)
        enemyCards = flag.get_cards(enemy)
        # the flag needs to be checked
        if len(enemyCards) == 0:
            bestFormationPossible = self.formationLogic.greatestPossibleFormation(
                [], self.playedCardList)
            self.__claim_flag_if_player_formation_is_best()
        else:
            bestEnemyFormation = self.formationLogic.greatestPossibleFormation(
                enemyCards, self.playedCardList)
            self.__claim_flag_if_player_formation_is_best(
                playerCards, bestEnemyFormation, flag, player)
            # if self.__is_current_player_formation_best(playerCards, bestEnemyFormation):
            #   flag.claim(player)
            # Need to think about changing getTheBetterFormation to not depend
            # on which is passed first to dectect equal strength
            if self.__is_enemy_formation_best(playerCards, bestEnemyFormation) and self.__is_enemy_formation_best(bestEnemyFormation, playerCards):
                # the latestPlayer loses
                if latestPlayer != player:
                    flag.claim(player)

    def __claim_flag_if_player_formation_is_best(self, playerCards, bestEnemyFormation, flag, player):
        if self.__is_current_player_formation_best(playerCards, bestEnemyFormation):
            flag.claim(player)

    def __is_current_player_formation_best(self, playerCards, bestEnemyFormation):
        return (self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation) == playerCards)

    def __is_enemy_formation_best(self, playerCards, bestEnemyFormation):
        return (self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation) == bestEnemyFormation)

    def __get_enemy(self, player):
        return Identifiers.SOUTH if (player == Identifiers.NORTH) else Identifiers.NORTH
