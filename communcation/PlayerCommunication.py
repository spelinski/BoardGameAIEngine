'''
Created on Sep 23, 2015

@author: rohk
'''
from subprocess import Popen,PIPE
import threading


class PlayerCommunication(object):
    '''
    classdocs
    '''

    def __init__(self, programWithPath):
        '''
        Constructor
        '''
        self.runningPlayer = Popen("./"+programWithPath,stdin =PIPE,stdout=PIPE, shell=True)
    
    def close(self):
        self.runningPlayer.terminate()
        
    def send_message(self, message):
        self.runningPlayer.stdin.write(message + "\n")
        self.runningPlayer.stdin.flush()
        
    def get_response(self, timeout=10):
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
        self.response = self.runningPlayer.stdout.readline()
        if len(self.response) <= 0:
            self.exceptionFromThread = BotCommunicationError("program didn't say anything")
        

class BotCommunicationError(Exception):

    def __init__(self, whatWentWrong):
        """Create an Exception that the program is not valid
        @param programWithPathString
        """
        self.whatWentWrong = whatWentWrong

    def __str__(self):
        return "Failed to send message because of {}".format(self.whatWentWrong)