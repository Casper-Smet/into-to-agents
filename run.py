from model import MoneyModel

import matplotlib.pyplot as plt
import numpy as np

model = MoneyModel(50, 10, 10)
for _ in range(100):
    model.step()

agent_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
    
plt.imshow(agent_counts)
plt.colorbar()
plt.show()

agent_wealth = [agent.wealth for agent in model.schedule.agents ]
plt.hist(agent_wealth)
plt.show()

gini = model.datacollector.get_model_vars_dataframe()
gini.plot()
plt.show()