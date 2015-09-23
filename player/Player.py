class Player(object):

    def __init__(self, name):
        """
        Constructor
        @param name name of the player
        """
        self.name = name

    def take_turn(self):
        raise NotImplementedError
