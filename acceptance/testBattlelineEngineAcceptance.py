import unittest
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.Player import Player

class MockPlayer(Player):

    def compute_turn(self, board, last_move):
        return Play(card=self.hand[0], flag=self.next_flag)


class BattlelineEngineAcceptanceTest(unittest.TestCase):

    def test_can_run_complete_game(self):
        engine = BattlelineEngine(MockPlayer(), MockPlayer())
        engine.troop_deck = Deck(sorted(engine.get_troop_cards(), key=lambda x: (
            x[1], x[0]), reverse=True), shuffleDeck=False)
        engine.run_until_game_end()
        while engine.get_winning_player() == None:
            engine.progress_turn()
        self.assertEquals(engine.get_winning_player(), "Player 1")
