from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.Identifiers import Identifiers
from itertools import product


class BoardLogic:

    def __init__(self):
        """
        Constructor
        """
        self.playedCardList = []
        self.formationLogic = FormationLogic()
        self.board = Board()

    def addCard(self, flag, player, card):
        """
        add card to players side of the flag
        @param flag the flag being added to
        @param player direction string north/south
        @param card the card to be added
        """
        self.board.flags[flag].add_card(player, card)
        self.playedCardList.append(card)
        self.checkAllFlags(player)

    def is_flag_playable(self, flag_index, direction):
        """
        Check if a flag can be played on
        @param flag_index the index of the flag being checked
        @param direction the side of the flag to check
        """
        return self.board.flags[flag_index].is_playable(direction)

    def checkAllFlags(self, latestPlayer):
        """
        iterates through all of the unclaimed flags checking to see if anymore can be claimed
        @param latestPlayer the last player that has played a card
        """
        self.latestPlayer = latestPlayer
        unclaimedFlags = (
            flag for flag in self.board.flags if not flag.is_claimed())
        for flag, player in product(unclaimedFlags, [Identifiers.NORTH, Identifiers.SOUTH]):
            self.__check_individual_flag(flag, player)

    def __check_individual_flag(self, flag, player):
        """
        check if the individual flag is ready to be claimed
        @param flag the flag to be checked
        @param player which player to see if they can claim it
        """
        playerCards = flag.get_cards(player)
        if len(playerCards) == flag.MAX_CARDS_PER_SIDE:
            enemyCards = flag.get_cards(self.__get_enemy(player))
            bestEnemyFormation = self.formationLogic.greatestPossibleFormation(
                enemyCards, self.playedCardList)
            if self.formationLogic.is_equivalent_in_strength(playerCards, bestEnemyFormation):
                if len(enemyCards) != flag.MAX_CARDS_PER_SIDE or self.latestPlayer != player:
                    flag.claim(player)
            elif self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation) == playerCards:
                flag.claim(player)

    def __get_enemy(self, player):
        """
        get the other player than the one given
        @param player
        """
        return Identifiers.SOUTH if (player == Identifiers.NORTH) else Identifiers.NORTH
