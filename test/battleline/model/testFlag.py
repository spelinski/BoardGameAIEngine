import unittest
from battleline.model.Flag import Flag, InvalidPlayerError, Card, TooManyCardsOnOneSideError

class TestFlag(unittest.TestCase):
    def setUp(self):
        self.flag = Flag()

    def test_flag_is_empty_by_default(self):
        self.assertTrue(self.flag.is_empty())

    def test_flag_is_empty_by_player(self):
        self.assertTrue(self.flag.is_empty(Flag.PLAYER_ONE))
        self.assertTrue(self.flag.is_empty(Flag.PLAYER_TWO))

    def test_board_cannot_get_invalid_flags(self):
        self.assertRaisesRegexp(InvalidPlayerError, "Player String player3 is invalid", self.flag.is_empty, "player3")

    def test_flag_cannot_add_to_invalid_player(self):
        self.assertRaisesRegexp(InvalidPlayerError, "Player String player3 is invalid", self.flag.add_card, "player3", Card())

    def test_flag_player_and_global_not_empty_after_adding_card(self):
        self.flag.add_card(Flag.PLAYER_ONE, Card())
        self.assertFalse(self.flag.is_empty(Flag.PLAYER_ONE))
        self.assertTrue(self.flag.is_empty(Flag.PLAYER_TWO))
        self.assertFalse(self.flag.is_empty())

    def test_flag_can_not_add_more_than_tree_cards(self):
        for x in range(0,3): self.flag.add_card(Flag.PLAYER_ONE, Card())
        self.assertRaisesRegexp(TooManyCardsOnOneSideError, "Player player1 is attempting to add to many cards", self.flag.add_card, "player1", Card())
