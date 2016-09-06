'''
Created on Sep 23, 2015

@author: rohk
'''
import subprocess
from subprocess import Popen, PIPE
import threading
import shlex
import time


class PlayerCommunication(object):
    """
    Class to communicate back and forth with an external program
    """

    def __init__(self, program, workdir=None, debugFile=None):
        """
        Constructor
        @param programWithPath relative path to executable
        """
        shell_command = shlex.split(program)
        self.runningPlayer = Popen(
            shell_command, cwd=workdir, stdin=PIPE, stdout=PIPE)
        self.debugFile = debugFile

    def send_message(self, message):
        """
        send a string to the external program
        @param message string to send
        """
        if self.runningPlayer.poll() is None:
            self.runningPlayer.stdin.write(message + "\n")
            self.runningPlayer.stdin.flush()
            self.log(message)
        else:
            raise BotCommunicationError("not running, cannot send message")

    def get_response(self, timeout=10):
        """
        get the response from the external program
        @param timeout amount of time to wait in seconds (default 10)
        @raise BotCommunicationError on a timeout or empty response
        """
        if self.runningPlayer.poll() is None:
            self.exceptionFromThread = None
            thread = threading.Thread(target=self.__get_response_thread)
            thread.daemon = True
            thread.start()
            thread.join(timeout)
            if self.exceptionFromThread is not None:
                raise self.exceptionFromThread
            if thread.is_alive():
                raise BotCommunicationError("timeout")
            self.log(self.response)
            return self.response
        else:
            raise BotCommunicationError("not running, cannot get response")

    def __get_response_thread(self):
        """
        get_response calls this so that it can run
        a seperate thread with a timeout
        """
        self.response = self.runningPlayer.stdout.readline()
        if len(self.response) <= 0:
            self.exceptionFromThread = BotCommunicationError(
                "program didn't say anything")

    def close(self):
        """
        kill the external process
        """
        if self.debugFile:
            self.debugFile.close()
        if not self.polite_close():
            self.brutal_close()

    def polite_close(self):
        # Send SIGTERM, to be polite
        self.runningPlayer.terminate()

        # Give the process 5 seconds to shut down
        countdown = 5
        while self.runningPlayer.poll() is None:
            if countdown <= 0:
                return False
            time.sleep(0.1)
            countdown = countdown - 0.1
        return True

    def brutal_close(self):
        self.runningPlayer.kill()
        self.runningPlayer.wait()

    def log(self, message):
        if self.debugFile:
            self.debugFile.write(message+"\n")
            self.debugFile.flush()


class BotCommunicationError(Exception):

    def __init__(self, commFailure):
        """Create an Exception that the communcation with the bot failed
        @param commFailure
        """
        self.commFailure = commFailure

    def __str__(self):
        return "Failed to send message because of {}".format(self.commFailure)
