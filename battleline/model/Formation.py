class Formation(object):
    """
    A representation of a formation (three cards)
    """
    MAX_SIZE = 3
    def __init__(self, troops):
        """
        Constructor
        @param troops a list of three troops in the format (number, color)
        @raises FormationInvalidError if there are not 3 troops
        """
        if len(troops) != 3:
            raise FormationInvalidError
        self.troops = troops

    def get_numbers(self):
        """
        Return the numbers listed on the cards
        @return the numbers listed on the cards
        """
        return tuple(sorted(x[0] for x in self.troops))

    def get_colors(self):
        """
        Return the colors listed on the cards
        @return the colors listed on the cards
        """
        return tuple(x[1] for x in self.troops)

    def get_max_number(self):
        """
        Get the maximum number of the cards
        @return the maximum number of the cards
        """
        return max(self.get_numbers())

    def is_wedge(self):
        """
        Return true if we are a wedge (straight flush)
        @return if this formation is a wedge (straight flush)
        """
        return self.__is_in_order() and self.__is_same_color()

    def is_phalanx(self):
        """
        Return if we are a phalanx (three of a kind)
        @return if this formation is a phalanx(three of a kind)
        """
        return self.__is_same_number()

    def is_battalion(self):
        """
        Return if we are a battalion (flush)
        @return if this formation was a battalion(flush)
        """
        return self.__is_same_color()

    def is_skirmish(self):
        """
        Return if we are a skirmish (straight)
        @return if this formation was a skirmish (straight)
        """
        return self.__is_in_order()

    def is_host(self):
        """
        @Return if we are a host (sum)
        @return True, since everything can be a host
        """
        return True

    def __is_in_order(self):
        sorted_nums = sorted(self.get_numbers())
        return sorted_nums[0] == sorted_nums[1] - 1 and sorted_nums[1] == sorted_nums[2] - 1

    def __is_same_color(self):
        return self.__is_one_value(self.get_colors())

    def __is_same_number(self):
        return self.__is_one_value(self.get_numbers())

    def __is_one_value(self, list):
        return len(set(list)) == 1

    def __get_sum(self):
        return sum(self.get_numbers())

    def __does_match_type(self, other):
        # does not check host values
        return self.is_wedge() == other.is_wedge() and \
               self.is_phalanx() == other.is_phalanx() and \
               self.is_battalion() == other.is_battalion() and \
               self.is_skirmish() == other.is_skirmish()


    def is_equivalent_in_strength(self, other):
        if self.__does_match_type(other):
            return  self.__get_sum() == other.__get_sum()
        return False

    def is_greater_strength_than(self, other):
        if self.__does_match_type(other):
            return self.__get_sum() > other.__get_sum()
        if self.is_wedge(): return not other.is_wedge()
        if self.is_phalanx(): return not other.is_phalanx()
        if self.is_battalion(): return not other.is_battalion()
        if self.is_skirmish(): return not other.is_skirmish()



class FormationInvalidError(Exception):

    def __str__(self):
        """
        Return a error string
        @return error string
        """
        return "Formation must have 3 cards"
