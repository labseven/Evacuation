from Agent import *
from Point import Point

import pygame
from pygame.locals import *
from pygame.color import *
import thinkplot
import random

from datetime import datetime
import pickle
import pandas

import sys

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
            # assert isinstance(self.parameters["radius"], int), "Radius needs to be an int"

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

    pygameScale = 100

    def __init__(self, environment):
        self.env = environment
        self.screen = pygame.display.set_mode((1000,1000))

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
        pygame.draw.circle(self.screen, self.YELLOW, agent.pos.pygame, int(agent.size * self.pygameScale))
        # Draw desired vector
        pygame.draw.line(self.screen, self.YELLOW, agent.pos.pygame, (agent.pos + (agent.desiredDirection)).pygame)
        if(DEBUG): print("drew agent at ", agent.pos)

    def drawWall(self, wall, color=WHITE):
        if wall.wallType == 'circle':
            pygame.draw.circle(self.screen, color, wall.parameters['center'].pygame, int(wall.parameters['radius'] * self.pygameScale))
            if(DEBUG): print("drew wall at {}".format(wall.parameters['center']))

        if wall.wallType == 'line':
            pygame.draw.line(self.screen, color, wall.parameters['p1'].pygame, wall.parameters['p2'].pygame, 10)
            if(DEBUG): print("drew wall between {} and {}".format(wall.parameters['p1'], wall.parameters['p2']))

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



def randFloat(minVal, maxVal):
    return random.random() * (maxVal - minVal) + minVal

def runSimulation(roomHeight=10,
                  roomWidth=8,
                  barrier={ 'radius': .3, 'pos': Point(-1,0)}, # pos is relative to door center
                  doorWidth=1.5,
                  numAgents=50,
                  agentMass=80,
                  desiredSpeed=4,
                  view=False):

    walls = []
    # Only add barrier if its radius is above 0
    if barrier:
        walls.append(Wall('circle', **{ 'center': Point(roomWidth + barrier['pos'].x, roomHeight//2 + barrier['pos'].y), 'radius': barrier['radius'] }))

    walls.append(Wall('line', **{ 'p1': Point(0,0), 'p2': Point(roomWidth, 0) })) # Top
    # walls.append(Wall('line', **{ 'p1': Point(0,0), 'p2': Point(0, roomHeight) })) # Left
    walls.append(Wall('line', **{ 'p1': Point(0,roomHeight), 'p2': Point(roomWidth, roomHeight) })) # Bottom

    walls.append(Wall('line', **{ 'p1': Point(roomWidth,0), 'p2': Point(roomWidth, roomHeight/2 - doorWidth/2) })) # Top Doorway
    walls.append(Wall('line', **{ 'p1': Point(roomWidth, roomHeight/2 + doorWidth/2), 'p2': Point(roomWidth, roomHeight) })) # Bottom Doorway



    goals = []
    goals.append(Goal('line', **{ 'p1': Point(roomWidth, roomHeight/2 - doorWidth/2), 'p2': Point(roomWidth, roomHeight/2 + doorWidth/2) }))

    instruments = []
    instruments.append(ReachedGoal())


    agents = []
    for _ in range(numAgents):
        # Agent(size, mass, pos, goal, desiredSpeed = 4))
        size = randFloat(.25, .35)
        mass = agentMass
        pos = Point(randFloat(.5, 2*roomWidth/3 - .5), randFloat(.5,roomHeight-.5))
        goal = goals[0]

        agents.append(Agent(size, mass, pos, goal, desiredSpeed=desiredSpeed))

    env = Environment(100, walls, goals, agents, {}, instruments)

    if view:
        viewer = EnvironmentViewer(env)
        viewer.draw()

    env.step()

    # print(env.instruments[0].metric)
    # Run until all agents have escaped
    while env.instruments[0].metric[-1] < len(env.agents):
        env.step()
        if view:
            viewer.draw()
            # pygame.event.wait()
        if (len(env.instruments[0].metric) % 100 == 0):
            message = "num escaped: {}, step: {}".format(env.instruments[0].metric[-1], len(env.instruments[0].metric))
            sys.stdout.write('\r' + str(message) + ' ' * 20)
            sys.stdout.flush() # important

        if len(env.instruments[0].metric) == 6000:
            break

    print()
    return env.instruments[0].metric

def runExperiment():
    x = []
    time_to_escape = []
    for num_agents in range(50, 500, 50):
        statistics = runSimulation()

        x.append(num_agents)
        time_to_escape.append(len(statistics))

    export = [x, time_to_escape]
    # with open("{}.pd".format(datetime.time()), "r") as outfile:
    #     pickle.dump(export, outfile)


if __name__ == '__main__':
    simResult = runSimulation( view=True, desiredSpeed=2, numAgents=500, roomHeight=20, roomWidth=10)
    print(simResult)

    # thinkplot.plot(defaultExperiment)
    # thinkplot.show()
