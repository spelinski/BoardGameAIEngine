'''
Created on Sep 23, 2015

@author: rohk
'''
import unittest
import sys
from communcation.PlayerCommunication import PlayerCommunication, BotCommunicationError
import os
import time


class TestPlayerCommunication(unittest.TestCase):

    def setUp(self):
        self.workingBot = "{} test/mockBot/mockBot.py".format(sys.executable)
        self.nonExistantBot = "{} test/mockBot/dontExist.py".format(sys.executable)

    def test_should_always_send_without_timout_valid_program(self):
        localPlayerCommunication = PlayerCommunication(self.workingBot)
        localPlayerCommunication.send_message("testing")
        localPlayerCommunication.close()

    def test_should_always_send_without_timout_invalid_program(self):
        localPlayerCommunication = PlayerCommunication(self.nonExistantBot)
        localPlayerCommunication.send_message("testing")
        localPlayerCommunication.close()

    def test_should_respond_to_say_something(self):
        localPlayerCommunication = PlayerCommunication(self.workingBot)
        localPlayerCommunication.send_message("testing")
        responseFromBot = localPlayerCommunication.get_response()
        self.assertEqual(responseFromBot, "1..2..3\n")
        localPlayerCommunication.close()

    def test_should_raise_bot_communication_error_if_bot_can_not_respond(self):
        localPlayerCommunication = PlayerCommunication(self.nonExistantBot)
        localPlayerCommunication.send_message("testing")
        self.assertRaisesRegexp(
            BotCommunicationError, "Failed to send message because of program didn't say anything", localPlayerCommunication.get_response)
        localPlayerCommunication.close()

    def test_should_raise_bot_communication_error_if_bot_times_out(self):
        localPlayerCommunication = PlayerCommunication(self.workingBot)
        localPlayerCommunication.send_message("fail")
        self.assertRaisesRegexp(
            BotCommunicationError, "Failed to send message because of timeout", localPlayerCommunication.get_response, 0.1)
        localPlayerCommunication.close()

    def test_subprocess_terminated_on_close(self):
        # Only run the following test on linux (arg!) because the code to check
        # if a process is still running is super platform specific
        if "linux" in sys.platform:
            localPlayerCommunication = PlayerCommunication(self.workingBot)
            pid = localPlayerCommunication.runningPlayer.pid
            
            # Sig 0 doesn't do anything, use it to poke the subprocess
            os.kill(pid,0)
            
            # stop the process and wait a bit
            localPlayerCommunication.close()

            # An exception will be raised if sig 0 couldn't be delivered
            # because the process is now gone
            with self.assertRaises(OSError):
                os.kill(pid,0)
        
      

