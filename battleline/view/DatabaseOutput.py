import pymongo
import datetime
from battleline.Identifiers import Identifiers

'''import os.path
from battleline.Identifiers import Identifiers

ACTIONS = ['draw', 'play', 'claim', 'win']'''


class DatabaseOutput:

    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['test_database']
        initPost = {"northPlayerName" : "",
                    "southPlayerName" : "",
                    "actionsTaken" : [],
                    "winner" : "",
                    "date" : datetime.datetime.utcnow()}
        self.posts = db.posts
        self.post_id = self.posts.insert_one(initPost).inserted_id
        self.playerNames = {Identifiers.NORTH:'player1', Identifiers.SOUTH:'player2'}


    def setup_player_positions(self, playerName, place):
        self.playerNames[place] = playerName
        if place == "north":
            self.posts.update({'_id':self.post_id}, {"northPlayerName":playerName})
        else:
            self.posts.update({'_id':self.post_id}, {"southPlayerName":playerName})
            
    def get_north_player_name(self):
        whatever = self.posts.find({'_id':self.post_id})
        myDocument = whatever.next()
        return myDocument['northPlayerName']
    
    def get_south_player_name(self):
        whatever = self.posts.find({'_id':self.post_id})
        myDocument = whatever.next()
        return myDocument['southPlayerName']
        
    def draw_action(self, place, card):
        myOutput = "{} draws {} {}".format(self.playerNames[place], str(card.number), card.color)
        self.posts.update({'_id':self.post_id}, { '$push': {"actionsTaken": myOutput}})
    
    def play_action(self, place, card, flagNumber):
        myOutput = "{} plays {} {} {}".format(self.playerNames[place], str(card.number), card.color, str(flagNumber))
        self.posts.update({'_id':self.post_id}, { '$push': {"actionsTaken": myOutput}})
        
    def claim_action(self, place, flagNumber):
        myOutput = self.playerNames[place] + " claims " + str(flagNumber)
        self.posts.update({'_id':self.post_id}, { '$push': {"actionsTaken": myOutput}})
        
    def get_action(self):
        whatever = self.posts.find({'_id':self.post_id})
        myDocument = whatever.next()
        return str(myDocument['actionsTaken'][0])
    
    def declare_winner(self, place):
        myOutput = self.playerNames[place] + " wins"
        self.posts.update({'_id':self.post_id},{"winner":myOutput})
        
    def get_winner(self):
        whatever = self.posts.find({'_id':self.post_id})
        myDocument = whatever.next()
        return myDocument['winner']
        