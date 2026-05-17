import blackjack



# inputs:
#  cards are shown on the table --> what is potentially left in the deck
#  sum of hand
#  dealer showing
# 
#
# 13 nodes for every card's value
#  1,2,3,4 indicating amount left in deck
# 
# 1 node for dealer showing
#  2-11
# 
# 1 node for player sum
#  4-21
# 
# 1 node for player ace
#  0-4
#
# 1 node for bank balance
#  0-inf
#
# 1 node for bet amount
#  ?-?
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
#   tempList = sorted(neuralNetworks, key=lambda x: x.fitness, reverse=True)
#   neuralNetworks = tempList[:(n/10)]
# 
#   #populate
#   for j in range(n/10):
#       neuralNetworks[j].reset(BANK, MIN, MAX)
#       for k in range(9):
#           tempNN = copy.deepcopy(neuralNetworks[j])
#           tempNN.mutate()
#           neuralNetworks.append(tempNN)
# 
# 







































