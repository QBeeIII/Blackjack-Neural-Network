
# 13 nodes for every card's value
#  1,2,3,4 indicating amount left in deck
# 
# 1 node for dealer showing
#  2-11
# 
# 1 node for player sum
#  4-21
#
# perhaps not needed as deck covers what's drawn
# 1 node for player ace
#  0-4

import random

class Deck:
    def __init__(self):
        self.deck = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4
        self.drawn = []
        self.index = 0

    def shuffle(self):
        random.shuffle(self.deck)
        self.drawn = []
        self.index = 0
    
    def draw(self):
        index = self.index
        self.index = self.index + 1
        self.drawn.append(self.deck[index])
        return self.deck[index]


class Blackjack:
    #         0       1                 2                 3              4
    state = ["deck", "dealer showing", "player showing", "dealer aces", "player aces"]
    deck = Deck()



    # not necessary?
    def reset(self):
        self.state[0].shuffle()
        self.state[1] = 0
        self.state[2] = 0
        self.state[3] = 0

    def deal(self):
        #dealer
        draw = self.state[0].draw()
        if draw == 1:
            self.state[3] = self.state[3] + 1
        self.state[1] = draw

        #player
        for i in range(2):
            draw = self.state[0].draw()
            if draw == 1:
                self.state[4] = self.state[4] + 1
            self.state[2] = self.state[2] + draw
    
    def hit(self):
        self.state[2] = self.state[2] + self.deck.draw()
        if self.state[2] > 21:
            placeholder
            #execute loss somewhere
    
    def double(self):
        self.state[2] = self.state[2] + self.deck.draw()
        #find a way to double the bet
        if self.state[2] > 21:
            placeholder
            #execute loss somewhere

    def stand(self):
        #reveal 2nd card
        self.state[1] = self.state[0].draw()
        
        #dealers turn
        for i in range(4): # potentially 4 ace draw...
            while self.state[1] < 18: #stand on 17
                draw = self.state[0].draw()
                if draw == 1: #aces
                    self.state[3] = self.state[3] + 1
                self.state[1] = draw

            if self.state[1] > 21: #if bust but have ace, reduce
                if self.state[3] > 0:
                    self.state[1] = self.state[1] - 10
                else:
                    break
        
        if self.state[1] > 21 | self.state[1] < self.state[2]:
            placeholder
            #WIN
        
        #LOSE



