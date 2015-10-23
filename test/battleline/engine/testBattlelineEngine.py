import unittest
import os
from itertools import product
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine, TroopCard
from battleline.player.BattlelinePlayer import SubprocessPlayer
from test.battleline.player.MockPlayerCommunication import MockPlayerCommunication
from battleline.Identifiers import Identifiers
from battleline.model.Play import Play


class MockPlayer(SubprocessPlayer):

    def provide_next_turn(self, next_card, next_flag):
        self.next_card = next_card
        self.next_flag = next_flag

    def compute_turn(self, board, last_move):
        return Play(card=self.next_card, flag=self.next_flag)


def get_engine_with_ordered_cards():
    communication = MockPlayerCommunication()
    engine = BattlelineEngine(MockPlayer(communication), MockPlayer(communication))

    # reinitialize the deck with a non shuffled deck to make things more reliable
    # don't do this in production code, the deck should be shuffled in real
    # code
    engine.troop_deck = Deck(sorted(engine.get_troop_cards(), key=lambda x: (
        x[1], x[0]), reverse=True), shuffleDeck=False)
    return engine


class TestBattlelineUninitializedEngine(unittest.TestCase):

    def setUp(self):
        self.engine = get_engine_with_ordered_cards()

    def tearDown(self):
        os.remove(self.engine.output_handler.filename)

    def test_board_deck_should_have_all_sixty_cards_to_start_with(self):
        colors = ["RED", "GREEN", "ORANGE", "YELLOW", "BLUE", "PURPLE"]
        all_troops = [TroopCard(number, color) for color, number in sorted(
            product(colors, range(1, 11)), reverse=True)]
        return sorted(all_troops) == sorted(self.engine.troop_deck.deck)


class TestBattlelineInitializedEngine(unittest.TestCase):

    def setUp(self):
        self.engine = get_engine_with_ordered_cards()
        self.engine.initialize()
        # list of identifiers for which bot is in which position, SubprocessPlayer names default to the position name
        self.moreFirsterThanStartingArray = ["north is north", "south is south"]
        # list of cards that are drawn at the beginning of the game
        self.startingOutputStringArray = ["north draws 1 color1 ", "south draws 2 color1 ",
                                          "north draws 3 color1 ", "south draws 4 color1 ",
                                          "north draws 5 color1 ", "south draws 6 color1 ",
                                          "north draws 7 color1 ", "south draws 8 color1 ",
                                          "north draws 9 color1 ", "south draws 10 color1 ",
                                          "north draws 1 color2 ", "south draws 2 color2 ",
                                          "north draws 3 color2 ", "south draws 4 color2 "]
        # list of moves that all of the tests perform...edit at your own risk
        self.movesList = [["north plays 1 color1 0", "north draws 5 color2 ", "south plays 2 color1 0", "south draws 6 color2 "],
                          ["north plays 3 color1 0", "north draws 7 color2 ",
                              "south plays 4 color1 0", "south draws 8 color2 "],
                          ["north plays 5 color1 0", "north draws 9 color2 ",
                              "south plays 6 color1 0", "south draws 10 color2 ", "south claims 0"],
                          ["north plays 7 color1 1", "north draws 1 color3 ",
                              "south plays 8 color1 1", "south draws 2 color3 "],
                          ["north plays 9 color1 1", "north draws 3 color3 ",
                              "south plays 10 color1 1", "south draws 4 color3 "],
                          ["north plays 1 color2 1", "north draws 5 color3 ",
                              "south plays 2 color2 1", "south draws 6 color3 ", "south claims 1"],
                          ["north plays 3 color2 2", "north draws 7 color3 ",
                              "south plays 4 color2 2", "south draws 8 color3 "],
                          ["north plays 5 color2 2", "north draws 9 color3 ",
                              "south plays 6 color2 2", "south draws 10 color3 "],
                          ["north plays 7 color2 2", "north draws 1 color4 ", "south plays 8 color2 2",
                              "south draws 2 color4 ", "south claims 2", "south wins "],
                          ["north plays 9 color2 3", "north draws 3 color4 ", "south wins ",
                              "south plays 10 color2 3", "south draws 4 color4 ", "south wins "],
                          ["north plays 1 color3 3", "north draws 5 color4 ", "south wins ",
                              "south plays 2 color3 3", "south draws 6 color4 ", "south wins "],
                          ["north plays 3 color3 3", "north draws 7 color4 ", "south wins ",
                              "south plays 4 color3 3", "south draws 8 color4 ", "south claims 3", "south wins "],
                          ["north plays 5 color3 4", "north draws 9 color4 ", "south wins ",
                              "south plays 6 color3 4", "south draws 10 color4 ", "south wins "],
                          ["north plays 7 color3 4", "north draws 1 color5 ", "south wins ",
                              "south plays 8 color3 4", "south draws 2 color5 ", "south wins "],
                          ["north plays 9 color3 4", "north draws 3 color5 ", "south wins ", "south plays 10 color3 4",
                              "south draws 4 color5 ", "south claims 4", "south wins ", "south wins "],
                          ["north plays 1 color4 5", "north draws 5 color5 ", "south wins ", "south wins ",
                              "south plays 2 color4 5", "south draws 6 color5 ", "south wins ", "south wins "],
                          ["north plays 3 color4 5", "north draws 7 color5 ", "south wins ", "south wins ",
                              "south plays 4 color4 5", "south draws 8 color5 ", "south wins ", "south wins "],
                          ["north plays 5 color4 5", "north draws 9 color5 ", "south wins ", "south wins ",
                              "south plays 6 color4 5", "south draws 10 color5 ", "south claims 5", "south wins ", "south wins "],
                          ["north plays 7 color4 6", "north draws 1 color6 ", "south wins ", "south wins ",
                              "south plays 8 color4 6", "south draws 2 color6 ", "south wins ", "south wins "],
                          ["north plays 9 color4 6", "north draws 3 color6 ", "south wins ", "south wins ",
                              "south plays 10 color4 6", "south draws 4 color6 ", "south wins ", "south wins "],
                          ["north plays 1 color5 6", "north draws 5 color6 ", "south wins ", "south wins ",
                              "south plays 2 color5 6", "south draws 6 color6 ", "south claims 6", "south wins ", "south wins "],
                          ["north plays 3 color5 7", "north draws 7 color6 ", "south wins ", "south wins ",
                              "south plays 4 color5 7", "south draws 8 color6 ", "south wins ", "south wins "],
                          ["north plays 5 color5 7", "north draws 9 color6 ", "south wins ", "south wins ",
                              "south plays 6 color5 7", "south draws 10 color6 ", "south wins ", "south wins "],
                          ["north plays 7 color5 7", "north draws nothing", "south wins ", "south wins ", "south plays 8 color5 7", "south draws nothing", "south claims 7", "south wins ", "south wins "]]

    def __getOutputFileContents(self):
        with open(self.engine.output_handler.filename) as f:
            data = f.read()
        return data

    def __getStartingString(self):
        return self.moreFirsterThanStartingArray + self.startingOutputStringArray

    def tearDown(self):
        os.remove(self.engine.output_handler.filename)
        #pass

    def test_each_player_starts_with_names_and_with_7_cards_after_initialization(self):
        self.assertEquals([TroopCard(1, "color1"),
                           TroopCard(3, "color1"),
                           TroopCard(5, "color1"),
                           TroopCard(7, "color1"),
                           TroopCard(9, "color1"),
                           TroopCard(1, "color2"),
                           TroopCard(3, "color2")], self.engine.player1.hand)
        self.assertEquals([TroopCard(2, "color1"),
                           TroopCard(4, "color1"),
                           TroopCard(6, "color1"),
                           TroopCard(8, "color1"),
                           TroopCard(10, "color1"),
                           TroopCard(2, "color2"),
                           TroopCard(4, "color2")], self.engine.player2.hand)

        trueStartingString = self.__getStartingString()
        trueStartingString.append("")
        self.assertEquals(self.__getOutputFileContents(), "\n".join(trueStartingString))
        '''
        self.startingOutputStringArray.append("")
        self.assertEquals(self.__getOutputFileContents(),
                          "\n".join(self.startingOutputStringArray))
        '''

    def test_one_turn_plays_a_troop_and_draws_new_one(self):
        # make new copies of the hand
        player1_hand = [card for card in self.engine.player1.hand]
        player2_hand = [card for card in self.engine.player2.hand]

        self.__play_turn()

        self.assertHandsDifferBy1(player1_hand, self.engine.player1.hand)
        self.assertHandsDifferBy1(player2_hand, self.engine.player2.hand)
        self.assertNotIn(TroopCard(1, "color1"), self.engine.player1.hand)
        self.assertNotIn(TroopCard(2, "color1"), self.engine.player1.hand)
        outputArray = self.__getStartingString()
        for move in self.movesList[0]:
            outputArray.append(move)

        outputArray.append("")
        self.assertEquals(self.__getOutputFileContents(),
                          "\n".join(outputArray))

    def test_players_hands_diminish_if_deck_runs_out(self):
        for _ in xrange(46):
            next(self.engine.troop_deck)
        self.__play_turn()
        self.assertEquals(6, len(self.engine.player1.hand))
        self.assertEquals(6, len(self.engine.player2.hand))

    def test_winner_can_be_determined(self):
        for i in xrange(23):
            self.__play_turn()
        self.assertEquals("south", self.engine.get_winning_player())

    def test_invalid_moves_still_produce_a_valid_move(self):
        for i in xrange(4):
            self.__play_turn()
        self.assertEquals([TroopCard(color="color1", number=1),
                           TroopCard(color="color1", number=3),
                           TroopCard(color="color1", number=5)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.NORTH])
        self.assertEquals([TroopCard(color="color1", number=2),
                           TroopCard(color="color1", number=4),
                           TroopCard(color="color1", number=6)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.SOUTH])
        self.assertEquals([TroopCard(color="color1", number=7)],
                          self.engine.board_logic.board.get_flag(2).sides[Identifiers.NORTH])
        self.assertEquals([TroopCard(color="color1", number=8)],
                          self.engine.board_logic.board.get_flag(2).sides[Identifiers.SOUTH])

        outputArray = self.__getStartingString()
        for turn in self.movesList[:4]:
            for move in turn:
                outputArray.append(move)
        outputArray.append("")
        self.assertEquals(self.__getOutputFileContents(),
                          "\n".join(outputArray))

    def test_winner_is_none_to_begin_with(self):
        self.assertIsNone(self.engine.get_winning_player())

    def test_invalid_moves_with_flag_and_card(self):

        self.engine.player1.provide_next_turn(TroopCard(1, "blah"), 1)
        self.engine.player2.provide_next_turn(TroopCard(11, "color1"), 1)
        self.engine.progress_turn()

        self.assertEquals([TroopCard(color="color1", number=1)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.NORTH])
        self.assertEquals([TroopCard(color="color1", number=2)],
                          self.engine.board_logic.board.get_flag(1).sides[Identifiers.SOUTH])

        outputArray = self.__getStartingString()
        for move in self.movesList[0]:
            outputArray.append(move)

        outputArray.append("")
        self.assertEquals(self.__getOutputFileContents(),
                          "\n".join(outputArray))

    def test_unplayed_cards_after_initialization(self):
        expected_cards = set(self.engine.get_troop_cards())
        self.assertEquals(expected_cards, set(
            self.engine.get_unplayed_cards()))
        self.__play_turn()
        expected_cards = expected_cards - \
            set([TroopCard(color="color1", number=1),
                 TroopCard(color="color1", number=2)])
        self.assertEquals(expected_cards, set(
            self.engine.get_unplayed_cards()))

        outputArray = self.__getStartingString()
        for move in self.movesList[0]:
            outputArray.append(move)

        outputArray.append("")
        self.assertEquals(self.__getOutputFileContents(),
                          "\n".join(outputArray))

    def assertHandsDifferBy1(self, old_hand, new_hand):
        self.assertEquals(1, len(set(old_hand) - set(new_hand)))
        self.assertEquals(1, len(set(new_hand) - set(old_hand)))

    def __play_turn(self):
        self.engine.player1.provide_next_turn(TroopCard(1, "color1"), 1)
        self.engine.player2.provide_next_turn(TroopCard(2, "color1"), 1)
        self.engine.progress_turn()

    def test_player2_does_not_get_turn_if_player1_wins(self):
        self.engine.board_logic.addCard(
            1, Identifiers.NORTH, TroopCard(10, "color1"))
        self.engine.board_logic.addCard(
            1, Identifiers.NORTH, TroopCard(9, "color1"))
        self.engine.board_logic.addCard(
            1, Identifiers.NORTH, TroopCard(8, "color1"))
        self.engine.board_logic.addCard(
            2, Identifiers.NORTH, TroopCard(10, "color4"))
        self.engine.board_logic.addCard(
            2, Identifiers.NORTH, TroopCard(9, "color4"))
        self.engine.board_logic.addCard(
            2, Identifiers.NORTH, TroopCard(8, "color4"))
        self.engine.board_logic.addCard(
            3, Identifiers.NORTH, TroopCard(10, "color3"))
        self.engine.board_logic.addCard(
            3, Identifiers.NORTH, TroopCard(9, "color3"))
        self.engine.board_logic.addCard(
            3, Identifiers.NORTH, TroopCard(8, "color3"))
        self.engine.player1.provide_next_turn(TroopCard(1, "color2"), 9)
        self.engine.player2.provide_next_turn(TroopCard(2, "color2"), 9)
        self.engine.progress_turn()
        self.assertEquals(self.engine.last_move.flag, 9)
        self.assertEquals(self.engine.last_move.card, TroopCard(1, "color2"))

    def test_flag_cannot_be_played_if_already_claimed(self):
        for number in [10, 9, 8]:
            self.engine.board_logic.addCard(
                2, Identifiers.NORTH, TroopCard(number, "color1"))

        self.engine.player1.provide_next_turn(TroopCard(1, "color2"), 3)
        self.engine.player2.provide_next_turn(TroopCard(2, "color2"), 3)
        self.engine.progress_turn()
        self.assertEquals(self.engine.last_move.flag, 1)
        self.assertEquals(self.engine.last_move.card, TroopCard(2, "color2"))

    def test_player2_does_not_get_turn_if_player1_wins(self):
        for flag in xrange(9):
            self.engine.board_logic.addCard(
                flag, Identifiers.SOUTH, TroopCard(1, "color1"))
            self.engine.board_logic.addCard(
                flag, Identifiers.SOUTH, TroopCard(2, "color1"))
            self.engine.board_logic.addCard(
                flag, Identifiers.SOUTH, TroopCard(3, "color1"))

        self.engine.player1.provide_next_turn(TroopCard(1, "color2"), 9)
        self.engine.player2.provide_next_turn(TroopCard(2, "color2"), 9)
        self.engine.progress_turn()
        self.assertEquals(self.engine.last_move.flag, 9)
        self.assertEquals(self.engine.last_move.card, TroopCard(1, "color2"))
