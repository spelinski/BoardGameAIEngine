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

class FormationInvalidError(Exception):

    def __str__(self):
        """
        Return a error string
        @return error string
        """
        return "Formation must have 3 cards"
