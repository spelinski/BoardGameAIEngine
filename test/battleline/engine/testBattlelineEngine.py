import unittest
from itertools import product
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine, TroopCard
from battleline.player.BattlelinePlayer import BattlelinePlayer
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication

class TestBattlelineEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BattlelineEngine(BattlelinePlayer("1", MockPlayerCommunication()), BattlelinePlayer("2", MockPlayerCommunication))

        #reinitialize the deck with a non shuffled deck to make things more reliable
        #don't do this in production code, the deck should be shuffled in real code
        self.engine.troop_deck = Deck(sorted(self.engine.get_troop_cards(), reverse=True), shuffleDeck=False)

    def test_can_create_engine_with_two_players(self):
        self.assertEquals("1", self.engine.player1.name)
        self.assertEquals("2", self.engine.player2.name)
        self.assertEquals([], self.engine.player1.hand)
        self.assertEquals([], self.engine.player2.hand)


    def test_board_deck_should_have_all_sixty_cards_to_start_with(self):
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        all_troops =  [TroopCard(name,number) for name,number in sorted(product(colors, range(1,11)), reverse=True)]
        return sorted(all_troops) == sorted(self.engine.troop_deck.deck)

    def test_each_player_starts_with_7_cards_after_initialization(self):
        self.engine.initialize()
        self.assertEquals([TroopCard("BLUE", 1),
                           TroopCard("BLUE", 3),
                           TroopCard("BLUE", 5),
                           TroopCard("BLUE", 7),
                           TroopCard("BLUE", 9),
                           TroopCard("GREEN", 1),
                           TroopCard("GREEN", 3)], self.engine.player1.hand)
        self.assertEquals([TroopCard("BLUE", 2),
                           TroopCard("BLUE", 4),
                           TroopCard("BLUE", 6),
                           TroopCard("BLUE", 8),
                           TroopCard("BLUE", 10),
                           TroopCard("GREEN", 2),
                           TroopCard("GREEN", 4)], self.engine.player2.hand)
