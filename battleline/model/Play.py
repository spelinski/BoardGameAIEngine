

class Play(object):
    """
    A Play represents an individual action taken by a player.
    """

    def __init__(self, flag, card):
        """
        Constructor
        :param flag: The flag index that the card was used on.
        :param card: The TroopCard played.
        """
        self.flag = flag
        self.card = card

    @staticmethod
    def from_tuple(tuple):
        """
        For convenience, create an instace of Play from a
        two-length tuple containing the flag index and
        the card.
        :param tuple: A tuple of (flag,card)
        :return: A new Play instance
        """
        return Play(flag=tuple[0], card=tuple[1])
