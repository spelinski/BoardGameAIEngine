import unittest
from battleline.engine.CommandParser import ServerCommandParser, ClientCommandParser, InvalidParseError, Identifiers


class TestCommandParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message_server(self):
        self.assertRaisesRegexp(
            InvalidParseError, "Invalid Parsed Message - Invalid Message", ServerCommandParser().parse, "Invalid Message")
        self.assertRaisesRegexp(
            InvalidParseError, "Invalid Parsed Message - Invalid Message", ClientCommandParser().parse, "Invalid Message")

    def test_can_parse_player_name_request(self):
        self.assertEquals({"type": "player_name_request", "value": Identifiers.NORTH},
                          ServerCommandParser().parse("player north name"))
        self.assertEquals({"type": "player_name_request", "value": Identifiers.SOUTH},
                          ServerCommandParser().parse("player south name"))
