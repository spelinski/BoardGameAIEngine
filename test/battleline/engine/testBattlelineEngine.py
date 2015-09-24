import unittest
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import BattlelinePlayer

from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
class TestBattlelineEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BattlelineEngine(BattlelinePlayer("1", MockPlayerCommunication()), BattlelinePlayer("2", MockPlayerCommunication()))

    def test_can_create_engine_with_two_players(self):
        self.assertEquals("1", self.engine.player1.name)
        self.assertEquals("2", self.engine.player2.name)

    def test_board_deck_should_have_all_sixty_cards_to_start_with(self):
        #add a test in here once we have a deck working
        pass

    def test_each_player_starts_with_7_cards(self):
        self.assertEquals(7, len(self.engine.player1.hand))
        self.assertEquals(7, len(self.engine.player2.hand))
