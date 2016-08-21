import unittest
from dominion.model.Player import Player

class TestPlayerModel(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def gain_cards(self, num_to_gain):
        for x in range(num_to_gain):
            self.player.gain_card(x)

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
        self.gain_cards(5)
        self.player.draw_cards(5)

        self.assertEquals([], self.player.get_discard_pile())
        self.assertEquals(range(5), sorted(self.player.get_hand()))

    def test_player_can_draw_hand_if_less_than_five(self):
        self.gain_cards(3)
        self.player.draw_cards(5)

        self.assertEquals([], self.player.get_discard_pile())
        self.assertEquals(range(3), sorted(self.player.get_hand()))

    def test_player_can_keep_drawing_through_deck(self):
        self.gain_cards(12)

        self.player.draw_cards(5)
        self.player.cleanup()
        self.player.draw_cards(5)

        self.assertEquals(5, len(self.player.get_discard_pile()))
        self.assertEquals(2, len(self.player.get_deck_cards()))
        self.assertEquals(5, len(self.player.get_hand()))
        self.assertEquals(range(12), sorted(self.player.get_hand() + self.player.get_discard_pile() + self.player.get_deck_cards()))


    def test_player_can_keep_drawing_through_deck_multiple_turns(self):
        self.gain_cards(10)
        self.player.draw_cards(5)

        for turn in xrange(10, 20):
            self.player.gain_card(turn)
            self.player.cleanup()
            self.player.draw_cards(5)

        self.assertEquals(range(20), sorted(self.player.get_hand() + self.player.get_discard_pile() + self.player.get_deck_cards()))

    def test_player_can_gain_to_hand(self):
        self.player.add_to_hand(2)
        self.player.add_to_hand(3)
        self.assertEquals([2,3], self.player.get_hand())
