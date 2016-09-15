import unittest
from mock import Mock
from dominion.Identifiers import *
from dominion.engine.DominionEngine import *
from dominion.model.Player import *

def create_player_that_responds_to_first_message():
    player = Player()
    def send_message_and_await_response(json_message):
        message = json.loads(json_message)
        return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                "name" : "nothing-bot", "version": 1})
    player.send_message_and_await_response = send_message_and_await_response
    player.send_message = lambda msg: None
    return player

class TestDominionEngine(unittest.TestCase):

    def test_game_engine_deals_starting_hand(self):

        player = create_player_that_responds_to_first_message()
        players = [player]
        engine = DominionEngine(players, FIRST_GAME)

        self.assertEquals([COPPER, COPPER, COPPER, COPPER, COPPER, COPPER, COPPER, ESTATE, ESTATE, ESTATE], sorted(player.get_hand() + player.get_deck_cards()))

    def test_game_ends_if_no_player_can_make_a_move(self):
        player = Player()

        def send_message_and_await_response(json_message):
            message = json.loads(json_message)
            if message["type"] == "player-name-request":
                 return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                        "name" : "nothing-bot", "version": 1})
            else:
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player.send_message_and_await_response = send_message_and_await_response
        player.send_message = lambda msg: None

        players = [player]
        engine = DominionEngine(players, FIRST_GAME)
        engine.run_until_game_end()

        self.assertEquals(3, player.get_score())
        self.assertEquals(500, player.get_number_of_turns_taken())

    def test_player_sees_kingdom_cards(self):
        player = Player()
        player.hit_game_info = False
        def send_message_and_await_response(json_message):
            message = json.loads(json_message)
            if message["type"] == "player-name-request":
                 return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                        "name" : "nothing-bot", "version": 1})
            elif message["type"] == "game-info":
                self.assertEquals([CELLAR, MARKET, MILITIA, MINE, MOAT, REMODEL, SMITHY, VILLAGE, WOODCUTTER, WORKSHOP], message["kingdom_cards"])
                player.hit_game_info = True
            else:
                return json.dumps({"type": "play-reply", "phase": "cleanup"})
        player.send_message_and_await_response = send_message_and_await_response
        player.send_message = send_message_and_await_response

        players = [player]
        engine = DominionEngine(players, FIRST_GAME)

        self.assertTrue(player.hit_game_info)

    def test_game_ends_if_invalid_messages(self):
        player = Player()

        def send_message_and_await_response(json_message):
            message = json.loads(json_message)
            if message["type"] == "player-name-request":
                 return json.dumps( {"type": "player-name-reply", "player_number": message["player_number"],
                        "name" : "nothing-bot", "version": 1})
            else:
                return ""
        player.send_message_and_await_response = send_message_and_await_response
        player.send_message = lambda msg: None

        players = [player]
        engine = DominionEngine(players, FIRST_GAME)
        engine.run_until_game_end()

        self.assertEquals(3, player.get_score())
        self.assertEquals(500, player.get_number_of_turns_taken())

    def test_engine_exits_early_if_invalid_response_to_player_name(self):
        player = Player()
        player.send_message_and_await_response = lambda msg: ""
        player.send_message = lambda msg: self.fail

        with self.assertRaisesRegexp(Exception, "Player 1 did not respond correctly"):
            engine = DominionEngine([player], FIRST_GAME)

    def test_player_with_highest_score_wins(self):
        player1 = create_player_that_responds_to_first_message()
        player2 = create_player_that_responds_to_first_message()
        player1.add_to_hand(ESTATE)
        players = [player1, player2]
        engine = DominionEngine(players, FIRST_GAME)
        self.assertEquals([player1], engine.get_winners())

    def test_player_wins_with_less_turns_tiebreaker(self):
        player1 = create_player_that_responds_to_first_message()
        player2 = create_player_that_responds_to_first_message()
        player1.add_to_hand(ESTATE)
        player2.add_to_hand(ESTATE)
        player1.mark_turn_taken()
        players = [player1, player2]
        engine = DominionEngine(players, FIRST_GAME)
        self.assertEquals([player2], engine.get_winners())

    def test_players_with_same_scores_and_turns_tie(self):
        player1 = create_player_that_responds_to_first_message()
        player2 = create_player_that_responds_to_first_message()
        player1.add_to_hand(ESTATE)
        player2.add_to_hand(ESTATE)
        players = [player1, player2]
        engine = DominionEngine(players, FIRST_GAME)
        self.assertEquals([player1, player2], engine.get_winners())
