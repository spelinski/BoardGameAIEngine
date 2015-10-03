from battleline.Identifiers import *

def make_dict(type, value):
    return {"type": type, "value": value}

def make_card( card):
    try:
        card_parts = card.split(",")
        if len(card_parts) != 2 or card_parts[0] not in Identifiers.COLORS or int(card_parts[1]) not in range(1,11):
            raise ValueError

        return TroopCard(color=card_parts[0], number=int(card_parts[1]))
    except ValueError:
        raise InvalidParseError("Invalid Card " + card)



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
        if self.__is_colors_message(message):
            return self.__parse_colors_message(message)
        if self.__is_player_hand_message(message):
            return self.__parse_player_hand_message(message)
        if self.__is_flag_claim_message(message):
            return self.__parse_flag_claim_message(message)
        if self.__is_flag_card_message(message):
            return self.__parse_flag_card_message(message)
        if self.__is_opponent_message(message):
            return self.__parse_opponent_message(message)
        if self.__is_play_card_message(message):
            return self.__parse_play_card_message(message)
        raise InvalidParseError(message)

    def __is_player_name_request(self, string):
        message = string.split()
        return len(message) == 3 and message[0] == "player" and message[2] == "name"

    def __parse_player_name_request(self, string):
        message = string.split()
        if not Identifiers.is_player_valid(message[1]):
            raise InvalidParseError(string)
        return make_dict("player_name_request", message[1])

    def __is_colors_message(self, string):
        message = string.split()
        return len(message) == 7 and message[0] == "colors"

    def __parse_colors_message(self, string):
        message = string.split()
        return make_dict("colors", message[1:])

    def __is_player_hand_message(self, string):
        message = string.split()
        return len(message) >= 3 and len(message) <=10 and message[0] == "player" and Identifiers.is_player_valid(message[1]) and message[2] == "hand"

    def __parse_player_hand_message(self, string):
        message = string.split()
        return make_dict("player_hand", (message[1], [make_card(card) for card in message[3:]]))


    def __is_flag_claim_message(self, string):
        message = string.split()
        return len(message) == 11 and message[0] == "flag" and message[1] == "claim-status" and all(status in ["unclaimed", Identifiers.NORTH, Identifiers.SOUTH] for status in message[3:])

    def __parse_flag_claim_message(self,string):
        message = string.split()
        return make_dict("flag_claim" , message[2:])

    def __is_flag_card_message(self, string):
        message = string.split()
        return len(message) >= 4 and len(message) <= 7 and message[0] == "flag" and message[2] == "cards" and Identifiers.is_player_valid(message[3])

    def __parse_flag_card_message(self, string):
        message = string.split()
        try:
            if int(message[1]) not in range(1,10):
                raise ValueError
            return make_dict("flag_cards", (int(message[1]), message[3], [make_card(card) for card in message[4:]]))
        except ValueError:
            raise InvalidParseError(string)

    def __is_opponent_message(self, string):
        message = string.split()
        return len(message) == 4 and message[0] == "opponent" and message[1] == "play"

    def __parse_opponent_message(self, string):
        message = string.split()
        try:
            if int(message[2]) not in range(1,10):
                raise ValueError
            return make_dict("opponent", (int(message[2]), make_card(message[3])))
        except ValueError:
            raise InvalidParseError(string)

    def __is_play_card_message(self, string):
        return string == "go play-card"

    def __parse_play_card_message(self,string):
        return make_dict("play_card", None)

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
        if self.__is_player_name_response(message):
            return self.__parse_player_name_response(message)
        if self.__is_play_card_response(message):
            return self.__parse_play_card_response(message)
        raise InvalidParseError(message)

    def __is_player_name_response(self, string):
        message = string.split()
        return len(message) == 3 and message[0] == "player"

    def __parse_player_name_response(self, string):
        message = string.split()
        if not Identifiers.is_player_valid(message[1]):
            raise InvalidParseError(string)
        return make_dict("player_name_response", (message[1], message[2]))

    def __is_play_card_response(self,string):
        message = string.split()
        return len(message) == 3 and message[0] == "play"

    def __parse_play_card_response(self,string):
        message = string.split()
        try:
            if int(message[1]) not in range(1,10):
                raise ValueError
            return make_dict("play_card_response", (int(message[1]), make_card(message[2])))
        except ValueError:
            raise InvalidParseError(string)


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
