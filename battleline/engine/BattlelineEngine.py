class BattlelineEngine(object):
    """
    An engine that coordinates two players, a board and the decks for battleline
    """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
