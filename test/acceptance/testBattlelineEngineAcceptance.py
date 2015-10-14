import unittest
from battleline.engine.BattlelineEngine import BattlelineEngine
from test.battleline.engine.testBattlelineEngine import MockPlayer
from mechanics.Deck import Deck

class BattlelineEngineAcceptanceTest(unittest.TestCase):

    def test_can_run_complete_game(self):
        engine = BattlelineEngine(MockPlayer(), MockPlayer())
        engine.troop_deck = Deck(sorted(engine.get_troop_cards(), key=lambda x: (
            x[1], x[0]), reverse=True), shuffleDeck=False)
        while engine.get_winning_player() == None:
            engine.progress_turn()
        self.assertEquals(engine.get_winning_player(), "Player 1")
