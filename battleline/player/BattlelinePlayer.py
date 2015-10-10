from battleline.engine.CommandGenerator import CommandGenerator
from battleline.engine.CommandParser import ClientCommandParser

class Player(object):
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
        self.communication = communication

    def new_game(self, direction, initial_hand):
        super(subprocessplayer, self).new_game(direction, initial_hand)

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

        return flag, card 

class BattlelinePlayer(object):
    """
    Player object for Battleline
    Keeps track of a hand
    """


    HAND_LIMIT = 7
    def __init__(self, communication, direction):
        """Constructor
        @param communication the communication the player has with a bot
        @param direction which direction this player is at
        """
        self.hand = []
        self.communication = communication
        self.generator = CommandGenerator(communication, direction)
        self.generator.send_player_direction_name()
        try:
            self.name = ClientCommandParser().parse(
                self.communication.get_response())["value"][1]
        except:
            self.name = direction

        self.direction = direction

    def add_to_hand(self, card):
        """
        Add to the hand, as long as the hand is not already at the limit
        @param card the card we want to add to the hand
        @raise HandFullError if we are already have a full hand
        """
        if(self.__is_hand_at_limit()):
            raise HandFullError(BattlelinePlayer.HAND_LIMIT)
        self.hand.append(card)

    def __is_hand_at_limit(self):
        return len(self.hand) == BattlelinePlayer.HAND_LIMIT

    def send_message(self, message):
        """
        Use the underlying communication object to talk convey commands
        @param the message we want to send using communication object
        """
        return self.communication.send_message(message)

    def get_response(self):
        """
        Use the underlying communication object to get messages back
        @return response being sent back
        """
        return self.communication.get_response()

    def remove_from_hand(self, card):
        """
        Remove a card from the hand
        @param the card to remove
        @raises InvalidMoveError if the player didn't have the card
        """
        if card not in self.hand:
            raise InvalidMoveError("Player did not have card in hand")
        self.hand.remove(card)


class HandFullError(Exception):

    def __init__(self, hand_limit):
        """
        Construtor
        @param hand_limit the limit that the player hand can be
        """
        self.hand_limit = hand_limit

    def __str__(self):
        """
        Return a string representation of the exception
        """
        return "Cannot exceed hand limit of {}".format(self.hand_limit)


class InvalidMoveError(Exception):

    def __init__(self, reason):
        """
        Constructor
        @param reason the reason why this is an invalid mov
        """
        self.reason = reason

    def __str__(self):
        """
        Return a string representation of the exception
        """
        return "Invalid Move - {}".format(self.reason)
