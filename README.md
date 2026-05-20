This was a short project to experiment with genetic algorithms to play blackjack.
I was inspired to make this after playing Gamble With Your Friends and watching a few videos from Primer (@PrimerBlobs).

The game works simply, dealer stands on 17, player can choose to hit, stand, or double down.
The model is bare, only having one hidden layer of 128 nodes.
The inputs are: how many of each card is left in the deck, what the dealer is showing, what the player's sum is, if the dealer has an ace, if the player has a soft ace, and if it is the first turn
The reward function is basic. The model starts with 0 reward and it increments or decrements if it wins or loses.
I made a variation based on how close it was to getting 21 on top of the win/lose framework. On wins and ties it gains its sum/21 so that it doesn't unnecessarily stand.
The simulation ran 100 models per generation, 1000 games per model per generation, and 100 generations.

The images are really wide as there is a state for every possible combination of the player's hand without mirroring so just zoom in ((A,2) but not (2,A))

Here is the result of the simple reward system:
<img width="12387" height="2577" alt="blackjack_strategy_table" src="https://github.com/QBeeIII/Blackjack-Neural-Network/blob/main/blackjack_strategy_table.png" />

And the result of the second reward system:
<img width="12387" height="2577" alt="blackjack_strategy_table" src="https://github.com/QBeeIII/Blackjack-Neural-Network/blob/main/blackjack_strategy_table%20w%20card%20rewards.png" />

An interesting thing to note is that the models never double down and that is definitely because of how i handled enforcement of the rule. If it wasn't the first turn and the model chose to double down, I set its reward to a large negative number and I guess that it took that as "never double down." I didn't want to convert later double downs into hits because I thought that would make the models confused after the first turn. With masking the doubles and hits past turn 1, these are the results:

Simple reward system:
<img width="12387" height="2577" alt="blackjack_strategy_table" src="" />

Second reward system:
<img width="12387" height="2577" alt="blackjack_strategy_table" src="" />

It doesn't seem to care about doubling down still, likely because doubling down doubles the penalty which would happen more often than it doubles reward.
