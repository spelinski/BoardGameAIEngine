'''
Created on Sep 23, 2015

@author: rohk
'''
from subprocess import Popen, PIPE
import threading
class PlayerCommunication(object):
    """
    Class to communicate back and forth with an external program
    """
    def __init__(self, programWithPath):
        """
        Constructor
        @param programWithPath relative path to executable
        """
        self.runningPlayer = Popen(
            "./" + programWithPath, stdin=PIPE, stdout=PIPE, shell=True)

    def send_message(self, message):
        """
        send a string to the external program
        @param message string to send
        """
        self.runningPlayer.stdin.write(message + "\n")
        self.runningPlayer.stdin.flush()

    def get_response(self, timeout=10):
        """
        get the response from the external program
        @param timeout amount of time to wait in seconds (default 10)
        @raise BotCommunicationError on a timeout or empty response
        """
        self.exceptionFromThread = None
        thread = threading.Thread(target=self.__get_response_thread)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        if self.exceptionFromThread is not None:
            raise self.exceptionFromThread
        if thread.is_alive():
            raise BotCommunicationError("timeout")
        return self.response

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
        self.runningPlayer.terminate()


class BotCommunicationError(Exception):

    def __init__(self, commFailure):
        """Create an Exception that the communcation with the bot failed
        @param commFailure
        """
        self.commFailure = commFailure

    def __str__(self):
        return "Failed to send message because of {}".format(self.commFailure)
