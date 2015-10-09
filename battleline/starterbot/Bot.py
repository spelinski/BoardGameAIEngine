'''
Created 2 Oct 15

@author: Drofsned
'''

from sys import stdin, stdout
from parse.Parser import Parser


class Bot(object):

    def __init__(self):
        self.parser = Parser()

    def run(self):
        while not stdin.closed:
            try:
                message = stdin.readline().strip()

                if len(message) == 0:
                    continue

                if self.parser.process(message):
                    self.__respond(self.parser.response())

            except (EOFError, KeyboardInterrupt):
                return

    def __respond(self, response):
        stdout.write(response + '\n')
        stdout.flush()

if __name__ == '__main__':
    Bot().run()
