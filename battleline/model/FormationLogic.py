from Board import Board
from battleline.Identifiers import Identifiers, TroopCard
from Formation import Formation
import itertools


class FormationLogic:
    """ A class to compare formations and infer what formations are better than others"""

    def getTheBetterFormation(self, formation1, formation2):
        """
        returns the better formation
        @param formation1 first formation
        @param formation2 second formation
        @return formation1 if its better than formation2 else formation2
        """
        return formation1 if Formation(formation1).is_greater_strength_than(Formation(formation2)) else formation2

    def is_equivalent_in_strength(self, formation1, formation2):
        """
        returns if two formations have equal strength
        @param formation1 first formation
        @param formation2 second formation
        @return if both formations have equal srength
        """
        return Formation(formation1).is_equivalent_in_strength(Formation(formation2))

    def get_best_formation(self, current_formation, unplayed_cards):
        """
        Get the best possible formation based on the current formation and the cards yet to be played
        @param the current formation (length 0 to 3)
        @param unplayed_cards cards that have not been played yet
        @return the best possible formation
        """
        return self.__get_best_option([card for card in current_formation], unplayed_cards)

    def __get_best_option(self, options, unplayed_cards):
        if len(options) == 3:
            return options
        else:
            return self.__get_max_strength_formation(options, unplayed_cards)

    def __get_max_strength_formation(self, options, unplayed_cards):
        number_of_cards_left = 3 - len(options)
        max_formation = self.__get_minimum_strength_formation()
        max_formation_object = Formation(max_formation)
        for combo in itertools.combinations(unplayed_cards, number_of_cards_left):
            formation = options + list(combo)
            if Formation(formation).is_greater_strength_than(max_formation_object):
                max_formation = formation
                max_formation_object = Formation(formation)
        return max_formation

    def __get_minimum_strength_formation(self):
        return [TroopCard(1, Identifiers.COLORS[0]), TroopCard(1, Identifiers.COLORS[1]), TroopCard(0, Identifiers.COLORS[0])]
