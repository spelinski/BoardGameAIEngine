'''
Created 2 Oct 15

@author: Drofsned

'''

import unittest
from battleline.starterbot.Bot import Bot


class TestBattleLineBotExists(unittest.TestCase):

    def setUp(self):
        self.bot = Bot()

    def test_bot_a_bot_class(self):
        self.assertIsInstance(self.bot, Bot)
