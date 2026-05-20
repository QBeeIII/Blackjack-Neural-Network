import torch
import copy
import blackjack



# inputs:
#  cards are shown on the table --> what is potentially left in the deck
#  sum of hand
#  dealer showing
# 
#
# 10 nodes for every card's value
#  9 nodes, 0-4 for A-9
#  1 node, 0-16 for 10-K
# 
# 1 node for dealer showing
#  2-11
# 
# 1 node for player sum
#  4-21
#
# 1 node for dealer fluid ace
#  0-1 #cant have 2 fluid aces
#  
# 1 node for player fluid ace
#  0-1
#
# 1 node for first turn to enforce double only on first turn
#  0-1
# 
# outputs:
#  hit
#  stand
#  double



# structure ---
# spawn n blackjack objects with it's own NN
#  n % 10 == 0
# randomized weights n stuff
# each plays x rounds
# take the top 10% according to their fitness
# each will create 9 blackjack objects with slightly adjusted weights to their parents
# simulate for a while
# export the best 10 of the final generation
# 
# 
# n = number of neural networks per generation
# g = number of generations
# x = games per generation
# 
# 
# neuralNetworks = [n blackjack objects], (randomization within?)
# 
# for i in range(g):
#   for NN in neuralNetworks:
#       for j in range(x):
#           NN.play()
#
#   #fetch top 10%
#   tempList = sorted(neuralNetworks, key=lambda x: x.reward, reverse=True)
#   neuralNetworks = tempList[:(n/10)]
# 
#   #populate
#   for j in range(n/10):
#       neuralNetworks[j].reset()
#       oldBrain = copy.deepcopy(neuralNetworks[j].brain.state_dict())
#       for k in range(n/10*9):
#           child = blackjack.Blackjack()
#           child.brain.load_state_dict(oldBrain)
#           child.mutate()
#           neuralNetworks.append(child)
# 
# 

n = 10 #10% of neural networks per generation
g = 100 #number of generations
x = 1000 #games per generation

BlackjackObjects = [blackjack.Blackjack() for i in range(n)]

#generation loop
for i in range(g):
    print("Generation " + str(i+1))
    #simulate games
    for blackjackObject in BlackjackObjects:
        for j in range(x):
            blackjackObject.play()
    
    #fetch top 10%
    tempList = sorted(BlackjackObjects, key=lambda x: x.reward, reverse=True)
    BlackjackObjects = tempList[:n]

    #populate
    for j in range(n):
        BlackjackObjects[j].reset()
        oldBrain = copy.deepcopy(BlackjackObjects[j].brain.state_dict())
        for k in range(n*9):
            child = blackjack.Blackjack()
            child.brain.load_state_dict(oldBrain)
            child.mutate()
            BlackjackObjects.append(child)



finalList = sorted(BlackjackObjects, key=lambda x: x.reward, reverse=True)
torch.save(finalList[0].brain.state_dict(), "model.pt")
open("model reward value simple DD.txt", "w").write(str(finalList[0].rewardmem))


































