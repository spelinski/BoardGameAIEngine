import unittest
from battleline.view.DatabaseOutput import DatabaseOutput
from battleline.Identifiers import Identifiers, TroopCard
from mock import patch
from MockPyMongo import MockMongoClient
        

class TestDatabaseOutput(unittest.TestCase):

    @patch('battleline.view.DatabaseOutput.pymongo.MongoClient', MockMongoClient)
    def setUp(self):
        self.output = DatabaseOutput('localhost', 27017, 'test_database')

    def tearDown(self):
        self.output.delete_database('test_database')

    def test_setup_player_positions_north(self):
        self.output.setup_player_positions('north_side', Identifiers.NORTH)
        self.assertEqual(self.output.games.find({'_id': self.output.post_id}).next()['northPlayerName'], 'north_side')

    def test_setup_player_positions_south(self):
        self.output.setup_player_positions('south_side', Identifiers.SOUTH)
        self.assertEqual(self.output.games.find({'_id': self.output.post_id}).next()['southPlayerName'], 'south_side')

    def test_drawing_card_north(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.draw_action(Identifiers.NORTH, TroopCard(1, "red"))
        self.assertEqual(self.output.games.find({'_id': self.output.post_id}).next()['actionsTaken'][0], "Synergy draws 1 red")

    def test_playing_card_north_flag_one(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.play_action(Identifiers.NORTH, TroopCard(1, "red"), 1)
        self.assertEqual(self.output.games.find({'_id': self.output.post_id}).next()['actionsTaken'][0], "Synergy plays 1 red 1")

    def test_claiming_flag_one_north(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.claim_action(Identifiers.NORTH, 1)
        self.assertEqual(self.output.games.find({'_id': self.output.post_id}).next()['actionsTaken'][0], "Synergy claims 1")

    def test_north_wins(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.declare_winner(Identifiers.NORTH)
        self.assertEqual(self.output.games.find({'_id': self.output.post_id}).next()['winner'], "Synergy wins")
