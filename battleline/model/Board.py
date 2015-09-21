from Flag import Flag
class Board(object):
    """Represent a board in Battleline.
    A board is represented as 9 flags, each with 3 potential slots on the top and bottom
    """

    def __is_flag_in_range(self,index):
        return index in range(1,11)

    def get_flag(self, flag_index):
        """Get the Flag associated with the index"""
        if not self.__is_flag_in_range(flag_index):
            raise FlagNotFoundError(flag_index)

        return Flag()

class FlagNotFoundError(Exception):
    def __init__(self, flag_index):
        """Create an Exception that the index is not valid
        @param flag_index the index of the flag that was not valid
        """
        self.index = flag_index

    def __str__(self):
        return "Flag Index {} is invalid".format(self.index)
