import unittest
import os
from battleline.view.Output import Output
from battleline.Identifiers import Identifiers, TroopCard


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.output = Output()

    def tearDown(self):
        os.remove(self.output.filename)

    def test_setup_player_positions(self):
        self.output.setup_player_positions('Hooch', 'crazy')
        self.assertEqual(self.output.outputstring, 'Hooch is crazy')

    def test_changing_player_name(self):
        self.output.setup_player_positions('A_POLAR_BEAR', Identifiers.NORTH)
        self.output.draw_action(Identifiers.NORTH, TroopCard(1, "magenta"))
        self.assertEqual(self.output.outputstring.rstrip(),
                         "A_POLAR_BEAR draws 1 magenta")

    def test_output_draw_card(self):
        self.output.draw_action(Identifiers.NORTH, TroopCard(1, "puce"))
        self.assertEqual(self.output.outputstring.rstrip(),
                         "player1 draws 1 puce")

    def test_output_play_card(self):
        self.output.play_action(Identifiers.NORTH, TroopCard(1, "puce"), 1)
        self.assertEqual(self.output.outputstring.rstrip(),
                         "player1 plays 1 puce 1")

    def test_output_claim_flag(self):
        self.output.claim_action(Identifiers.NORTH, 1)
        self.assertEqual(self.output.outputstring.rstrip(), "player1 claims 1")

    def test_output_winner(self):
        self.output.declare_winner(Identifiers.NORTH)
        self.assertEqual(self.output.outputstring.rstrip(), "player1 wins")

    def test_find_new_file_name(self):
        secondOutput = Output()
        self.assertNotEqual(self.output.filename, secondOutput.filename)
        os.remove(secondOutput.filename)
