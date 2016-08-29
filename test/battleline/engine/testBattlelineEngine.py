import unittest
import os
from itertools import product
from mechanics.Deck import Deck
from battleline.engine.BattlelineEngine import BattlelineEngine, TroopCard
from battleline.player.BattlelinePlayer import Player
from battleline.Identifiers import Identifiers
from battleline.model.Play import Play
from battleline.view.Output import Output


class MockPlayer(Player):

    def __init__(self, name):
        self.name = name

    def provide_next_turn(self, next_card, next_flag):
        self.next_card = next_card
        self.next_flag = next_flag

    def compute_turn(self, board, are_flags_open, last_move):
        return Play(card=self.next_card, flag=self.next_flag)


def get_engine_with_ordered_cards():
    engine = BattlelineEngine(MockPlayer("yankeeBot"),
                              MockPlayer("rebelBot"), Output())

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
        # list of identifiers for which bot is in which position,
        # SubprocessPlayer names default to the position name
        self.nameAndPositionIdentifierStringArray = [
            "yankeeBot is north", "rebelBot is south"]
        # list of cards that are drawn at the beginning of the game
        self.startingOutputStringArray = [
            "yankeeBot draws 1 color1", "rebelBot draws 2 color1",
            "yankeeBot draws 3 color1", "rebelBot draws 4 color1",
            "yankeeBot draws 5 color1", "rebelBot draws 6 color1",
            "yankeeBot draws 7 color1", "rebelBot draws 8 color1",
            "yankeeBot draws 9 color1", "rebelBot draws 10 color1",
            "yankeeBot draws 1 color2", "rebelBot draws 2 color2",
            "yankeeBot draws 3 color2", "rebelBot draws 4 color2"]
        # list of moves that all of the tests perform...edit at your own risk
        self.movesList = [
            ["yankeeBot plays 1 color1 1", "yankeeBot draws 5 color2",
                "rebelBot plays 2 color1 1", "rebelBot draws 6 color2"],
            ["yankeeBot plays 3 color1 1", "yankeeBot draws 7 color2",
             "rebelBot plays 4 color1 1", "rebelBot draws 8 color2"],
            ["yankeeBot plays 5 color1 1", "yankeeBot draws 9 color2",
             "rebelBot plays 6 color1 1", "rebelBot draws 10 color2", "rebelBot claims 1"],
            ["yankeeBot plays 7 color1 2", "yankeeBot draws 1 color3",
             "rebelBot plays 8 color1 2", "rebelBot draws 2 color3"],
            ["yankeeBot plays 9 color1 2", "yankeeBot draws 3 color3",
             "rebelBot plays 10 color1 2", "rebelBot draws 4 color3"],
            ["yankeeBot plays 1 color2 2", "yankeeBot draws 5 color3",
             "rebelBot plays 2 color2 2", "rebelBot draws 6 color3", "rebelBot claims 2"],
            ["yankeeBot plays 3 color2 3", "yankeeBot draws 7 color3",
             "rebelBot plays 4 color2 3", "rebelBot draws 8 color3"],
            ["yankeeBot plays 5 color2 3", "yankeeBot draws 9 color3",
             "rebelBot plays 6 color2 3", "rebelBot draws 10 color3"],
            ["yankeeBot plays 7 color2 3", "yankeeBot draws 1 color4", "rebelBot plays 8 color2 3",
             "rebelBot draws 2 color4", "rebelBot claims 3", "rebelBot wins "],
            ["yankeeBot plays 9 color2 4", "yankeeBot draws 3 color4", "rebelBot wins",
             "rebelBot plays 10 color2 4", "rebelBot draws 4 color4", "rebelBot wins"],
            ["yankeeBot plays 1 color3 4", "yankeeBot draws 5 color4", "rebelBot wins",
             "rebelBot plays 2 color3 4", "rebelBot draws 6 color4", "rebelBot wins"],
            ["yankeeBot plays 3 color3 4", "yankeeBot draws 7 color4", "rebelBot wins",
             "rebelBot plays 4 color3 4", "rebelBot draws 8 color4", "rebelBot claims 4", "rebelBot wins"],
            ["yankeeBot plays 5 color3 5", "yankeeBot draws 9 color4", "rebelBot wins",
             "rebelBot plays 6 color3 5", "rebelBot draws 10 color4", "rebelBot wins"],
            ["yankeeBot plays 7 color3 5", "yankeeBot draws 1 color5", "rebelBot wins",
             "rebelBot plays 8 color3 5", "rebelBot draws 2 color5", "rebelBot wins"],
            ["yankeeBot plays 9 color3 5", "yankeeBot draws 3 color5", "rebelBot wins", "rebelBot plays 10 color3 5",
             "rebelBot draws 4 color5 ", "rebelBot claims 5", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 1 color4 6", "yankeeBot draws 5 color5", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 2 color4 6", "rebelBot draws 6 color5", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 3 color4 6", "yankeeBot draws 7 color5", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 4 color4 6", "rebelBot draws 8 color5", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 5 color4 6", "yankeeBot draws 9 color5", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 6 color4 6", "rebelBot draws 10 color5", "rebelBot claims 6", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 7 color4 7", "yankeeBot draws 1 color6", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 8 color4 7", "rebelBot draws 2 color6", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 9 color4 7", "yankeeBot draws 3 color6", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 10 color4 7", "rebelBot draws 4 color6", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 1 color5 7", "yankeeBot draws 5 color6", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 2 color5 7", "rebelBot draws 6 color6", "rebelBot claims 7", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 3 color5 8", "yankeeBot draws 7 color6", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 4 color5 8", "rebelBot draws 8 color6", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 5 color5 8", "yankeeBot draws 9 color6", "rebelBot wins", "rebelBot wins",
             "rebelBot plays 6 color5 8", "rebelBot draws 10 color6", "rebelBot wins", "rebelBot wins"],
            ["yankeeBot plays 7 color5 8", "yankeeBot draws nothing", "rebelBot wins", "rebelBot wins", "rebelBot plays 8 color5 8", "rebelBot draws nothing", "rebelBot claims 8", "rebelBot wins", "rebelBot wins"]]

    def __getOutputFileContents(self):
        with open(self.engine.output_handler.filename) as f:
            data = f.read()
        return data

    def __getStartingString(self):
        return self.nameAndPositionIdentifierStringArray + self.startingOutputStringArray

    def tearDown(self):
        os.remove(self.engine.output_handler.filename)

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
        self.assertEquals(
            self.__getOutputFileContents(), "\n".join(trueStartingString))

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
        self.assertEquals("rebelBot", self.engine.get_winning_player_name())

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
