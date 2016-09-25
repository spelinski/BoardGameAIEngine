import unittest
from dominion.model.Player import Player, CardNotInHandException
from dominion import Identifiers
from mock import Mock

class TestPlayerModel(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def gain_cards(self, num_to_gain):
        self.player.gain_cards(range(num_to_gain))

    def test_player_discard_pile_is_empty_by_default(self):
        self.assertEquals([], self.player.get_discard_pile())

    def test_player_can_gain_cards(self):
        self.player.gain_cards([1])
        self.assertEquals([1], self.player.get_discard_pile())

        self.player.gain_cards([2])
        self.assertEquals([1,2], self.player.get_discard_pile())

        self.player.gain_cards([3,4])
        self.assertEquals([1,2,3,4], self.player.get_discard_pile())

    def test_players_hand_is_empty_by_default(self):
        self.assertEquals([], self.player.get_hand())

    def test_can_get_top_discard_card(self):
        self.assertIsNone(self.player.get_top_discard_card())

        self.player.gain_cards([1])
        self.assertEquals(1, self.player.get_top_discard_card())

        self.player.gain_cards([2])
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
            self.player.gain_cards([turn])
            self.player.cleanup()
            self.player.draw_cards(5)

        self.assertEquals(range(20), sorted(self.player.get_hand() + self.player.get_discard_pile() + self.player.get_deck_cards()))

    def test_player_can_add_to_hand(self):
        self.player.add_to_hand(2)
        self.player.add_to_hand(3)
        self.assertEquals([2,3], self.player.get_hand())

    def test_is_in_hand(self):
        self.assertFalse(self.player.is_in_hand(2))
        self.player.add_to_hand(2)
        self.assertFalse(self.player.is_in_hand(3))
        self.assertTrue(self.player.is_in_hand(2))


    def test_discard_puts_card_from_hand_to_discard_pile(self):
        self.player.add_to_hand(2)
        self.player.add_to_hand(3)
        self.player.discard(2)
        self.assertEquals([2], self.player.get_discard_pile())
        self.assertEquals([3], self.player.get_hand())

    def test_discard_multiple(self):
        for i in range(3):
            self.player.add_to_hand(i)
        self.player.discard_multiple([0,2])
        self.assertEquals([0,2], self.player.get_discard_pile())
        self.assertEquals([1], self.player.get_hand())

    def test_discard_throws_exception_if_card_not_in_hand(self):
        with self.assertRaisesRegexp(CardNotInHandException, "4 is not in the hand"):
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
            self.player.gain_cards(["copper"])
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

    def test_player_can_only_play_cards_from_hand(self):
        with self.assertRaises(CardNotInHandException):
            self.player.play_card("copper")

    def test_player_can_cleanup_from_played_cards(self):
        for _ in range(5):
            self.player.put_card_on_top_of_deck("copper")
        self.player.add_to_hand("silver")
        self.player.add_to_hand("gold")
        self.player.add_to_hand("province")
        self.player.play_card("silver")
        self.player.cleanup("silver")
        self.assertEquals("silver", self.player.get_top_discard_card())
        self.assertEquals([], self.player.get_played_cards())

    def test_player_communication_send_and_receive(self):
        mock_comm = Mock()
        mock_comm.hit_send = False
        mock_comm.hit_respond = False

        def send_message(msg):
            self.assertEquals("hello", msg)
            mock_comm.hit_send = True

        def get_response():
            mock_comm.hit_respond = True
            return ""

        mock_comm.send_message = send_message
        mock_comm.get_response = get_response
        self.player.set_communication(mock_comm)
        self.assertEquals("", self.player.send_message_and_await_response("hello"))
        self.assertTrue(mock_comm.hit_send)
        self.assertTrue(mock_comm.hit_respond)

    def test_player_communication_close(self):
        mock_comm = Mock()
        mock_comm.hit_close = False

        def close():
            mock_comm.hit_close = True

        mock_comm.close = close
        self.player.close_communication()
        self.assertFalse(mock_comm.hit_close)

        self.player.set_communication(mock_comm)
        self.player.close_communication()

        self.assertTrue(mock_comm.hit_close)

    def test_player_communication_send_only(self):
        mock_comm = Mock()
        mock_comm.hit_send = False
        mock_comm.hit_respond = False

        def send_message(msg):
            self.assertEquals("hello", msg)
            mock_comm.hit_send = True

        def get_response():
            self.fail()

        mock_comm.send_message = send_message
        mock_comm.get_response = get_response
        self.player.set_communication(mock_comm)
        self.player.send_message("hello")
        self.assertTrue(mock_comm.hit_send)

    def test_player_can_mark_turn_taken(self):
        self.assertEquals(0, self.player.get_number_of_turns_taken())
        self.player.mark_turn_taken()
        self.assertEquals(1, self.player.get_number_of_turns_taken())
        self.player.mark_turn_taken()
        self.assertEquals(2, self.player.get_number_of_turns_taken())

    def test_player_can_get_score_from_all_card_piles(self):
        self.assertEquals(0, self.player.get_score())
        self.player.add_to_hand(Identifiers.ESTATE)
        self.assertEquals(1, self.player.get_score())
        self.player.gain_cards([Identifiers.PROVINCE])
        self.assertEquals(7, self.player.get_score())
        self.player.put_card_on_top_of_deck(Identifiers.DUCHY)
        self.assertEquals(10, self.player.get_score())

    def test_player_can_get_notified_if_shuffles(self):
        listener = Mock()
        listener.hit_notify = False
        def notify(message):
            self.assertEquals("shuffle-deck", message.type)
            listener.hit_notify = True
        listener.notify = notify
        self.player.gain_cards([Identifiers.COPPER])
        self.player.add_event_listener(listener)
        self.player.draw_cards(1)
        self.assertTrue(listener.hit_notify)

    def test_player_can_get_notified_if_gains_cards(self):
        listener = Mock()
        listener.hit_notify = False
        def notify(message):
            self.assertEquals("gained-cards", message.type)
            self.assertEquals([Identifiers.COPPER], message.cards)
            listener.hit_notify = True
        listener.notify = notify
        self.player.add_event_listener(listener)
        self.player.gain_cards([Identifiers.COPPER])
        self.assertTrue(listener.hit_notify)

    def test_player_can_get_notified_if_cleanup(self):
        listener = Mock()
        listener.hit_notify = False
        top_discard = Identifiers.CURSE
        hand_list = [Identifiers.CURSE] * 3
        played_list = [Identifiers.COPPER] * 3
        def notify(message):
            self.assertIn(message.type, ("discard-card", "played-cards"))
            if getattr(message, 'card', False):
                self.assertEquals(top_discard, message.card)
            if getattr(message, 'cards', False):
                self.assertEquals(played_list, message.cards)
            listener.hit_notify = True
        listener.notify = notify
        self.player.add_event_listener(listener)
        self.player.hand = hand_list
        self.player.played = played_list
        self.player.cleanup(top_discard)
        self.assertTrue(listener.hit_notify)
