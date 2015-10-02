import unittest
from battleline.engine.CommandParser import CommandParser, InvalidParseError, Identifiers


class TestCommandParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message(self):
        self.assertRaisesRegexp(
            InvalidParseError, "Invalid Parsed Message - Invalid Message", CommandParser().parse, "Invalid Message")

    def test_can_parse_player_name_request(self):
        self.assertEquals({"type": "player_name_request", "value" : Identifiers.NORTH}, CommandParser().parse("player north name"))
        self.assertEquals({"type": "player_name_request", "value" : Identifiers.SOUTH}, CommandParser().parse("player south name"))
