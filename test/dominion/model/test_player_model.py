import unittest
from dominion.model.Player import Player

class TestPlayerModel(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def test_player_discard_pile_is_empty_by_default(self):
        self.assertEquals([], self.player.get_discard_pile())

    def test_player_can_gain_cards(self):
        self.player.gain_card(1)
        self.assertEquals([1], self.player.get_discard_pile())

        self.player.gain_card(2)
        self.assertEquals([1,2], self.player.get_discard_pile())

    def test_players_hand_is_empty_by_default(self):
        self.assertEquals([], self.player.get_hand())

    def test_can_get_top_discard_card(self):
        self.assertIsNone(self.player.get_top_discard_card())

        self.player.gain_card(1)
        self.assertEquals(1, self.player.get_top_discard_card())

        self.player.gain_card(2)
        self.assertEquals(2, self.player.get_top_discard_card())


    def test_player_can_draw_initial_hand_of_five(self):
        for x in range(5):
            self.player.gain_card(x)
        self.player.draw_cards(5)

        self.assertEquals([], self.player.get_discard_pile())
        self.assertEquals(range(5), sorted(self.player.get_hand()))

    def test_player_can_keep_drawing_through_deck(self):
        for x in range(12):
            self.player.gain_card(x)

        self.player.draw_cards(5)
        self.player.cleanup()
        self.player.draw_cards(5)

        self.assertEquals(5, len(self.player.get_discard_pile()))
        self.assertEquals(2, len(self.player.get_deck_cards()))
        self.assertEquals(5, len(self.player.get_hand()))
        self.assertEquals(range(12), sorted(self.player.get_hand() + self.player.get_discard_pile() + self.player.get_deck_cards()))
