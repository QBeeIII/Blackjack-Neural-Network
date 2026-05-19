import random
import torch
import neuralNetwork as BJNN

# I wanted to see how the model would do if it could set the bet amount
#  but I couldn't figure out a way to make the model have bet amount
#  as an input AND output
#  so stuff relating to bets and bank are commented out
#  doubling down does increase score by 2 instead of 1 though
# BANK = 1000 #starting money
# MIN = 10 #minbet
# MAX = 500 #maxbet

class Deck:
    def __init__(self):
        #aces are initially 11 and reduced later
        self.deck = [11,2,3,4,5,6,7,8,9,10,10,10,10] * 4
        #             A 2 3 4 5 6 7 8 9 [10-K]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)
        self.deckCount = [4,4,4,4,4,4,4,4,4,16]
        # self.drawn = []
        self.index = 0
    
    def draw(self):
        index = self.index
        self.index = self.index + 1
        draw = self.deck[index]
        if draw == 11:
            self.deckCount[0] = self.deckCount[0] - 1
        else:
            self.deckCount[draw-1] = self.deckCount[draw-1] - 1
        # self.drawn.append(self.deck[index])
        return draw
    
    def forceDraw(self, value):
        self.deck.remove(value)
        self.deck.append(value)
        #we have 52 items so putting it at the end is sufficient
        if value == 11:
            self.deckCount[0] = self.deckCount[0] - 1
        else:
            self.deckCount[value-1] = self.deckCount[value-1] - 1
        return value

        



class Blackjack:
    def __init__(self):
        #reward memory
        self.reward = 0
        self.rewardmem = 0
        # self.reset(BANK, MIN, MAX)
        self.reset()
        #make neural network
        self.brain = BJNN.DQN(15, 3)
        
    
    # def reset(self, bank, min, max):
    def reset(self):
        self.state = [#             index (including card counts)
            Deck(),#                0 (10)
            0, #dealer showing      1 (11)
            0, #player showing      2 (12)
            0, #dealer fluid aces   3 (13)
            0, #player fluid aces   4 (14)
            1  #first turn          5 (15)
            ]
        self.rewardmem = self.reward
        self.reward = 0
        self.wager = 1 #bet
        self.firstTurn = True
        # self.bank = bank
        # self.bet = min
        # self.pot = 0
        # self.min = min
        # self.max = max

    def endRound(self):
        self.state[0].shuffle()
        self.state[1] = 0
        self.state[2] = 0
        self.state[3] = 0
        self.state[4] = 0
        self.state[5] = 1
        self.firstTurn = True
        # self.pot = 0


    def lose(self):
        self.endRound()
        return 0

    def win(self):
        # self.bank = self.bank + 2*self.pot
        self.reward = self.reward + 2*self.wager + self.state[2]/21
        self.endRound()
        return 1
    
    def tie(self):
        # self.bank = self.bank + self.pot
        self.reward = self.reward + self.wager + self.state[2]/21
        self.endRound()
        return 2

    # PLAYER ACTIONS: start, hit, double, stand
    # returns:
    # -1 = game continues
    #  0 = loss
    #  1 = win
    #  2 = tie
    def deal(self):
        # self.pot = self.bet
        # self.bank = self.bank - self.bet
        self.reward = self.reward - 1

        #dealer
        draw = self.state[0].draw()
        if draw == 11:
            self.state[3] = 1
        self.state[1] = draw

        #player
        for i in range(2):
            draw = self.state[0].draw()
            if draw == 11:
                self.state[4] = self.state[4] + 1
            self.state[2] = self.state[2] + draw
        
        #drew 2 aces
        if self.state[2] > 21 and self.state[4] > 0:
            self.state[2] = self.state[2] - 10
            self.state[4] = self.state[4] - 1
        
        if self.state[2] == 21:
            return self.stand()
        return -1

    def hit(self):
        if self.firstTurn:
            self.firstTurn = False
            self.state[5] = 0
        
        draw = self.state[0].draw()
        
        if draw == 11:
            self.state[4] = self.state[4] + 1 #ace count
        self.state[2] = self.state[2] + draw

        #bust but have ace
        if self.state[2] > 21 and self.state[4] > 0:
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
        if self.firstTurn:
            self.firstTurn = False
            self.state[5] = 0
        else:
            return self.hit()
        
        # self.pot = 2*self.bet
        # self.bank = self.bank - self.bet
        self.reward = self.reward - 1

        result = self.hit()
        if result >= 0:
            return result
        else:
            return self.stand()

    def stand(self):
        if self.firstTurn:
            self.firstTurn = False
            self.state[5] = 0

        #reveal 2nd card
        self.state[1] = self.state[0].draw()
        
        #dealers turn
        while self.state[1] < 17: #stand on 17
            draw = self.state[0].draw()
            if draw == 11:
                self.state[3] = self.state[3] + 1
            self.state[1] = self.state[1] + draw

            if self.state[1] > 21 and self.state[3] > 0: #if bust but have ace, reduce
                self.state[1] = self.state[1] - 10
                self.state[3] = self.state[3] - 1
        
        #dealer bust or player closer to 21
        if self.state[1] > 21 or self.state[1] < self.state[2]:
            return self.win()
        elif self.state[1] == self.state[2]:
            return self.tie()
        else:
            return self.lose()
    
    #a single game
    def play(self):
        result = self.deal()
        while result == -1:
            with torch.no_grad():
                action = self.brain(self.stateAsTensor()).max(1)[1].item()
            if action == 0:
                result = self.hit()
            elif action == 1:
                result = self.stand()
            else:
                result = self.double()


    def mutate(self):
        mutationStrength = 0.1
        for param in self.brain.parameters():
            param.data += torch.randn_like(param) * mutationStrength

    def stateAsTensor(self):
        #original values
        temp = self.state[0].deckCount.copy()
        temp.extend(self.state[1:6])

        #normalize to 0-1
        for i in range(10):
            temp[i] = temp[i]/4 #card counts to 0-1
        temp[10] = (temp[10]-2)/9 #dealer showing to 0-1
        # the prereq for this is that the game has not ended, so [4-20] ->  17 states
        temp[11] = (temp[11]-4)/17 #player sum to 0-1

        return torch.tensor(temp, dtype=torch.float32).unsqueeze(0)


    def runScenario(self, dealerShow, playerShow1, playerShow2):
        self.reset()
        self.state[1] = self.state[0].forceDraw(dealerShow)
        self.state[2] = self.state[0].forceDraw(playerShow1) + self.state[0].forceDraw(playerShow2)
        #aces
        if dealerShow == 11:
            self.state[3] = 1
        if playerShow1 == 11:
            self.state[4] = 1
        if  playerShow2 == 11:
            self.state[4]= self.state[4] + 1
        if self.state[2] > 21 and self.state[4] > 0:
            self.state[2] = self.state[2] - 10
            self.state[4] = self.state[4] - 1
        
        #blackjack start
        if self.state[2] == 21:
            return "stand"
        
        with torch.no_grad():
            action = self.brain(self.stateAsTensor()).max(1)[1].item()
        if action == 0:
            return "hit"
        elif action == 1:
            return "stand"
        else:
            return "double"

                





















