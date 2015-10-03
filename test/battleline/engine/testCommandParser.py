import unittest
from battleline.engine.CommandParser import ServerCommandParser, ClientCommandParser, InvalidParseError
from battleline.Identifiers import *


def make_dict(msg_type, value):
    return {"type": msg_type, "value": value}


class TestServerParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message_server(self):
        invalid_messages = ["Invalid Server Message",
                            "player north wrong", "player unknown name", "colors 0 1 2 3 4"]
        for message in invalid_messages:
            self.assertRaisesRegexp(
                InvalidParseError, "Invalid Parsed Message - {}".format(message), ServerCommandParser().parse, message)

    def test_can_parse_player_name_request(self):
        self.assertEquals(make_dict("player_name_request", Identifiers.NORTH),
                          ServerCommandParser().parse("player north name"))
        self.assertEquals(make_dict("player_name_request", Identifiers.SOUTH),
                          ServerCommandParser().parse("player south name"))

    def test_can_parse_colors(self):
        self.assertEquals(make_dict("colors", ["0", "1", "2", "3", "4", "5"]),
                          ServerCommandParser().parse("colors 0 1 2 3 4 5"))

    def test_can_parse_player_hand_empty(self):
        self.assertEquals(make_dict("player_hand", (Identifiers.NORTH, [])),
                          ServerCommandParser().parse("player north hand"))


class TestClientParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message_server(self):
        self.assertRaisesRegexp(
            InvalidParseError, "Invalid Parsed Message - Invalid Server Message", ServerCommandParser().parse, "Invalid Server Message")

    def test_can_parse_player_name_response(self):
        self.assertEquals({"type": "player_name_response", "value": (
            Identifiers.NORTH, "name")}, ClientCommandParser().parse("player north name"))
        self.assertEquals({"type": "player_name_response", "value": (
            Identifiers.SOUTH, "name2")}, ClientCommandParser().parse("player south name2"))
