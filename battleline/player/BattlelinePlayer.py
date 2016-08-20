from battleline.engine.CommandGenerator import CommandGenerator
from battleline.engine.CommandParser import ClientCommandParser, InvalidParseError
from battleline.model.Play import Play


class Player(object):
    """
    An abstract player that is used by an Engine for the purposes
    of playing a game of Battle Line. The engine interacts with
    a Player by:

    (1) Calling new_game to provide initial state for a new game
    (2) Calling compute_turn to allow the player to provide its next play
    (3) Calling finish_turn to provide the player with the actual card played (in
        case of some error with the player's response), and the
        next card drawn for their hand.
    (4) Repeeat 2-3 until game end
    """
    def __init__(self):
        """
        Constructor
        """
        self.hand = []
        self.direction = None

    def new_game(self, direction, initial_hand):
        """
        Start a new game of Battle Line
        :param direction: The direction ("north"/"south") the player is facing.
        :param initial_hand: The inital hand of seven TroopCards for the player.
        """
        self.direction = direction
        self.hand = initial_hand

    def compute_turn(self,board, are_flags_open, last_move):
        """
        Implement this method in a derived class to provide the special
        logic for your player.
        :param board: The current game board state.
        :param are_flags_open: if there are flags open to play
        :param last_move: The previous move taken by the opponent. None if
            this is the first turn (and thus no previous move)
        :return: A Play to be performed on the board
        """
        raise NotImplementedError
        # return card, flag

    def finish_turn(self,card_to_remove,next_card):
        """
        Finish the turn by removing a card from your hand and adding a new card
        (drawn from the deck) to your hand. Note that card_to_remove may not match
        the card you played, especially in the case where your Player has executed
        an invalid move.
        :param card_to_remove: The card to remove from your hand.
        :param next_card: A new card to add to your hand.
        """
        self.hand.remove(card_to_remove)
        if next_card is not None:
            self.hand.append(next_card)


class SubprocessPlayer(Player):
    """
    A SubprocessPlayer defers player decisions to a subprocess. It acts as a proxy between
    the engine and communication with those external players.
    """
    def __init__(self, communication):
        """
        Constructor
        :param communication: The communication path to use with the subprocess.
        """
        super(SubprocessPlayer, self).__init__()
        self.communication = communication
        self.parser = ClientCommandParser()
        self.name = None
        self.generator = None

    def new_game(self, direction, initial_hand):
        """
        Pump the new game state into the subprocess. See Player.new_game for
        more information.
        :param direction:
        :param initial_hand:
        :return:
        """
        super(SubprocessPlayer, self).new_game(direction, initial_hand)
        self.generator = CommandGenerator(self.communication, direction)
        self.generator.send_player_direction_name()
        self.name = self.__get_response_or_default((None, direction))[1]
        self.generator.send_colors()

    def compute_turn(self, board, are_flags_open, last_move):
        """
        Provide the current game state to the supprocess and then ask the
        subprocess for its next move. See Player.compute_turn for more information.
        :param board: The current game board state.
        :param are_flags_open: if there are flags open to play
        :param last_move: The last move taken by the opponent.
        :return: The next Play taken by the subprocess.
        """
        self.__send_game_state(board, last_move)
        return self.__request_next_move() if are_flags_open else Play.from_tuple((1,None))

    def __send_game_state(self, board, last_move):
        """
        Send the current game state to the subprocess.
        :param board: The current game board.
        :param last_move: The last move taken by the opponent, or None
        """
        # Send current state to subprocess
        self.generator.send_player_hand(self.hand)
        self.generator.send_flag_claim_status(board.flags)
        self.generator.send_flag_cards(board.flags)
        if last_move is not None:
            self.generator.send_opponent_play(last_move.flag, last_move.card)

    def __request_next_move(self):
        """
        Request the next move from the subprocess
        :return: A (flag,card) tuple
        """
        self.generator.send_go_play()
        return Play.from_tuple(self.__get_response_or_default((1, None)))

    def __get_response_or_default(self, default):
        """
        Retrieve a response from the subprocess or a default on error.
        :param default: The default to return on error retrieving the response.
        :return: The subprocess response or the default.
        """
        try:
            data = self.parser.parse(self.communication.get_response())
            return data["value"]
        except InvalidParseError:
            return default
