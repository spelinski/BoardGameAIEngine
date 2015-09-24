'''
Created on Sep 23, 2015

@author: rohk
'''
import unittest
from communcation.PlayerCommunication import PlayerCommunication
from communcation.PlayerCommunication import InvalidBotProgramError


class TestPlayerCommunication(unittest.TestCase):

    def test_goes_running_with_valid_program(self):
        localPlayerCommunication = PlayerCommunication("test/mockBot/mockBot.py")
        self.assertTrue(localPlayerCommunication.isRunning)
        localPlayerCommunication.close()
        
    def test_raises_invalid_bot_program_error(self):
        self.assertRaisesRegexp(InvalidBotProgramError, "Attempted to open invalid program ", PlayerCommunication,"a")