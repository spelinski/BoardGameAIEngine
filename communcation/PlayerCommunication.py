'''
Created on Sep 23, 2015

@author: rohk
'''
from subprocess import Popen,PIPE


class PlayerCommunication(object):
    '''
    classdocs
    '''

    def __init__(self, programWithPath):
        '''
        Constructor
        '''
        self.runningPlayer = Popen("./"+programWithPath,stdin =PIPE,stdout=PIPE, shell=True)
        self.runningPlayer.stdin.write("identify yourself\n")
        self.runningPlayer.stdin.flush()
        self.playerName = self.runningPlayer.stdout.readline()
        if len(self.playerName) <= 0:
            raise InvalidBotProgramError(programWithPath)
        self.isRunning = True
    
    def close(self):
        self.runningPlayer.terminate()

class InvalidBotProgramError(Exception):

    def __init__(self, programWithPathString):
        """Create an Exception that the program is not valid
        @param programWithPathString
        """
        self.programWithPathString = programWithPathString

    def __str__(self):
        return "Attempted to open invalid program {}".format(self.programWithPathString)