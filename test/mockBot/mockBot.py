#!/usr/bin/python
'''
Created on Sep 23, 2015

@author: rohk
'''

from sys import stdin, stdout
import signal

def snuff_signal(x,y):
    print "STAYING ALIIIIIIIVE"
    return 

class Bot:

    def __init__(self):
        self.staying_alive = False

    def run(self):
        while not stdin.closed:
            try:
                line = stdin.readline().strip()

                if len(line) == 0:
                    continue

                if line == "nahnahstayingalive":
                    print "MY JAM!"
                    self.staying_alive=True
                    signal.signal(signal.SIGTERM, snuff_signal)

                if line == "testing":
                    try:
                        stdout.write("1..2..3\n")
                        stdout.flush()
                    except:
                        pass

            except EOFError:
                return
            except KeyboardInterrupt:
                if not self.staying_alive:
                    raise KeyboardInterrupt()
                else:
                    pass

    @staticmethod
    def sendMoves(moves):
        stdout.write(','.join(moves) + '\n')
        stdout.flush()


if __name__ == '__main__':
    Bot().run()
