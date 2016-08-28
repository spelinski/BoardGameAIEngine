'''
Created on Sep 23, 2015

@author: rohk
'''
import unittest
import sys
from communication.PlayerCommunication import PlayerCommunication, BotCommunicationError
import os
import time


class TestPlayerCommunication(unittest.TestCase):

    def setUp(self):
        self.workingDir = "test/mockBot"
        self.workingBot = "{} mockBot.py".format(sys.executable)
        self.workingBotWithPath = "{} test/mockBot/mockBot.py".format(
            sys.executable)
        self.nonExistantBot = "{} test/mockBot/dontExist.py".format(
            sys.executable)

    def test_should_always_send_without_timout_valid_program(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.send_message("testing")
        localPlayerCommunication.close()

    def test_should_always_send_without_timout_invalid_program(self):
        localPlayerCommunication = PlayerCommunication(
            self.nonExistantBot, self.workingDir)
        time.sleep(1)
        with self.assertRaises(BotCommunicationError):
            localPlayerCommunication.send_message("testing")

    def test_should_respond_to_say_something(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.send_message("testing")
        responseFromBot = localPlayerCommunication.get_response()
        self.assertEqual(responseFromBot, "1..2..3\n")
        localPlayerCommunication.close()

    def test_should_respond_to_say_something_without_set_workingdir(self):
        localPlayerCommunication = PlayerCommunication(self.workingBotWithPath)
        localPlayerCommunication.send_message("testing")
        responseFromBot = localPlayerCommunication.get_response()
        self.assertEqual(responseFromBot, "1..2..3\n")
        localPlayerCommunication.close()

    def test_should_raise_bot_communication_error_if_bot_can_not_respond(self):
        localPlayerCommunication = PlayerCommunication(
            self.nonExistantBot, self.workingDir)
        time.sleep(1)
        with self.assertRaises(BotCommunicationError):
            localPlayerCommunication.send_message("testing")

    def test_should_raise_bot_communication_error_if_bot_times_out(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.send_message("fail")
        self.assertRaisesRegexp(
            BotCommunicationError, "Failed to send message because of timeout", localPlayerCommunication.get_response, 0.1)
        localPlayerCommunication.close()

    def test_should_raise_exception_if_bot_died_and_eof_read(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.send_message("die")
        self.assertRaisesRegexp(
            BotCommunicationError, "program didn't say anything", localPlayerCommunication.get_response, 0.1)
        localPlayerCommunication.close()

    def test_should_raise_exception_if_bot_already_shutdown(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.close()
        self.assertRaisesRegexp(
            BotCommunicationError, "not running, cannot get response", localPlayerCommunication.get_response, 0.1)


class TestPlayerCommunicationShutdown(unittest.TestCase):

    def setUp(self):
        self.workingDir = "test/mockBot"
        self.workingBot = "{} mockBot.py".format(sys.executable)

    def test_subprocess_terminated_on_close(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        self.assert_comms_closed(localPlayerCommunication)

    def test_subprocess_terminated_on_close_with_input(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.send_message("testing")
        self.assert_comms_closed(localPlayerCommunication)

    def test_subprocess_terminated_on_close_with_bad_input(self):
        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.send_message("fail")
        self.assert_comms_closed(localPlayerCommunication)

    def test_subprocess_ignores_sigterm(self):
        def fake_terminate():
            pass

        localPlayerCommunication = PlayerCommunication(
            self.workingBot, self.workingDir)
        localPlayerCommunication.runningPlayer.terminate = fake_terminate
        localPlayerCommunication.send_message("nahnahstayingalive")
        responseFromBot = localPlayerCommunication.get_response()
        self.assertIn("MY JAM!", responseFromBot)
        self.assert_comms_closed(localPlayerCommunication)

    def assert_comms_closed(self, comms):
        pid = comms.runningPlayer.pid

        # Sig 0 doesn't do anything, use it to poke the subprocess
        os.kill(pid, 0)

        # stop the process and wait a bit
        comms.close()

        # An exception will be raised if sig 0 couldn't be delivered
        # because the process is now gone
        with self.assertRaises(OSError):
            os.kill(pid, 0)
