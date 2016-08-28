from dominion.Identifiers import *
from dominion.model.Supply import *
class DominionEngine(object):

    def __init__(self, players, game_set):
        self.players = players
        self.supply = Supply(len(players), game_set)

    def run_until_game_end(self):
        pass

    
