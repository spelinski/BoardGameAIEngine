class Player(object):

    def __init__(self, name):
        """
        Constructor
        @param name name of the player
        """
        self.name = name

    def take_turn(self):
        """
        Meant to be overridden by derived classes
        """
        raise NotImplementedError
