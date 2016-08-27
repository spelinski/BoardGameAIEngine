class CommandGenerator(object):
    def create_player_info_request(self, player_number, version):
        return {
                 "type" : "player-name-request",
                 "player_number" : "player" + str(player_number),
                 "version" : version
                }

    def create_supply_info_message(self, supply):
        return {
          "type" : "supply-info",
          "cards" : supply
        }
