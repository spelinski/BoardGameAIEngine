from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.Identifiers import Identifiers
from itertools import product, groupby


class BoardLogic:

    def __init__(self, engine):
        """
        Constructor
        """
        self.playedCardList = []
        self.formationLogic = FormationLogic()
        self.board = Board()
        self.winner = None
        self.engine = engine

    def addCard(self, flag, player, card):
        """
        add card to players side of the flag
        @param flag the flag being added to
        @param player direction string north/south
        @param card the card to be added
        """
        self.board.flags[flag].add_card(player, card)
        self.engine.output_handler.play_action(player, card, flag + 1)
        self.latestPlayer = player


    def is_any_flag_playable(self,  direction):
        """
        Check if any flag can be played
        @param direction the side of the flag to check
        """
        return any(flag.is_playable(direction) for flag in  self.board.flags)

    def is_flag_playable(self, flag_index, direction):
        """
        Check if a flag can be played on
        @param flag_index the index of the flag being checked
        @param direction the side of the flag to check
        """
        return self.board.flags[flag_index].is_playable(direction)

    def __check_winning_conditions(self):
        self.__check_for_envelopment()
        self.__check_for_breakthrough()

    def __get_flags_claimed_by_player(self, player):
        return [flag.is_claimed_by_player(player) for flag in self.board.flags]

    def __check_for_envelopment(self):
        for player in [Identifiers.NORTH, Identifiers.SOUTH]:
            numClaimedFlags = len(
                [x for x in self.__get_flags_claimed_by_player(player) if x])
            if numClaimedFlags >= 5:
                self.winner = player
                self.engine.output_handler.declare_winner(player)

    def __check_for_breakthrough(self):
        for player in [Identifiers.NORTH, Identifiers.SOUTH]:
            claimedFlags = self.__get_flags_claimed_by_player(player)
            consecutiveFlags = [i for i in [
                list(g) for _, g in groupby(claimedFlags)] if len(i) >= 3]
            consecutiveClaimedFlags = [
                claimed for claimed in consecutiveFlags if claimed[0]]
            if len(consecutiveClaimedFlags) > 0:
                self.winner = player
                self.engine.output_handler.declare_winner(player)

    def checkAllFlags(self):
        """
        iterates through all of the unclaimed flags checking to see if anymore can be claimed
        @param latestPlayer the last player that has played a card
        """
        unclaimedFlags = (
            (index, flag) for index, flag in enumerate(self.board.flags) if not flag.is_claimed())
        for indexed_flag, player in product(unclaimedFlags, [Identifiers.NORTH, Identifiers.SOUTH]):
            self.__check_individual_flag(indexed_flag, player)
        self.__check_winning_conditions()

    def __check_individual_flag(self, indexed_flag, player):
        """
        check if the individual flag is ready to be claimed
        @param flag the flag to be checked
        @param player which player to see if they can claim it
        """
        index, flag = indexed_flag
        playerCards = flag.get_cards(player)
        if len(playerCards) == flag.MAX_CARDS_PER_SIDE:
            enemyCards = flag.get_cards(self.__get_enemy(player))
            bestEnemyFormation = self.formationLogic.get_best_formation(
                enemyCards, self.engine.get_unplayed_cards())
            if self.formationLogic.is_equivalent_in_strength(playerCards, bestEnemyFormation):
                if len(enemyCards) != flag.MAX_CARDS_PER_SIDE or self.latestPlayer != player:
                    flag.claim(player)
                    self.engine.output_handler.claim_action(
                        player, flagNumber=index + 1)
            elif self.formationLogic.getTheBetterFormation(playerCards, bestEnemyFormation) == playerCards:
                flag.claim(player)
                self.engine.output_handler.claim_action(
                    player, flagNumber=index + 1)

    def __get_enemy(self, player):
        """
        get the other player than the one given
        @param player
        """
        return Identifiers.SOUTH if (player == Identifiers.NORTH) else Identifiers.NORTH

    def get_first_playable_flag(self, direction):
        """
        Find the first flag playable from this direction
        @return the first flag playable, None otherwise
        """
        return next((f for f in xrange(1, 10) if self.is_flag_playable(f - 1, direction)), None)
