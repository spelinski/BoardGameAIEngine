import unittest,os
from collections import namedtuple
from battleline.view.Output import Output, ACTIONS
from battleline.Identifiers import Identifiers,TroopCard


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
        self.output.action(Identifiers.NORTH, ACTIONS[0], TroopCard(1, "magenta"))
        self.assertEqual(self.output.outputstring.rstrip(), "A_POLAR_BEAR draws 1 magenta")

    def test_output_all_actions_function(self):
        actionList = [(Identifiers.NORTH, ACTIONS[0], TroopCard(1, "puce"), "", "player1 draws 1 puce"),
                      (Identifiers.NORTH, ACTIONS[1], TroopCard(
                          1, "puce"), 1, "player1 plays 1 puce 1"),
                      (Identifiers.NORTH, ACTIONS[2], "", 1, "player1 claims 1"),
                      (Identifiers.NORTH, ACTIONS[3], "", "", "player1 wins")
                      ]

        for name, action, card, flag, result in actionList:
            self.output.action(name, action, card, flag)
            self.assertEqual(self.output.outputstring.rstrip(), result)

    def test_find_new_file_name(self):
        secondOutput = Output()
        self.assertNotEqual(self.output.filename, secondOutput.filename)
        os.remove(secondOutput.filename)
        
