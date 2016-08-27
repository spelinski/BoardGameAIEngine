import unittest
from dominion.model.Player import Player, CardNotInHandException

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

    def test_player_can_add_to_hand(self):
        self.player.add_to_hand(2)
        self.player.add_to_hand(3)
        self.assertEquals([2,3], self.player.get_hand())

    def test_discard_puts_card_from_hand_to_discard_pile(self):
        self.player.add_to_hand(2)
        self.player.add_to_hand(3)
        self.player.discard(2)
        self.assertEquals([2], self.player.get_discard_pile())
        self.assertEquals([3], self.player.get_hand())

    def test_discard_throws_exception_if_card_not_in_hand(self):
        with self.assertRaises(CardNotInHandException):
            self.player.discard(4)

        self.player.add_to_hand(5)
        with self.assertRaises(CardNotInHandException):
            self.player.discard(4)

    def test_trashing_card_from_hand(self):
        self.player.add_to_hand(2)
        self.player.add_to_hand(3)
        self.player.trash(2)
        self.assertEquals([], self.player.get_discard_pile())
        self.assertEquals([3], self.player.get_hand())

    def test_trash_throws_exception_if_card_not_in_hand(self):
        with self.assertRaises(CardNotInHandException):
            self.player.trash(4)

        self.player.add_to_hand(5)
        with self.assertRaises(CardNotInHandException):
            self.player.trash(4)

    def test_can_put_on_top_of_deck(self):
        for _ in range(10):
            self.player.gain_card("copper")
        self.player.draw_cards(5)
        self.player.put_card_on_top_of_deck("silver")
        self.player.draw_cards(1)
        self.assertEquals(["copper", "copper", "copper", "copper", "copper", "silver"], self.player.get_hand())

    def test_can_specify_top_card_when_cleaning_up(self):
        for _ in range(5):
            self.player.put_card_on_top_of_deck("copper")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("gold")
        self.player.add_to_hand("province")
        self.player.cleanup("gold")
        self.assertEquals("gold", self.player.get_top_discard_card())

    def test_can_specify_different_top_card_when_cleaning_up(self):
        for _ in range(5):
            self.player.put_card_on_top_of_deck("copper")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("gold")
        self.player.add_to_hand("province")
        self.player.cleanup("silver")
        self.assertEquals("silver", self.player.get_top_discard_card())

    def test_card_is_picked_if_top_not_specified_on_cleanup(self):
        for _ in range(5):
            self.player.put_card_on_top_of_deck("copper")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("gold")
        self.player.add_to_hand("province")
        self.player.cleanup()
        self.assertTrue(self.player.get_top_discard_card() in ["silver", "gold", "province"])

    def test_card_is_picked_if_top_not_in_hand_on_cleanup(self):
        for _ in range(5):
            self.player.put_card_on_top_of_deck("copper")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("gold")
        self.player.add_to_hand("province")
        self.player.cleanup("copper")
        self.assertTrue(self.player.get_top_discard_card() in ["silver", "gold", "province"])

    def test_card_is_picked_if_top_has_multiples(self):
        for _ in range(5):
            self.player.put_card_on_top_of_deck("copper")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("gold")
        self.player.add_to_hand("province")
        self.player.cleanup("silver")
        self.assertTrue("silver" == self.player.get_top_discard_card())

    def test_player_can_play_cards(self):
        self.player.add_to_hand("copper")
        self.player.play_card("copper")
        self.assertEquals([], self.player.get_hand())
        self.assertEquals(["copper"], self.player.get_played_cards())
