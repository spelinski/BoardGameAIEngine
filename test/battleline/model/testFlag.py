import unittest
from battleline.model.Flag import Flag, InvalidPlayerError, TooManyCardsOnOneSideError, FlagAlreadyClaimedError

class TestFlag(unittest.TestCase):
    def setUp(self):
        self.flag = Flag()
        self.card = "dummyCard"

    def test_flag_is_empty_by_default(self):
        self.assertTrue(self.flag.is_empty())

    def test_flag_is_empty_by_player(self):
        self.assertTrue(self.flag.is_player_side_empty(Flag.PLAYER_ONE_ID))
        self.assertTrue(self.flag.is_player_side_empty(Flag.PLAYER_TWO_ID))

    def test_board_cannot_get_invalid_flags(self):
        self.assertRaisesRegexp(InvalidPlayerError, "Player String player3 is invalid", self.flag.is_player_side_empty, "player3")

    def test_board_cannot_get_is_flag_playable_on_invalid_player(self):
        self.assertRaisesRegexp(InvalidPlayerError, "Player String player3 is invalid", self.flag.is_flag_playable, "player3")

    def test_flag_cannot_add_to_invalid_player(self):
        self.assertRaisesRegexp(InvalidPlayerError, "Player String player3 is invalid", self.flag.add_card, "player3", self.card)

    def test_flag_player_and_global_not_empty_after_adding_card(self):
        self.flag.add_card(Flag.PLAYER_ONE_ID, self.card) 
        self.assertFalse(self.flag.is_player_side_empty(Flag.PLAYER_ONE_ID))
        self.assertTrue(self.flag.is_player_side_empty(Flag.PLAYER_TWO_ID))
        self.assertFalse(self.flag.is_empty())

    def test_flag_can_not_add_more_than_three_cards(self):
        for x in range(0,3): self.flag.add_card(Flag.PLAYER_ONE_ID, self.card)
        self.assertRaisesRegexp(TooManyCardsOnOneSideError, "Player player1 is attempting to add to many cards", self.flag.add_card, Flag.PLAYER_ONE_ID, self.card)

    def test_flag_can_check_if_card_playable(self):
        for x in range(0,3):
            self.assertTrue(self.flag.is_flag_playable(Flag.PLAYER_ONE_ID))
            self.flag.add_card(Flag.PLAYER_ONE_ID, self.card)
        self.assertFalse(self.flag.is_flag_playable(Flag.PLAYER_ONE_ID))

    def test_flag_can_claim_and_check_claimed_flags(self):
        self.assertFalse(self.flag.is_flag_claimed())
        self.assertFalse(self.flag.is_flag_claimed_by_player(Flag.PLAYER_ONE_ID))
        self.assertFalse(self.flag.is_flag_claimed_by_player(Flag.PLAYER_TWO_ID)) 
        self.flag.claim_flag(Flag.PLAYER_ONE_ID)
        self.assertTrue(self.flag.is_flag_claimed())
        self.assertTrue(self.flag.is_flag_claimed_by_player(Flag.PLAYER_ONE_ID))
        self.assertFalse(self.flag.is_flag_claimed_by_player(Flag.PLAYER_TWO_ID)) 

    def test_flag_can_not_place_card_after_claimed(self):
        self.flag.claim_flag(Flag.PLAYER_ONE_ID)
        self.assertRaisesRegexp(FlagAlreadyClaimedError, "Player player2 is attempting to place card on already claimed flag.", self.flag.add_card, Flag.PLAYER_TWO_ID, self.card)

