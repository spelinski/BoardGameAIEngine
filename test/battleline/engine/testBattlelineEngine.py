import unittest
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import BattlelinePlayer
class TestBattlelineEngine(unittest.TestCase):

    def test_can_create_engine_with_two_players(self):
        engine = BattlelineEngine(BattlelinePlayer("1"), BattlelinePlayer("2"))
        self.assertEquals("1", engine.player1.name)
        self.assertEquals("2", engine.player2.name)
