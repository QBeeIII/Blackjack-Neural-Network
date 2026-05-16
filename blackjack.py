
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
        #aces are initially 11 and reduced later
        self.deck = [11,2,3,4,5,6,7,8,9,10,10,10,10] * 4
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
    def __init__(self):
        self.reset()

    #hardcoded vals for now
    def reset(self):
        #              0       1                 2                 3                    4
        self.state = ["deck", "dealer showing", "player showing", "dealer fluid aces", "player fluid aces"]
        self.deck = Deck()
        self.bank = 1000
        self.bet = 10
        self.pot = 0
        self.min = 10
        self.max = 500

    def endRound(self):
        self.state[0].shuffle()
        self.state[1] = 0
        self.state[2] = 0
        self.state[3] = 0
        self.state[4] = 0
        self.pot = 0

    #TODO: tie results to model fitness
    def lose(self):
        self.endRound()
        return 0

    def win(self):
        self.bank = self.bank + 2*self.pot
        self.endRound()
        return 1
    
    def tie(self):
        self.bank = self.bank + self.pot
        self.endRound()
        return 2

    # PLAYER ACTIONS: start, hit, double, stand
    # returns:
    # -1 = game continues
    #  0 = loss
    #  1 = win
    #  2 = tie
    #TODO: figure out where to start rounds
    #TODO: figure out how to limit double to first round
    def deal(self):
        self.pot = self.bet
        self.bank = self.bank - self.bet

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
        
        if self.state[2] == 21:
            return self.stand()
        return -1

    def hit(self):
        draw = self.deck.draw()
        
        if draw == 11:
            self.state[4] = self.state[4] + 1 #ace count
        self.state[2] = self.state[2] + draw

        #bust but have ace
        if self.state[2] > 21 & self.state[4] > 0:
            self.state[2] = self.state[2] - 10
            self.state[4] = self.state[4] - 1
        
        if self.state[2] > 21:
            return self.lose()
        #no self sabotage
        elif self.state[2] == 21:
            return self.stand()
        else:
            return -1        
        
    def double(self):
        self.pot = 2*self.bet
        self.bank = self.bank - self.bet

        result = self.hit()
        if result >= 0:
            return result
        else:
            return self.stand()

    def stand(self):
        #reveal 2nd card
        self.state[1] = self.state[0].draw()
        
        #dealers turn
        for i in range(4): # potentially 4 ace draw
            while self.state[1] < 18: #stand on 17
                draw = self.state[0].draw()
                if draw == 11: #aces
                    self.state[3] = self.state[3] + 1
                self.state[1] = self.state[1] + draw

            if self.state[1] > 21 & self.state[3] > 0: #if bust but have ace, reduce
                self.state[1] = self.state[1] - 10
            else:
                break
        
        #dealer bust or player closer to 21
        if self.state[1] > 21 | self.state[1] < self.state[2]:
            return self.win()
        elif self.state[1] == self.state[2]:
            return self.tie()
        else:
            return self.lose()


    #main?
    






















