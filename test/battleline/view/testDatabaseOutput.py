import unittest
from battleline.view.DatabaseOutput import DatabaseOutput
from battleline.Identifiers import Identifiers, TroopCard


class TestDatabaseOutput(unittest.TestCase):

    def setUp(self):
        self.output = DatabaseOutput('localhost', 27017, 'test_database')

    def tearDown(self):
        self.output.delete_database('test_database')

    def test_setup_player_positions_north(self):
        self.output.setup_player_positions('Hooch', Identifiers.NORTH)
        myOutput = self.output.games.find({'_id': self.output.post_id}).next()['northPlayerName']
        self.assertEqual(myOutput, 'Hooch')

    def test_setup_player_positions_south(self):
        self.output.setup_player_positions('Pooch', Identifiers.SOUTH)
        myOutput = self.output.games.find({'_id': self.output.post_id}).next()['southPlayerName']
        self.assertEqual(myOutput, 'Pooch')

    def test_drawing_card_north(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.draw_action(Identifiers.NORTH, TroopCard(1, "red"))
        myOutput =  self.output.games.find({'_id': self.output.post_id}).next()['actionsTaken'][0]
        self.assertEqual(myOutput, "Synergy draws 1 red")

    def test_playing_card_north_flag_one(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.play_action(Identifiers.NORTH, TroopCard(1, "red"), 1)
        myOutput = self.output.games.find({'_id': self.output.post_id}).next()['actionsTaken'][0]
        self.assertEqual(myOutput, "Synergy plays 1 red 1")

    def test_claiming_flag_one_north(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.claim_action(Identifiers.NORTH, 1)
        myOutput = self.output.games.find({'_id': self.output.post_id}).next()['actionsTaken'][0]
        self.assertEqual(myOutput, "Synergy claims 1")

    def test_north_wins(self):
        self.output.setup_player_positions('Synergy', Identifiers.NORTH)
        self.output.declare_winner(Identifiers.NORTH)
        myOutput = self.output.games.find({'_id': self.output.post_id}).next()['winner']
        self.assertEqual(myOutput, "Synergy wins")
