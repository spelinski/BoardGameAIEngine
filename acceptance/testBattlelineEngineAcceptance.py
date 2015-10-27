import unittest
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.engine.BoardLogic import BoardLogic
from battleline.model.Play import Play
from battleline.player.BattlelinePlayer import Player


class MockPlayer(Player):

    def __init__(self, name):
        self.name = name

    def compute_turn(self, board, last_move):
        logic = BoardLogic(None)
        logic.board = board
        return Play(card=self.hand[0], flag=logic.get_first_playable_flag(self.direction))


class BattlelineEngineAcceptanceTest(unittest.TestCase):

    def test_can_run_complete_game(self):
        engine = BattlelineEngine(MockPlayer('r2d2'), MockPlayer('bb8'))
        engine.troop_deck = Deck(sorted(engine.get_troop_cards(), key=lambda x: (
            x[1], x[0]), reverse=True), shuffleDeck=False)
        engine.initialize()
        engine.run_until_game_end()
        self.assertEquals(engine.get_winning_player(), "south")
