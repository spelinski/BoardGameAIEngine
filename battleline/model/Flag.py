class Flag(object):
    """A representation of a flag in Battle Line.
    A flag can hold 3 cards for both players.
    """
    PLAYER_NORTH = "Player North"
    PLAYER_SOUTH = "Player South"
    MAX_CARDS_PER_SIDE = 3

    def __init__(self):
        """
        Constructor
        """
        self.sides = {self.PLAYER_NORTH: [], self.PLAYER_SOUTH: []}
        self.claimed = None 

    def is_empty(self):
        """
        Determines if there are any cards played on this flag.
        """
        return self.is_player_side_empty(self.PLAYER_NORTH) and self.is_player_side_empty(self.PLAYER_SOUTH)

    def is_player_side_empty(self, player):
        """ Determines if a player side is empty.

        @param player The player side to check.
        """
        self.__raise_error_if_invalid_player(player)
        return len(self.sides[player]) == 0

    def add_card(self, player, card):
        """Add a card to the Flag

        @param player player side to add the flag to. 
        @param card   the card to add to the player side
        """
        self.__raise_error_if_invalid_player(player)
        self.__raise_error_if_card_can_not_be_played(player)
        self.sides[player].append(card)

    def get_cards(self, player):
        """Get all cards on owned by this player on this flag

        @param player player side to get the cards from 
        """
        return self.sides[player]

    def is_playable(self, player):
        """Checks if a side of the flag can be played on.

        @param player Player side to check
        """
        self.__raise_error_if_invalid_player(player)
        return len(self.sides[player]) < self.MAX_CARDS_PER_SIDE
    
    def claim(self, player):
        """Mark this flag as claimed by this player

        @param player player side to add the flag to. 
        """
        self.__raise_error_if_invalid_player(player) 
        self.claimed = player

    def is_claimed(self):
        return self.claimed is not None

    def is_claimed_by_player(self, player):
        return self.claimed == player
    
    def who_has_claimed(self):
        return self.claimed

    def __is_valid_player_choice(self, player):
        return player in self.sides

    def __raise_error_if_invalid_player(self, player):
        if not self.__is_valid_player_choice(player):
            raise InvalidPlayerError(player)

    def __raise_error_if_card_can_not_be_played(self, player):
        if not self.is_playable(player): 
            raise TooManyCardsOnOneSideError(player) 
        if self.is_claimed():
            raise FlagAlreadyClaimedError(player)

class FlagAlreadyClaimedError(Exception):
    def __init__(self, player_string):
        """Create an Exception that the player is trying to place 
        a card on and already claimed flag.
        @param player_string the player name that is placing the card
        """
        self.player = player_string

    def __str__(self):
        return "{} is attempting to place card on already claimed flag.".format(self.player)

class InvalidPlayerError(Exception):

    def __init__(self, player_string):
        """Create an Exception that the player is not valid
        @param player_string the player name that was not valid
        """
        self.player = player_string

    def __str__(self):
        return "Player String {} is invalid".format(self.player)


class TooManyCardsOnOneSideError(Exception):
     def __init__(self, player_string):
         """Create an Exception that the player is trying to add to many cards
         @param player_string the player name that was adding too many cards 
         """
         self.player = player_string 
 
     def __str__(self):
         return "{} is attempting to add to many cards".format(self.player)

