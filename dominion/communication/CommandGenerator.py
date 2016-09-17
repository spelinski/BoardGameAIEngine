class CommandGenerator(object):
    def create_player_info_request(self, player_number, version):
        return {
                 "type" : "player-name-request",
                 "player_number" : "player" + str(player_number),
                 "version" : version
                }

    def create_supply_info_message(self, supply_dict):
        return {
          "type" : "supply-info",
          "cards" : supply_dict
        }

    def create_play_turn_request(self, actions, buys, extra_money, hand, played, gained):
        return {
          "type": "play-turn",
          "actions": actions,
          "buys": buys,
          "extra_money": extra_money,
          "hand" : hand,
          "cards_played": played,
          "cards_gained": gained
        }
    def create_attack_request_discard(self, number_to_discard, options):
        return {
          "type" : "attack-request",
          "discard": number_to_discard,
          "options": options
        }

    def create_player_shuffled_message(self, number):
        return {
            "type": "player-shuffled",
            "player_number": number
        }

    def create_game_info_message(self, player_names, kingdom_cards):
        return {
            "type": "game-info",
            "player_bot_names": player_names,
            "kingdom_cards" : kingdom_cards
        }

    def create_game_end_message(self, scores, winners):
        return {
            "type" : "game-end",
            "scores": scores,
            "winners": winners
        }
