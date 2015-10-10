from battleline.engine.CommandGenerator import CommandGenerator
from battleline.engine.CommandParser import ClientCommandParser, InvalidParseError

class Player(object):
    def __init__(self):
        self.hand = []
        self.direction = None

    def new_game(self, direction, initial_hand):
        self.direction = direction
        self.hand = initial_hand

    def compute_turn(self,board):
        raise NotImplementedError
        # return card, flag

    def finish_turn(self,card_to_remove,next_card):
        self.hand.remove(card_to_remove)
        if next_card is not None:
            self.hand.append(next_card)

class SubprocessPlayer(Player):
    def __init__(self, communication):
        super(SubprocessPlayer, self).__init__()
        self.communication = communication

    def new_game(self, direction, initial_hand):
        super(SubprocessPlayer, self).new_game(direction, initial_hand)

        self.generator = CommandGenerator(self.communication, direction)
        self.generator.send_player_direction_name()
        
        try:
            self.name = ClientCommandParser().parse(
                self.communication.get_response())["value"][1]
        except:
            self.name = direction
        
        self.generator.send_colors()

    def compute_turn(self,board):
        # Send current state to subprocess
        self.generator.send_player_hand(self.hand)
        self.generator.send_flag_claim_status(board.flags)
        self.generator.send_flag_cards(board.flags)
        # Send last move?

        # Tell them to play
        self.generator.send_go_play()

        # Retrieve action from the subprocess
        try:
          data = ClientCommandParser().parse(self.communication.get_response())
          flag, card = data["value"]
        except InvalidParseError:
          flag, card = 1, None

        return card, flag 

