from mesa import Agent
# Mostly sourced from https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html
# steal_money was my own addition.
class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.in_city = False
        self.alive = True

    def move(self):
        """Move to a random position in an agent's neighborhood"""
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def interact(self):
        """"Give away or steal money based on current wealth"""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            if self.wealth == 0:
                self.steal_money(cellmates)
            elif self.wealth > 0:
                self.give_money(other)

    def give_money(self, other):
        """Give one of your wealth to other"""
        other.wealth += 1
        self.wealth -= 1

    def steal_money(self, others):
        """Steal and redistribute wealth, Robin Hood style"""
        wallet = 0

        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=2)
        
        for neighbor in neighbors:
            if neighbor.in_city == False:
                if wallet == len(others) + 1:
                    break
                elif neighbor.wealth > 1:
                    wallet += 1
                    neighbor.wealth -= 1
            # else:
            #     self.alive = False
            #     return None
        
        for other in others:
            if wallet > 0:
                other.wealth += 1
                wallet -= 1
        if wallet > 0:
            self.wealth += wallet
            wallet = 0        
        

    def step(self):
        if self.alive:
            if not self.in_city:
                self.move()            
            self.interact()

