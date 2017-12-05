from Agent import *
from Point import Point

import pygame
from pygame.locals import *
from pygame.color import *
import thinkplot
import random

DEBUG = False


class Wall:
    def __init__(self, wallType, **parameters):
        # type : "circle" | "line", points
        # Circle : type='circle' { "center": Point(x,y), "radius": r }
        # Line : type='line'{ "p1": Point(x1,y1), "p2": Point(x2,y2) }
        self.wallType = wallType
        self.parameters = parameters
        self.checkValid()

    def checkValid(self):
        if self.wallType == 'circle':
            assert isinstance(self.parameters["center"], Point), "Circles need a center"
            assert isinstance(self.parameters["radius"], int), "Radius needs to be an int"

        if self.wallType == 'line':
            assert isinstance(self.parameters['p1'], Point)
            assert isinstance(self.parameters['p2'], Point)


class Goal(Wall):
    """ Defines a goal. Currently, only horizontal and vertical lines are supported. """

    def checkValid(self):
        assert self.wallType == 'line'
        assert isinstance(self.parameters['p1'], Point)
        assert isinstance(self.parameters['p2'], Point)
        assert (self.parameters['p1'].x == self.parameters['p2'].x or self.parameters['p1'].y == self.parameters[
            'p2'].y)

        # p1 should always be smaller than p2
        if (self.parameters['p1'].x == self.parameters['p2'].x):
            if self.parameters['p1'].y > self.parameters['p2'].y:
                p1Temp = self.parameters['p1']
                self.parameters['p1'] = self.paramters['p2']
                self.parameters['p2'] = p1Temp
        elif (self.parameters['p1'].y == self.parameters['p2'].y):
            if self.parameters['p1'].x > self.parameters['p2'].x:
                p1Temp = self.parameters['p1']
                self.parameters['p1'] = self.paramters['p2']
                self.parameters['p2'] = p1Temp


class Environment():
    conditions = {'k': 1.2 * 10 ** 5, 'ka': 2.4 * 10 ** 5}

    def __init__(self, N, walls, goals, agents, conditions, instruments):
        self.N = N
        self.walls = walls
        self.goals = goals
        self.agents = agents
        self.instruments = instruments
        # Conditions: Agent force, Agent repulsive distance, acceleration time, step length,
        self.conditions.update(conditions)

    def step(self):
        for agent in self.agents:
            # print(agent.desiredDirection)
            selfDriveForce = agent.selfDriveForce()
            pairForce = Point(0, 0)
            wallForce = Point(0, 0)
            for wall in self.walls:
                wallForce += agent.wallForce(wall)
            for agent2 in self.agents:
                if agent.index == agent2.index:
                    continue
                pairForce += agent.pairForce(agent2)
            netForce = selfDriveForce + pairForce + wallForce
            agent.move(netForce)

        self.updateInstruments()

    def updateInstruments(self):
        for instrument in self.instruments:
            instrument.update(self)

    def plot(self, num):
        self.instruments[num].plot()


class EnvironmentViewer():
    BG_COLOR = Color(0, 0, 0)

    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    YELLOW = Color(255, 233, 0)
    RED = Color(203, 20, 16)
    GOAL = Color(252, 148, 37)

    def __init__(self, environment):
        self.env = environment
        self.screen = pygame.display.set_mode((1000, 1000))

    def draw(self):
        self.screen.fill(self.BG_COLOR)

        for agent in self.env.agents:
            self.drawAgent(agent)

        for wall in self.env.walls:
            self.drawWall(wall)

        for goal in self.env.goals:
            self.drawGoal(goal)

        pygame.display.update()

    def drawAgent(self, agent):
        # Draw agent
        pygame.draw.circle(self.screen, self.YELLOW, agent.pos.tuple, agent.size)
        # Draw desired vector
        pygame.draw.line(self.screen, self.YELLOW, agent.pos.tuple, (agent.pos + (agent.desiredDirection * 30)).tuple)
        if (DEBUG): print("drew agent at ", agent.pos)

    def drawWall(self, wall, color=WHITE):
        if wall.wallType == 'circle':
            pygame.draw.circle(self.screen, color, wall.parameters['center'].tuple, wall.parameters['radius'])
            if (DEBUG): print("drew wall at {}".format(wall.parameters['center']))

        if wall.wallType == 'line':
            pygame.draw.line(self.screen, color, wall.parameters['p1'].tuple, wall.parameters['p2'].tuple, 10)
            if (DEBUG): print("drew wall between {} and {}".format(wall.parameters['p1'], wall.parameters['p2']))

    def drawGoal(self, goal):
        self.drawWall(goal, color=self.GOAL)


class Instrument():
    """ Instrument that logs the state of the environment"""

    def __init__(self):
        self.metric = []

    def plot(self, **options):
        thinkplot.plot(self.metric, **options)
        thinkplot.show()


class ReachedGoal(Instrument):
    """ Logs the number of agents that have escaped """

    def update(self, env):
        self.metric.append(self.countReachedGoal(env))

    def countReachedGoal(self, env):
        num_escaped = 0

        for agent in env.agents:
            if agent.pos.x > agent.goal.parameters['p1'].x:
                num_escaped += 1
        return num_escaped


def runExperiment(roomHeight=1000,
                  roomWidth=800,
                  barrier={'radius': 50, 'pos': Point(-100, 0)},  # pos is relative to door center
                  doorWidth=100,
                  numAgents=50,
                  agentSize=20,
                  agentMass=50,
                  desiredSpeed=4):
    walls = []
    # Only add barrier if its radius is above 0
    if barrier:
        walls.append(Wall('circle',
                          **{'center': Point(roomWidth + barrier['pos'].x, roomHeight // 2 + barrier['pos'].y),
                             'radius': barrier['radius']}))

    walls.append(Wall('line', **{'p1': Point(0, 0), 'p2': Point(roomWidth, 0)}))  # Top
    walls.append(Wall('line', **{'p1': Point(0, 0), 'p2': Point(0, roomHeight)}))  # Left
    walls.append(Wall('line', **{'p1': Point(0, roomHeight), 'p2': Point(roomWidth, roomHeight)}))  # Bottom

    walls.append(Wall('line', **{'p1': Point(roomWidth, 0),
                                 'p2': Point(roomWidth, roomHeight / 2 - doorWidth / 2)}))  # Top Doorway
    walls.append(Wall('line', **{'p1': Point(roomWidth, roomHeight / 2 + doorWidth / 2),
                                 'p2': Point(roomWidth, roomHeight)}))  # Bottom Doorway

    goals = []
    goals.append(Goal('line', **{'p1': Point(roomWidth, roomHeight / 2 - doorWidth / 2),
                                 'p2': Point(roomWidth, roomHeight / 2 + doorWidth / 2)}))

    instruments = []
    instruments.append(ReachedGoal())

    agents = []
    for _ in range(numAgents):
        # Agent(size, mass, pos, goal, desiredSpeed = 4))
        size = random.randint(.9 * agentSize, 1.1 * agentSize)
        mass = agentMass
        pos = Point(random.randint(agentSize, roomWidth / 2 - agentSize),
                    random.randint(agentSize, roomHeight - agentSize))
        goal = goals[0]

        agents.append(Agent(size, mass, pos, goal, desiredSpeed=desiredSpeed))

    env = Environment(100, walls, goals, agents, {}, instruments)
    viewer = EnvironmentViewer(env)

    viewer.draw()
    env.step()

    # Run until all agents have escaped
    while env.instruments[0].metric[-1] < len(env.agents):
        env.step()

    return env.instruments[0].metric


if __name__ == '__main__':
    defaultExperiment = runExperiment()
    print(defaultExperiment)

    thinkplot.plot(defaultExperiment)
    thinkplot.show()
