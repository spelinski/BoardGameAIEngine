import unittest
from battleline.model.Play import Play
from battleline.Identifiers import TroopCard

class TestPlay(unittest.TestCase):

    def test_constructor(self):
        play = Play(1, TroopCard(number=1,color="color1"))
        self.assertEquals(play.flag, 1)
        self.assertEquals(play.card, TroopCard(number=1,color="color1"))


    def test_keyword_constructor(self):
        play = Play(flag=2,card=TroopCard(number=3,color="color4"))
        self.assertEquals(play.flag, 2)
        self.assertEquals(play.card, TroopCard(number=3,color="color4"))

    def test_from_tuple(self):
        play = Play.from_tuple((2, TroopCard(number=3,color="color4")))
        self.assertEquals(play.flag, 2)
        self.assertEquals(play.card, TroopCard(number=3,color="color4"))

