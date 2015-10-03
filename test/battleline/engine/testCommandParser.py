import unittest
from battleline.engine.CommandParser import ServerCommandParser, ClientCommandParser, InvalidParseError
from battleline.Identifiers import *


def make_dict(msg_type, value):
    return {"type": msg_type, "value": value}

invalid_card_strings = ["colorx,5", "color1,string",
                        "color1", "color1,1,3", "color1,0", "color1,11"]


class TestServerParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message_server(self):
        invalid_messages = ["Invalid Server Message",
                            "player north wrong", "player unknown name", "colors 0 1 2 3 4", "player unknown hand",
                            "player north hand 1,1 2,2 3,3 4,4 5,5 6,6 7,7 8,8",
                            "flag claim-status north north north north north north north north",
                            "flag claim-status north north north north north north north north north north",
                            "flag claim-wrong north north north north north north north north north",
                            "flag claim-status north north north north north north north north wrong",
                            "flag 1 cards",
                            "flag 1 cards north 1,1 2,2 3,3 4,4",
                            "flag wrong cards north", "flag 1 cards unknown", "flag 0 cards north", "flag 10 cards north", "opponent play 0 color1,4",
                            "opponent play 10 color1,4", "opponent play 1", "go"]
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

    def test_can_parse_player_hand_one_card(self):
        self.assertEquals(make_dict("player_hand", (Identifiers.SOUTH, [TroopCard(color=Identifiers.COLORS[0], number=5)])),
                          ServerCommandParser().parse("player south hand color1,5"))

    def test_can_parse_player_hand_one_card(self):
        self.assertEquals(make_dict("player_hand", (Identifiers.SOUTH, [TroopCard(color=Identifiers.COLORS[0], number=5),
                                                                        TroopCard(color=Identifiers.COLORS[
                                                                                  0], number=6),
                                                                        TroopCard(color=Identifiers.COLORS[
                                                                                  0], number=7),
                                                                        TroopCard(color=Identifiers.COLORS[
                                                                                  1], number=1),
                                                                        TroopCard(color=Identifiers.COLORS[
                                                                                  1], number=2),
                                                                        TroopCard(color=Identifiers.COLORS[
                                                                                  1], number=3),
                                                                        TroopCard(color=Identifiers.COLORS[1], number=4), ])),
                          ServerCommandParser().parse("player south hand color1,5 color1,6 color1,7 color2,1 color2,2 color2,3 color2,4"))

    def test_invalid_parse_error_raised_when_invalid_card(self):
        for card in invalid_card_strings:
            self.assertRaisesRegexp(
                InvalidParseError, "Invalid Parsed Message - Invalid Card " + card, ServerCommandParser().parse, "player north hand " + card)

    def test_flag_claim_status(self):
        self.assertEquals(make_dict("flag_claim", ["unclaimed", Identifiers.NORTH, Identifiers.SOUTH,
                                                   "unclaimed", Identifiers.NORTH, Identifiers.SOUTH,
                                                   "unclaimed", Identifiers.NORTH, Identifiers.SOUTH]),
                          ServerCommandParser().parse("flag claim-status unclaimed north south unclaimed north south unclaimed north south"))
        self.assertEquals(make_dict("flag_claim", ["unclaimed"] * 9),
                          ServerCommandParser().parse("flag claim-status unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed unclaimed"))

    def test_flag_card_status_empty(self):
        self.assertEquals(make_dict("flag_cards", (1, Identifiers.NORTH, [
        ])), ServerCommandParser().parse("flag 1 cards north"))
        self.assertEquals(make_dict("flag_cards", (2, Identifiers.SOUTH, [
        ])), ServerCommandParser().parse("flag 2 cards south"))

    def test_flag_card_status_one_card(self):
        self.assertEquals(make_dict("flag_cards", (1, Identifiers.NORTH, [TroopCard(color=Identifiers.COLORS[
                          0], number=3)])), ServerCommandParser().parse("flag 1 cards north color1,3"))

    def test_flag_card_status_three_cards(self):
        self.assertEquals(make_dict("flag_cards", (1, Identifiers.NORTH, [TroopCard(color=Identifiers.COLORS[0], number=3),
                                                                          TroopCard(color=Identifiers.COLORS[
                                                                                    0], number=4),
                                                                          TroopCard(color=Identifiers.COLORS[0], number=5)])),
                          ServerCommandParser().parse("flag 1 cards north color1,3 color1,4 color1,5"))

    def test_invalid_parse_error_raised_when_invalid_card_flag_cards(self):
        for card in invalid_card_strings:
            self.assertRaisesRegexp(
                InvalidParseError, "Invalid Parsed Message - Invalid Card " + card, ServerCommandParser().parse, "flag 1 cards north " + card)

    def test_opponent_message(self):
        self.assertEquals(make_dict("opponent", (1, TroopCard(
            color="color1", number=3))), ServerCommandParser().parse("opponent play 1 color1,3"))
        self.assertEquals(make_dict("opponent", (2, TroopCard(
            color="color2", number=4))), ServerCommandParser().parse("opponent play 2 color2,4"))

    def test_invalid_parse_error_raised_when_invalid_card_flag_cards(self):
        for card in invalid_card_strings:
            self.assertRaisesRegexp(
                InvalidParseError, "Invalid Parsed Message - Invalid Card " + card, ServerCommandParser().parse, "opponent play 1 " + card)

    def test_play_card_message(self):
        self.assertEquals(make_dict("play_card", None),
                          ServerCommandParser().parse("go play-card"))


class TestClientParser(unittest.TestCase):

    def test_invalid_message_thrown_if_invalid_message_server(self):
        invalid_messages = ["Invalid Client Message", "player unknown name", "player north", "play 0 color1,2",
                            "play 10 color1,3", "play 1"]
        for message in invalid_messages:
            self.assertRaisesRegexp(
                InvalidParseError, "Invalid Parsed Message - {}".format(message), ClientCommandParser().parse, message)

    def test_can_parse_player_name_response(self):
        self.assertEquals(make_dict("player_name_response", (Identifiers.NORTH,
                                                             "name")), ClientCommandParser().parse("player north name"))
        self.assertEquals(make_dict("player_name_response", (Identifiers.SOUTH,
                                                             "name2")), ClientCommandParser().parse("player south name2"))

    def test_can_parse_play_card_response(self):
        self.assertEquals(make_dict("play_card_response", (1, TroopCard(
            color="color1", number=2))), ClientCommandParser().parse("play 1 color1,2"))
        self.assertEquals(make_dict("play_card_response", (2, TroopCard(
            color="color3", number=4))), ClientCommandParser().parse("play 2 color3,4"))

    def test_invalid_parse_error_raised_when_invalid_card_play_card(self):
        for card in invalid_card_strings:
            self.assertRaisesRegexp(
                InvalidParseError, "Invalid Parsed Message - Invalid Card " + card, ClientCommandParser().parse, "play 1 " + card)
