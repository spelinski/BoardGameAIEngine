import unittest
from battleline.model.Board import Board
from battleline.model.FormationLogic import FormationLogic
from battleline.model.Formation import FormationInvalidError
class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.logic = FormationLogic()
        self.fullList = [(1, 'blue')  ,(2, 'blue')  ,(3, 'blue')  ,(4, 'blue')  ,(5, 'blue')  ,(6, 'blue')  ,(7, 'blue')  ,(8, 'blue')  ,(9, 'blue')  ,(10,'blue')  ,(1, 'red')   ,(2, 'red')   ,(3, 'red')   ,(4, 'red')   ,(5, 'red')   ,(6, 'red')   ,(7, 'red')   ,(8, 'red')   ,(9, 'red')   ,(10,'red')   ,(1, 'green') ,(2, 'green') ,(3, 'green') ,(4, 'green') ,(5, 'green') ,(6, 'green') ,(7, 'green') ,(8, 'green') ,(9, 'green') ,(10,'green') ,(1, 'orange'),(2, 'orange'),(3, 'orange'),(4, 'orange'),(5, 'orange'),(6, 'orange'),(7, 'orange'),(8, 'orange'),(9, 'orange'),(10,'orange'),(1, 'purple'),(2, 'purple'),(3, 'purple'),(4, 'purple'),(5, 'purple'),(6, 'purple'),(7, 'purple'),(8, 'purple'),(9, 'purple'),(10,'purple'),(1, 'yellow'),(2, 'yellow'),(3, 'yellow'),(4, 'yellow'),(5, 'yellow'),(6, 'yellow'),(7, 'yellow'),(8, 'yellow'),(9, 'yellow'),(10,'yellow')]

    """test_checkAllFlags_empty

    test if the checkAllFlags function will work on an empty board
    """
    def test_checkAllFlags_empty(self):
        self.logic.checkAllFlags(self.board)
        for flag in self.board.flags:
	        self.assertEquals(flag.is_flag_claimed(),False)

    """test_checkAllFlags_FlagContested

    test if the checkAllFlags function will work on an empty board
    """
    def test_checkAllFlags_FlagContested(self):
        #flag 1: 10-9-8 vs 1-2-3
        self.board.flags[0].add_card(self.board.flags[0].PLAYER_ONE_ID,(10,'blue'))
        self.board.flags[0].add_card(self.board.flags[0].PLAYER_ONE_ID,(9,'blue'))
        self.board.flags[0].add_card(self.board.flags[0].PLAYER_ONE_ID,(8,'blue'))

        self.board.flags[0].add_card(self.board.flags[0].PLAYER_TWO_ID,(1,'blue'))
        self.board.flags[0].add_card(self.board.flags[0].PLAYER_TWO_ID,(2,'blue'))
        self.board.flags[0].add_card(self.board.flags[0].PLAYER_TWO_ID,(3,'blue'))

        #flag 2: 10R-9R-8R vs 1-2-_
        self.board.flags[1].add_card(self.board.flags[1].PLAYER_ONE_ID,(10,'red'))
        self.board.flags[1].add_card(self.board.flags[1].PLAYER_ONE_ID,(9,'red'))
        self.board.flags[1].add_card(self.board.flags[1].PLAYER_ONE_ID,(8,'red'))

        self.board.flags[1].add_card(self.board.flags[1].PLAYER_TWO_ID,(1,'red'))
        self.board.flags[1].add_card(self.board.flags[1].PLAYER_TWO_ID,(2,'red'))

        #flag 3: 10-9-_ vs 1-2-3 (8 is played on flag 4)
        self.board.flags[2].add_card(self.board.flags[1].PLAYER_ONE_ID,(10,'green'))
        self.board.flags[2].add_card(self.board.flags[1].PLAYER_ONE_ID,(9,'green'))

        self.board.flags[2].add_card(self.board.flags[1].PLAYER_TWO_ID,(1,'green'))
        self.board.flags[2].add_card(self.board.flags[1].PLAYER_TWO_ID,(2,'green'))
        self.board.flags[2].add_card(self.board.flags[1].PLAYER_TWO_ID,(3,'green'))
        self.board.flags[3].add_card(self.board.flags[1].PLAYER_TWO_ID,(8,'green'))
        self.logic.checkAllFlags(self.board)

        #right now I just check if the flag has been claimed, I need to check if it has been claimed by the right person
        expectedResults =  [True, True, True, False, False, False, False, False, False]
        actualResults   = [False,False,False,False,False,False,False,False,False]
        for i,flag in enumerate(self.board.flags):
            actualResults[i] = flag.is_flag_claimed()
        self.assertEquals(actualResults, expectedResults)

    """test_isStraightFlush

    test if the isStraightFlush function works
    """
    def test_isStraightFlush(self):
        self.assertEquals(self.logic.isStraightFlush([(8,'blue'),(9,'blue'),(10,'blue')]),True)
        self.assertEquals(self.logic.isStraightFlush([(8,'blue'),(9,'blue'),(7,'blue')]),True)
        self.assertEquals(self.logic.isStraightFlush([(8,'blue'),(9,'blue'),(6,'blue')]),False)
        self.assertRaises(FormationInvalidError, self.logic.isStraightFlush, [(8,'blue'),(9,'blue')])

    """test_isThreeOfAKind

    test if the isThreeOfAKind function works
    """
    def test_isThreeOfAKind(self):
        self.assertEquals(self.logic.isThreeOfAKind([(8,'blue'),(8,'red'),(8,'green')]),True)
        self.assertEquals(self.logic.isThreeOfAKind([(8,'blue'),(8,'red'),(8,'orange')]),True)
        self.assertEquals(self.logic.isThreeOfAKind([(8,'blue'),(8,'blue'),(6,'blue')]),False)
        self.assertRaises(FormationInvalidError, self.logic.isThreeOfAKind, [(8,'blue'),(9,'blue')])

    """test_isFlush

    test if the isFlush function works
    """
    def test_isFlush(self):
        self.assertEquals(self.logic.isFlush([(8,'blue'),(9,'blue'),(1,'blue')]),True)
        self.assertEquals(self.logic.isFlush([(8,'blue'),(9,'blue'),(4,'blue')]),True)
        self.assertEquals(self.logic.isFlush([(8,'blue'),(9,'blue'),(6,'red')]),False)
        self.assertRaises(FormationInvalidError, self.logic.isFlush, [(8,'blue'),(9,'blue')])

    """test_isStraight

    test if the isStraight function works
    """
    def test_isStraight(self):
        self.assertEquals(self.logic.isStraight([(8,'blue'),(9,'red'),(10,'blue')]),True)
        self.assertEquals(self.logic.isStraight([(8,'blue'),(9,'red'),(7,'blue')]),True)
        self.assertEquals(self.logic.isStraight([(8,'blue'),(9,'blue'),(6,'red')]),False)
        self.assertRaises(FormationInvalidError, self.logic.isStraight, [(8,'blue'),(9,'blue')])

    """test_isHost

    test if the isHost function works
    """
    def test_isHost(self):
        self.assertEquals(self.logic.isHost([(8,'blue'),(9,'red'),(10,'blue')]),True)
        self.assertRaises(FormationInvalidError, self.logic.isHost, [(8,'blue'),(9,'blue')])

    """test_setPlayedCardList_empty

    test if the setPlayedCardList function will parse an empty board
    """
    def test_setPlayedCardList_empty(self):
        self.logic.setPlayedCardList(self.board)
        self.assertEquals(self.logic.playedCardList,[])

    """test_greatestPossibleFormation

    test if the greatestPossibleFormation function will give the correct best formation with all available cards
    """
    def test_greatestPossibleFormation_empty(self):
        self.assertEquals(self.logic.greatestPossibleFormation([]),[(8,'blue'),(9,'blue'),(10,'blue')])
        self.assertEquals(self.logic.greatestPossibleFormation([(1, 'blue'), (2, 'blue'), (3, 'blue')]),[(1, 'blue'), (2, 'blue'), (3, 'blue')])
    """test_creationFunctions_empty

    test if the create function will give the correct formation
    """
    def test_creationFunctions_empty(self):
        self.assertEquals(self.logic.createStraightFlush([]),[(8,'blue'),(9,'blue'),(10,'blue')])
        self.assertEquals(self.logic.createThreeOfAKind([]),[(10,'blue'),(10,'red'),(10,'green')])
        self.assertEquals(self.logic.createFlush([]),[(10,'blue'),(9,'blue'),(8,'blue')])
        self.assertEquals(self.logic.createStraight([]),[(10,'blue'),(9,'blue'),(8,'blue')])
        self.assertEquals(self.logic.createHost([]),[(10,'blue'),(10,'red'),(10,'green')])

    """test_creationFunctions_without10blue

    test if (10,'blue') card is used, the create function will give the correct formation
    """
    def test_creationFunctions_without10blue(self):
        self.logic.playedCardList = [(10,'blue')]
        self.assertEquals(self.logic.createStraightFlush([]),[(8,'red'),(9,'red'),(10,'red')])
        self.assertEquals(self.logic.createThreeOfAKind([]),[(10,'red'),(10,'green'),(10,'orange')])
        self.assertEquals(self.logic.createFlush([]),[(9,'blue'),(8,'blue'),(7,'blue')])
        self.assertEquals(self.logic.createStraight([]),[(10,'red'),(9,'blue'),(8,'blue')])
        self.assertEquals(self.logic.createHost([]),[(10,'red'),(10,'green'),(10,'orange')])

    """test_creationFunctions_oneCard

    test if the create function is passed 1 cards, that it will give the correct formation
    """
    def test_creationFunctions_oneCard(self):
        self.logic.playedCardList = [(5,'blue')]
        card5Blue = (5,'blue')
        self.assertEquals(self.logic.createStraightFlush([card5Blue]),[(5,'blue'),(6,'blue'),(7,'blue')])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue]),[(5,'blue'),(5,'red'),(5,'green')])
        self.assertEquals(self.logic.createFlush([card5Blue]),[(5,'blue'),(10,'blue'),(9,'blue')])
        self.assertEquals(self.logic.createStraight([card5Blue]),[(5,'blue'),(7,'blue'),(6,'blue')])
        self.assertEquals(self.logic.createHost([card5Blue]),[(5,'blue'),(10,'blue'),(10,'red')])

    """test_creationFunctions_twoCards

    test if the create function is passed 2 cards, that it will give the correct formation
    """
    def test_creationFunctions_twoCards(self):
        card5Blue = (5,'blue')
        card5Red  = (5,'red')
        card6Blue = (6,'blue')
        self.logic.playedCardList = [card5Blue,card6Blue,card5Red]
        self.assertEquals(self.logic.createStraightFlush([card5Blue,card6Blue]),[(5,'blue'),(6,'blue'),(7,'blue')])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue,card5Red]),[(5,'blue'),(5,'red'),(5,'green')])
        self.assertEquals(self.logic.createFlush([card5Blue,card6Blue]),[(5,'blue'),(6,'blue'),(10,'blue')])
        self.assertEquals(self.logic.createStraight([card5Blue,card6Blue]),[(5,'blue'),(6,'blue'),(7,'blue')])
        self.assertEquals(self.logic.createHost([card5Blue,card6Blue]),[(5,'blue'),(6,'blue'),(10,'blue')])

    """test_creationFunctions_invalids_empty

    if the create function can't create the formation, make sure it returns []
    """
    def test_creationFunctions_invalids_empty(self):
        self.logic.playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([]),[])
        self.assertEquals(self.logic.createThreeOfAKind([]),[])
        self.assertEquals(self.logic.createFlush([]),[])
        self.assertEquals(self.logic.createStraight([]),[])
        self.assertEquals(self.logic.createHost([]),[])

    """test_creationFunctions_invalids_oneCard

    if the create function can't create the formation, make sure it returns []
    """
    def test_creationFunctions_invalids_oneCard(self):
        card5Blue = (5,'blue')
        self.logic.playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([card5Blue]),[])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue]),[])
        self.assertEquals(self.logic.createFlush([card5Blue]),[])
        self.assertEquals(self.logic.createStraight([card5Blue]),[])
        self.assertEquals(self.logic.createHost([card5Blue]),[])

    """test_creationFunctions_invalids_twoCards

    if the create function can't create the formation, make sure it returns []
    """
    def test_creationFunctions_invalids_twoCards(self):
        card5Blue = (5,'blue')
        card5Red  = (5,'red')
        card6Blue = (6,'blue')
        self.logic.playedCardList = self.fullList
        self.assertEquals(self.logic.createStraightFlush([card5Blue,card6Blue]),[])
        self.assertEquals(self.logic.createThreeOfAKind([card5Blue,card5Red]),[])
        self.assertEquals(self.logic.createFlush([card5Blue,card6Blue]),[])
        self.assertEquals(self.logic.createStraight([card5Blue,card6Blue]),[])
        self.assertEquals(self.logic.createHost([card5Blue,card6Blue]),[])
