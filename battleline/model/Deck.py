from Card import Card
from random import shuffle
class Deck(object):
    def __init__(self):
        suites = {"Blue","Green","Pink","Red","White","Yellow"}
        numbers = {1,2,3,4,5,6,7,8,9,10}
        self.deck = []
        self.deck = [ Card(number,color) for number in numbers for color in suites]
        shuffle(self.deck)
        
    def is_empty(self):
        return False
    
    def draw(self):
        return self.deck.pop()