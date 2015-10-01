import unittest
from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Formation import FormationInvalidError


class TestFormationLogic(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.logic = FormationLogic()
        self.fullList = [(1, 'blue'), (2, 'blue'), (3, 'blue'), (4, 'blue'), (5, 'blue'), (6, 'blue'), (7, 'blue'), (8, 'blue'), (9, 'blue'), (10, 'blue'), (1, 'red'), (2, 'red'), (3, 'red'), (4, 'red'), (5, 'red'), (6, 'red'), (7, 'red'), (8, 'red'), (9, 'red'), (10, 'red'), (1, 'green'), (2, 'green'), (3, 'green'), (4, 'green'), (5, 'green'), (6, 'green'), (7, 'green'), (8, 'green'), (9, 'green'), (10, 'green'), (1, 'orange'), (
            2, 'orange'), (3, 'orange'), (4, 'orange'), (5, 'orange'), (6, 'orange'), (7, 'orange'), (8, 'orange'), (9, 'orange'), (10, 'orange'), (1, 'purple'), (2, 'purple'), (3, 'purple'), (4, 'purple'), (5, 'purple'), (6, 'purple'), (7, 'purple'), (8, 'purple'), (9, 'purple'), (10, 'purple'), (1, 'yellow'), (2, 'yellow'), (3, 'yellow'), (4, 'yellow'), (5, 'yellow'), (6, 'yellow'), (7, 'yellow'), (8, 'yellow'), (9, 'yellow'), (10, 'yellow')]


    """test_greatestPossibleFormation

    test if the greatestPossibleFormation function will give the correct best formation with all available cards
    """

    def test_greatestPossibleFormation_empty(self):
        self.assertEquals(self.logic.greatestPossibleFormation([],[]), [
                          (8, 'blue'), (9, 'blue'), (10, 'blue')])
        self.assertEquals(self.logic.greatestPossibleFormation(
            [(1, 'blue'), (2, 'blue'), (3, 'blue')],[]), [(1, 'blue'), (2, 'blue'), (3, 'blue')])
    """test_creationFunctions_empty

    test if the create function will give the correct formation
    """

    def test_creationFunctions_empty(self):
        self.assertEquals(self.logic.createStraightFlush(
            [],[]), [(8, 'blue'), (9, 'blue'), (10, 'blue')])
        self.assertEquals(self.logic.createThreeOfAKind(
            [],[]), [(10, 'blue'), (10, 'red'), (10, 'green')])
        self.assertEquals(self.logic.createFlush(
            [],[]), [(10, 'blue'), (9, 'blue'), (8, 'blue')])
        self.assertEquals(self.logic.createStraight(
            [],[]), [(10, 'blue'), (9, 'blue'), (8, 'blue')])
        self.assertEquals(self.logic.createHost(
            [],[]), [(10, 'blue'), (10, 'red'), (10, 'green')])

    """test_creationFunctions_without10blue

    test if (10,'blue') card is used, the create function will give the correct formation
    """

    def test_creationFunctions_without10blue(self):
        playedCardList = [(10, 'blue')]
        self.assertEquals(self.logic.createStraightFlush([],playedCardList), [
                          (8, 'red'), (9, 'red'), (10, 'red')])
        self.assertEquals(self.logic.createThreeOfAKind(
            [],playedCardList), [(10, 'red'), (10, 'green'), (10, 'orange')])
        self.assertEquals(self.logic.createFlush(
            [],playedCardList), [(9, 'blue'), (8, 'blue'), (7, 'blue')])
        self.assertEquals(self.logic.createStraight(
            [],playedCardList), [(10, 'red'), (9, 'blue'), (8, 'blue')])
        self.assertEquals(self.logic.createHost(
            [],playedCardList), [(10, 'red'), (10, 'green'), (10, 'orange')])

    """test_creationFunctions_oneCard

    test if the create function is passed 1 cards, that it will give the correct formation
    """

    def test_creationFunctions_oneCard(self):
        playedCardList = [(5, 'blue')]
        card5Blue = (5, 'blue')
        self.assertEquals(self.logic.createStraightFlush([card5Blue],playedCardList), [
                          (5, 'blue'), (6, 'blue'), (7, 'blue')])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue],playedCardList), [
                          (5, 'blue'), (5, 'red'), (5, 'green')])
        self.assertEquals(self.logic.createFlush([card5Blue],playedCardList), [
                          (5, 'blue'), (10, 'blue'), (9, 'blue')])
        self.assertEquals(self.logic.createStraight([card5Blue],playedCardList), [
                          (5, 'blue'), (7, 'blue'), (6, 'blue')])
        self.assertEquals(self.logic.createHost([card5Blue],playedCardList), [
                          (5, 'blue'), (10, 'blue'), (10, 'red')])

    """test_creationFunctions_twoCards

    test if the create function is passed 2 cards, that it will give the correct formation
    """

    def test_creationFunctions_twoCards(self):
        card5Blue = (5, 'blue')
        card5Red = (5, 'red')
        card6Blue = (6, 'blue')
        playedCardList = [card5Blue, card6Blue, card5Red]
        self.assertEquals(self.logic.createStraightFlush([card5Blue, card6Blue],playedCardList), [
                          (5, 'blue'), (6, 'blue'), (7, 'blue')])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue, card5Red],playedCardList), [
                          (5, 'blue'), (5, 'red'), (5, 'green')])
        self.assertEquals(self.logic.createFlush([card5Blue, card6Blue],playedCardList), [
                          (5, 'blue'), (6, 'blue'), (10, 'blue')])
        self.assertEquals(self.logic.createStraight([card5Blue, card6Blue],playedCardList), [
                          (5, 'blue'), (6, 'blue'), (7, 'blue')])
        self.assertEquals(self.logic.createHost([card5Blue, card6Blue],playedCardList), [
                          (5, 'blue'), (6, 'blue'), (10, 'blue')])

    """test_creationFunctions_invalids_empty

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_empty(self):
        playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([],playedCardList), [])
        self.assertEquals(self.logic.createThreeOfAKind([],playedCardList), [])
        self.assertEquals(self.logic.createFlush([],playedCardList), [])
        self.assertEquals(self.logic.createStraight([],playedCardList), [])
        self.assertEquals(self.logic.createHost([],playedCardList), [])

    """test_creationFunctions_invalids_oneCard

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_oneCard(self):
        card5Blue = (5, 'blue')
        playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([card5Blue],playedCardList), [])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue],playedCardList), [])
        self.assertEquals(self.logic.createFlush([card5Blue],playedCardList), [])
        self.assertEquals(self.logic.createStraight([card5Blue],playedCardList), [])
        self.assertEquals(self.logic.createHost([card5Blue],playedCardList), [])

    """test_creationFunctions_invalids_twoCards

    if the create function can't create the formation, make sure it returns []
    """

    def test_creationFunctions_invalids_twoCards(self):
        card5Blue = (5, 'blue')
        card5Red = (5, 'red')
        card6Blue = (6, 'blue')
        playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush(
            [card5Blue, card6Blue],playedCardList), [])
        self.assertEquals(self.logic.createThreeOfAKind(
            [card5Blue, card5Red],playedCardList), [])
        self.assertEquals(self.logic.createFlush([card5Blue, card6Blue],playedCardList), [])
        self.assertEquals(self.logic.createStraight(
            [card5Blue, card6Blue],playedCardList), [])
        self.assertEquals(self.logic.createHost([card5Blue, card6Blue],playedCardList), [])
