from Environment import *
from Agent import *
import random

agents = []
for _ in range(10):
    agents.append(Agent(random.randint(10,20), 50, (random.randint(10,990), random.randint(10,990)), None))

env = Environment(100, [], None, agents, {})
viewer = EnvironmentViewer(env)

viewer.draw()

while True:
    pass
