from dominion.Identifiers import *
from dominion.model.Supply import *
from dominion.communication.CommunicationFlow import *
from itertools import *

class DominionEngine(object):

    def __init__(self, players, game_set):
        self.players = players
        self.supply = Supply(len(players), game_set)
        for number, player in enumerate(players, start=1):
            try:
                send_player_info(player, number, 1)
            except:
                raise Exception("Player {} did not respond correctly".format(number))
            self.deal_starting_cards(player)

    def deal_starting_cards(self, player):
        for _ in range(3):
            self.supply.take(ESTATE)
            player.gain_card(ESTATE)
        for _ in range(7):
            self.supply.take(COPPER)
            player.gain_card(COPPER)
        player.draw_cards(5)

    def run_until_game_end(self):
        max_number_of_turns = 100 * len(self.players)
        for player in islice(cycle(self.players), max_number_of_turns):
            if self.supply.is_game_over():
                break
            send_supply_info(player, self.supply)
            try:
                send_turn_request(player, self.supply)
            except:
                #bot messed up, turn skipped
                pass
            player.mark_turn_taken()

    def get_winners(self):
        winning_players = []
        highest_score = max([player.get_score() for player in self.players])
        highest_score_players = [player for player in self.players if player.get_score() == highest_score]
        lowest_turns = min([player.get_number_of_turns_taken() for player in highest_score_players])
        winners = [player for player in highest_score_players if player.get_number_of_turns_taken() == lowest_turns]
        return winners
