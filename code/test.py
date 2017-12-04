from Environment import *
from Agent import *
import random
import timeit

walls = []
walls.append(Wall('circle', **{ 'center': Point(600,600), 'radius': 50 }))
walls.append(Wall('line', **{ 'p1': Point(900,400), 'p2': Point(950, 500) }))

goals = []
goals.append(Goal('line', **{ 'p1': Point(300,100), 'p2': Point(300,300) }))

instruments = []
instruments.append(ReachedGoal())

agents = []
for _ in range(10):
    # Agent(size, mass, pos, goal, desiredSpeed = 4))
    size = random.randint(10,20)
    mass = 50
    pos = Point(random.randint(10,990), random.randint(10,990))
    goal = goals[0]

    agents.append(Agent(size, mass, pos, goal))

env = Environment(100, walls, goals, agents, {}, instruments)
viewer = EnvironmentViewer(env)

viewer.draw()
env.step()

for _ in range(50):
    env.step()

env.plot(0)

while True:
    pass
