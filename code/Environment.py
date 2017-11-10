import pygame
from pygame.locals import *
from pygame.color import *

DEBUG = False

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tuple = (x,y)

	def __str__(self):
		return "{}, {}".format(self.x, self.y)
	# TODO: Addition subtraction


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


class Exit(Wall):
	pass

class Environment():
	conditions = { 'k': 1.2 * 10**5, 'ka': 2.4 * 10**5 }

	def __init__(self, N, walls, exits, agents, conditions):
		self.N = N
		self.walls = walls
		self.exits = exits
		self.agents = agents
		# Conditions: Agent force, Agent repulsive distance, acceleration time, step length,
		self.conditions.update(conditions)


	def step(self):
		raise NotImplementedError


class EnvironmentViewer():
	BG_COLOR = (0,0,0)

	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	YELLOW = (255, 233, 0)
	RED = (203, 20, 16)

	def __init__(self, environment):
		self.env = environment
		self.screen = pygame.display.set_mode((1000,1000))

	def draw(self):
		self.screen.fill(self.BG_COLOR)

		for agent in self.env.agents:
			self.drawAgent(agent)

		for wall in self.env.walls:
			self.drawWall(wall)

		pygame.display.update()

	def drawAgent(self, agent):
		pygame.draw.circle(self.screen, self.YELLOW, agent.pos, agent.size)
		if(DEBUG): print("drew agent at ", agent.pos)

	def drawWall(self, wall):
		if wall.wallType == 'circle':
			pygame.draw.circle(self.screen, self.WHITE, wall.parameters['center'].tuple, wall.parameters['radius'])
			if(DEBUG): print("drew wall at {}".format(wall.parameters['center']))

		if wall.wallType == 'line':
			pygame.draw.line(self.screen, self.WHITE, wall.parameters['p1'].tuple, wall.parameters['p2'].tuple, 10)
			if(DEBUG): print("drew wall between {} and {}".format(wall.parameters['p1'], wall.parameters['p2']))
