import unittest
from battleline.engine.CommandParser import CommandParser, InvalidParseError
class TestCommandParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message(self):
        self.assertRaisesRegexp(InvalidParseError, "Invalid Parsed Message - Invalid Message", CommandParser().parse, "Invalid Message")
