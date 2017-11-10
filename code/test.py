from Environment import *
from Agent import *
import random

walls = []
walls.append(Wall('circle', **{ 'center': Point(0,0), 'radius': 50 }))
walls.append(Wall('line', **{ 'p1': Point(50,10), 'p2': Point(400,200) }))


agents = []
for _ in range(10):
    agents.append(Agent(random.randint(10,20), 50, (random.randint(10,990), random.randint(10,990)), None))

env = Environment(100, walls, None, agents, {})
viewer = EnvironmentViewer(env)

viewer.draw()

while True:
    pass
