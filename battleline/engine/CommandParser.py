
class Identifiers(object):
    NORTH = "north"
    SOUTH = "south"


def make_dict(type, value):
    return {"type": type, "value": value}


class ServerCommandParser(object):
    """
    Meant for parsing messages that come from the server
    """

    def parse(self, message):
        """
        Parse the mesage and return a dict of information
        @param message the message to be parsed
        @return a dictionary of {type: message type,  values : arbitrary}
        @raise InvalidParseError if the message was not of the type we expected
        """
        if self.__is_player_name_request(message):
            return self.__parse_player_name_request(message)
        raise InvalidParseError(message)

    def __is_player_name_request(self, string):
        message = string.split()
        return len(message) == 3 and message[0] == "player" and message[2] == "name"

    def __parse_player_name_request(self, string):
        message = string.split()
        if message[1] != Identifiers.NORTH and message[1] != Identifiers.SOUTH:
            raise InvalidParseError(string)
        return make_dict("player_name_request", message[1])




class ClientCommandParser(object):
    """
    Meant for parsing messages that come from the server
    """

    def parse(self, message):
        """
        Parse the mesage and return a dict of information
        @param message the message to be parsed
        @return a dictionary of {type: message type,  values : arbitrary}
        @raise InvalidParseError if the message was not of the type we expected
        """
        if self.__is_player_name_response(message): return self.__make_player_name_response(message)
        raise InvalidParseError(message)

    def __is_player_name_response(self,string):
        return string.split()[0] == "player"

    def __make_player_name_response(self, string):
        message = string.split()
        if message[1] != Identifiers.NORTH and message[1] != Identifiers.SOUTH:
            raise InvalidParseError(string)
        return make_dict("player_name_response", (message[1], message[2]))


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
