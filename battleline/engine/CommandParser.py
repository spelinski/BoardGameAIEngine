
class Identifiers(object):
    NORTH = "north"
    SOUTH = "south"

class CommandParser(object):

    def parse(self, message):
        """
        Parse the mesage and return a dict of information
        @param message the message to be parsed
        @return a dictionary of {type: message type,  values : arbitrary}
        @raise InvalidParseError if the message was not of the type we expected
        """
        if self.__is_player_name_request(message): return self.__parse_player_name_request(message)
        raise InvalidParseError(message)

    def __is_player_name_request(self,string):
        message = string.split()
        return len(message) == 3 and message[0] == "player" and message[2] == "name"

    def __parse_player_name_request(self, string):
        message = string.split()
        if message[1] == "north" : return self.__make_dict("player_name_request", Identifiers.NORTH)
        if message[1] == "south" : return self.__make_dict("player_name_request", Identifiers.SOUTH)
        raise InvalidParseError(string)

    def __make_dict(self, type, value):
        return {"type":type, "value":value}


class InvalidParseError(Exception):

    def __init__(self, message):
        """
        Constructor
        @message the message that caused this error
        """
        self.message = message

    def __str__(self):
        """
        Return a string representation
        @return a string representation
        """
        return "Invalid Parsed Message - {}".format(self.message)
