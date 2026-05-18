import torch
import blackjack
import matplotlib.pyplot as plt

model = blackjack.Blackjack()
model.brain.load_state_dict(torch.load("model simple reward.pt", weights_only=True))

data = [[] for _ in range(10)]

valueTable = [11,2,3,4,5,6,7,8,9,10]

rows = ('A','2','3','4','5','6','7','8','9','10')
columns = []
for i in range(10):
    for j in range(i,10):
        sum = valueTable[i]+valueTable[j]
        columns.append(f"({valueTable[i]},{valueTable[j]}) {sum}")


#dealer card
for i in range(10):
    dlr = valueTable[i]
    #player card 1
    for j in range(10):
        plr1 = valueTable[j]
        #player card 2
        for k in range(j,10):
            plr2 = valueTable[k]
            data[i].append(model.runScenario(dlr, plr1, plr2))


fig, ax = plt.subplots(figsize=(20, 10))
ax.axis('off')  # Hide axes

table = ax.table(
    cellText=data,
    rowLabels=rows,
    colLabels=columns,
    cellLoc='center',
    loc='center',
    colWidths=[0.04] * len(columns)  # Adjust width as needed
)

table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1.2, 1.5)

for i in range(len(data)):
    for j in range(len(data[i])):
        cell_value = data[i][j]
        if cell_value == 'hit':
            table[(i+1, j)].set_facecolor('#ffcccc')  # light red
        elif cell_value == 'stand':
            table[(i+1, j)].set_facecolor('#ccffcc')  # light green
        elif cell_value == 'double':
            table[(i+1, j)].set_facecolor('#ccccff')  # light blue

plt.title('Blackjack Strategy Chart\n(Dealer Shows vs Player Hand)', 
          fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('blackjack_strategy_table.png', dpi=300, bbox_inches='tight', facecolor='white')



