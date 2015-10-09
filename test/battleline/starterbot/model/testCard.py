'''
Created 6 Oct 15

@author: Drofsned

'''

import unittest
from battleline.starterbot.model.Card import Card


class TestCard(unittest.TestCase):

    def test_new_card_with_no_parameters(self):
        self.assertEqual(['empty', 0], Card().value)

    def test_new_card_given_paramaters(self):
        self.assertEqual(['puce', 1], Card('puce', 1).value)

    def test_card_to_text(self):
        self.assertEqual('puce,1', Card().card_to_text(['puce', 1]))

    def test_text_to_card(self):
        self.assertEqual(Card().value, Card().text_to_card())
        self.assertEqual(Card('puse', 1).value, Card().text_to_card('puse,1'))
