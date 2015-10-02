class CommandParser(object):

    def parse(self, message):
        raise InvalidParseError(message)

class InvalidParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Invalid Parsed Message - {}".format(self.message)
