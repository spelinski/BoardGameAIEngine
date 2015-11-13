import pymongo
import datetime
from battleline.Identifiers import Identifiers


class DatabaseOutput:

    def __init__(self, host, port, database_name):
        self.client = pymongo.MongoClient(host, port)
        db = self.client[database_name]
        if not "games" in db.collection_names(include_system_collections=False):
            db.create_collection("games")
        initPost = {"northPlayerName": "",
                    "southPlayerName": "",
                    "actionsTaken": [],
                    "winner": "",
                    "date": datetime.datetime.utcnow()}

        self.games = db.games
        self.post_id = self.games.insert_one(initPost).inserted_id
        self.playerNames = {Identifiers.NORTH: 'player1',
                            Identifiers.SOUTH: 'player2'}

    def setup_player_positions(self, playerName, place):
        self.playerNames[place] = playerName
        if place == "north":
            playerPositionKey = "northPlayerName"
        else:
            playerPositionKey = "southPlayerName"
        self.games.update({'_id': self.post_id}, {
            '$set': {playerPositionKey: playerName}})

    def draw_action(self, place, card):
        if card == None:
            myOutput = self.playerNames[place] + " draws nothing"
        else:
            myOutput = "{} draws {} {}".format(
                self.playerNames[place], str(card.number), card.color)
        self.games.update({'_id': self.post_id}, {
                          '$push': {"actionsTaken": myOutput}})

    def play_action(self, place, card, flagNumber):
        if card == None:
            myOutput = self.playerNames[place] + " plays nothing"
        else:
            myOutput = "{} plays {} {} {}".format(
                self.playerNames[place], str(card.number), card.color, str(flagNumber))
        self.games.update({'_id': self.post_id}, {
                          '$push': {"actionsTaken": myOutput}})

    def claim_action(self, place, flagNumber):
        myOutput = self.playerNames[place] + " claims " + str(flagNumber)
        self.games.update({'_id': self.post_id}, {
                          '$push': {"actionsTaken": myOutput}})

    def declare_winner(self, place):
        myOutput = self.playerNames[place] + " wins"
        self.games.update({'_id': self.post_id}, {
                          '$set': {"winner": myOutput}})

    def _delete_database(self, database_name):
        self.client.drop_database(database_name)
