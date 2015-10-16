'''
Created 5 Oct 15

@author: Drofsned

'''


class Card(object):

    def __init__(self, color='empty', number=0):
        self.value = [color, int(number)]

    def card_to_text(self, text):
        return '{},{}'.format(*text)

    def text_to_card(self, text='empty,0'):
        return Card(*self.__split_text(text)).value

    def __split_text(self, text):
        return [text.split(',')[0], int(text.split(',')[1])]
