from dominion.communication.CommunicationFlow import *
class EventListener(object):
    def __init__(self, number, players):
        self.number = number
        self.players = players

    def notify(self, notification):
        if notification.type == "shuffle-deck":
            broadcast_message(self.players, 
            	CommandGenerator().create_player_shuffled_message(self.number))
        if notification.type == "gained-cards":
        	broadcast_message(self.players, 
        		CommandGenerator().create_player_gained_message(self.number, notification.cards))
        if notification.type == "played-cards":
        	broadcast_message(self.players, 
        		CommandGenerator().create_player_played_message(self.number, notification.cards))
        if notification.type == "trashed-cards":
        	broadcast_message(self.players, 
        		CommandGenerator().create_player_trashed_message(self.number, notification.cards))
        if notification.type == "discard-card":
        	broadcast_message(self.players, 
        		CommandGenerator().create_player_discard_message(self.number, notification.card))
        if notification.type == "revealed-cards":
        	broadcast_message(self.players, 
        		CommandGenerator().create_player_reveal_message(self.number, notification.cards))
