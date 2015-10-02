import unittest
from battleline.engine.CommandParser import ServerCommandParser, ClientCommandParser, InvalidParseError, Identifiers


class TestCommandParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message_server(self):
        self.assertRaisesRegexp(
            InvalidParseError, "Invalid Parsed Message - Invalid Server Message", ServerCommandParser().parse, "Invalid Server Message")
        self.assertRaisesRegexp(
            InvalidParseError, "Invalid Parsed Message - Invalid Client Message", ClientCommandParser().parse, "Invalid Client Message")

    def test_can_parse_player_name_request(self):
        self.assertEquals({"type": "player_name_request", "value": Identifiers.NORTH},
                          ServerCommandParser().parse("player north name"))
        self.assertEquals({"type": "player_name_request", "value": Identifiers.SOUTH},
                          ServerCommandParser().parse("player south name"))

    def test_can_parse_player_name_response(self):
        self.assertEquals({"type": "player_name_response", "value": (Identifiers.NORTH, "name")}, ClientCommandParser().parse("player north name"))
        self.assertEquals({"type": "player_name_response", "value": (Identifiers.SOUTH, "name2")}, ClientCommandParser().parse("player south name2"))
