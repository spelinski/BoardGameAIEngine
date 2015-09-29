import unittest
from battleline.view.Output import Output, ACTIONS, COLORS, TACTICS


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.output = Output()

    def test_output_all_actions_function(self):
        actionList = [	("p1", ACTIONS[0], 1, COLORS[0], "", 0, "p1 draws 1 blue"),
                       ("p1", ACTIONS[1], 0, COLORS[0],
                        TACTICS[0], 0, "p1 plays Alexander"),
                       ("p1", ACTIONS[1], 2, COLORS[
                        1], "", 0, "p1 plays 2 red"),
                       ("p1", ACTIONS[1], 0, COLORS[0],
                        TACTICS[1], 0, "p1 plays Darius"),
                       ("p1", ACTIONS[2], 0, COLORS[0], "", 1, "p1 claims 1"),
                       ("p1", ACTIONS[3], 0, COLORS[0], "", 0, "p1 wins ")
                       ]
        for name, action, number, color, tactic, flag, result in actionList:
            self.output.setOutputString(
                name, action, number, color, tactic, flag)
            self.assertTrue(self.output.outputString == result)
