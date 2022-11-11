import math
import mesa
import random
import time


class CleanerAgent(mesa.Agent):
    # An agent with fixed initial wealth.

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.counter = 0
        
    def step(self):
        if self.model.porcentaje_celdas_limpias() >= 0.99:
            self.model.final_time = time.time()
        else:
            self.move()
            self.clean()
            self.counter = self.counter + 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def clean(self):
        if not self.model.isDirty(self.pos):
            self.model.setDirty(self.pos)
        pass
    

class CleanerModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, percent):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.celdas_suc = math.ceil((width * height) * percent)
        self.celdas_lim = math.ceil((width * height) * (1 - percent))

        self.initial_time = time.time()
        self.final_time = 0

        self.dirty_matrix = [[False for _ in range(height)] for _ in range(width)]
        for i in range(self.celdas_suc):
            rand_x = random.randint(0, width - 1)
            rand_y = random.randint(0, height - 1)
            self.dirty_matrix[rand_x][rand_y] = True

        # Create agents
        for i in range(self.num_agents):
            a = CleanerAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            # x = self.random.randrange(self.grid.width)
            # y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (1, 1))
    
    def step(self):
        # Advance the model by one step.
        self.schedule.step()

    def isDirty(self, new_position):
        x, y = new_position
        return self.dirty_matrix[x][y]
        pass

    def setDirty(self, new_position):
        self.celdas_suc = self.celdas_suc - 1
        self.celdas_lim = self.celdas_lim + 1
        x, y = new_position
        self.dirty_matrix[x][y] = False

        if self.celdas_suc == 0:
            self.final_time = time.time()
    pass

    def total_movimiento(self):
        return [agent.counter for agent in self.schedule.agents]
        pass

    def porcentaje_celdas_limpias(self):
        return self.celdas_lim / (self.celdas_lim + self.celdas_suc)
        pass

    def program_execution_time(self):
        print('tiempo de ejecucion', self.final_time - self.initial_time, 'segundos')
        pass
    
