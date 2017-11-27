import pygame
from pygame.locals import *
from pygame.color import *
from math import sqrt

DEBUG = False

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tuple = (x,y)

	def __str__(self):
		return "{}, {}".format(self.x, self.y)

	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __mul__(self, scalar):
		return Point(self.x * scalar, self.y * scalar)

	def __truediv__(self, scalar):
		return Point(self.x / scalar, self.y / scalar)

	def mag(self):
		return sqrt((self.x**2) + (self.y**2))

	def norm(self):
		return self / self.mag()

class Wall():
	def __init__(self, wallType, **parameters):
		# type: "circle" | "line", points
		# Circle: type='circle' { "center": Point(x,y), "radius": r }
		# Line: type='line'{ "p1": Point(x1,y1), "p2": Point(x2,y2) }
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
		assert (self.parameters['p1'].x == self.parameters['p2'].x or  self.parameters['p1'].y == self.parameters['p2'].y)


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
	conditions = { 'k': 1.2 * 10**5, 'ka': 2.4 * 10**5 }

	def __init__(self, N, walls, goals, agents, conditions):
		self.N = N
		self.walls = walls
		self.goals = goals
		self.agents = agents
		# Conditions: Agent force, Agent repulsive distance, acceleration time, step length,
		self.conditions.update(conditions)


	def step(self):
		for agent in self.agents:
			print(agent.getDesiredVector())


class EnvironmentViewer():
	BG_COLOR = Color(0,0,0)

	BLACK  = Color(0, 0, 0)
	WHITE  = Color(255, 255, 255)
	YELLOW = Color(255, 233, 0)
	RED    = Color(203, 20, 16)
	GOAL   = Color(252, 148, 37)

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
		pygame.draw.circle(self.screen, self.YELLOW, agent.pos.tuple, agent.size)
		# Draw desired vector
		pygame.draw.line(self.screen, self.YELLOW, agent.pos.tuple, (agent.pos + (agent.getDesiredVector()*30)).tuple)
		if(DEBUG): print("drew agent at ", agent.pos)

	def drawWall(self, wall, color=WHITE):
		if wall.wallType == 'circle':
			pygame.draw.circle(self.screen, color, wall.parameters['center'].tuple, wall.parameters['radius'])
			if(DEBUG): print("drew wall at {}".format(wall.parameters['center']))

		if wall.wallType == 'line':
			pygame.draw.line(self.screen, color, wall.parameters['p1'].tuple, wall.parameters['p2'].tuple, 10)
			if(DEBUG): print("drew wall between {} and {}".format(wall.parameters['p1'], wall.parameters['p2']))

	def drawGoal(self, goal):
		self.drawWall(goal, color=self.GOAL)
