import unittest
from collections import namedtuple
from battleline.view.Output import Output, ACTIONS, COLORS, TACTICS

class TestOutput(unittest.TestCase):

    def setUp(self):
        self.output = Output()
        
    def test_setup_player_positions(self):
        self.output.setup_player_positions('he', 'here')
        self.assertEqual(self.output.outputstring, 'he is here')
    
    def test_output_all_actions_function(self):
        TroopCard = namedtuple("TroopCard", ["number", "color"])
        
        actionList = [  ("p1", ACTIONS[0], TroopCard(1, "puce"), "", "p1 draws 1 puce"),
                        ("p1", ACTIONS[1], TroopCard(1, "puce"), 1, "p1 plays 1 puce 1"),
                        ("p1", ACTIONS[2], "", 1, "p1 claims 1"),
                        ("p1", ACTIONS[3], "", "", "p1 wins")
                      ]

        for name, action, card, flag, result in actionList:
            self.output.action(name, action, card, flag)
            self.assertEqual(self.output.outputstring.rstrip(), result)