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
        self.numbers = tuple(sorted(x[0] for x in self.troops))
        self.colors = tuple(x[1] for x in self.troops)
        self.type = self.__get_type()

    def __get_type(self):
        if self.__is_wedge():
            return "wedge"
        if self.__is_phalanx():
            return "phalanx"
        if self.__is_battalion():
            return "battalion"
        if self.__is_skirmish():
            return "skirmish"
        return "host"

    def get_numbers(self):
        """
        Return the numbers listed on the cards
        @return the numbers listed on the cards
        """
        return self.numbers

    def get_colors(self):
        """
        Return the colors listed on the cards
        @return the colors listed on the cards
        """
        return self.colors

    def get_max_number(self):
        """
        Get the maximum number of the cards
        @return the maximum number of the cards
        """
        return max(self.get_numbers())

    def __is_wedge(self):
        return self.__is_in_order() and self.__is_same_color()

    def __is_phalanx(self):
        return self.__is_same_number()

    def __is_battalion(self):
        return self.__is_same_color()

    def __is_skirmish(self):
        return self.__is_in_order()

    def __is_in_order(self):
        return self.numbers[0] == self.numbers[1] - 1 and self.numbers[1] == self.numbers[2] - 1

    def __is_same_color(self):
        return self.__is_one_value(self.colors)

    def __is_same_number(self):
        return self.__is_one_value(self.numbers)

    def __is_one_value(self, list):
        return len(set(list)) == 1

    def __get_sum(self):
        return sum(self.numbers)

    def __does_match_type(self, other):
        # does not check host values
        return self.type == other.type

    def is_equivalent_in_strength(self, other):
        """
        Check if the two armies are equivalent in strength
        @param other the other formation
        @return true if the two armies are the same type and have the same sum
        """
        if self.__does_match_type(other):
            return self.__get_sum() == other.__get_sum()
        return False

    def is_greater_strength_than(self, other):
        """
        Check if the one formation is greater than the other
        @param other the other formation
        @return true if the two armies are the same type and this has the greater sum, otherwise, whoever has the greater formation
        """
        if self.__does_match_type(other):
            return self.__get_sum() > other.__get_sum()
        return self.__get_ordered_strength() > other.__get_ordered_strength()

    def __get_ordered_strength(self):
        strength = ["host", "skirmish", "battalion", "phalanx", "wedge"]
        return strength.index(self.type)


class FormationInvalidError(Exception):

    def __str__(self):
        """
        Return a error string
        @return error string
        """
        return "Formation must have 3 cards"
