import pygame
from pygame.locals import *
from pygame.color import *

class Wall():
	def __init__(self, **parameters):
		# type: "circle" | "line", points
		self.parameters = parameters

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
		print("drew agent at ", agent.pos)
	def drawWall(self, wall):
		raise NotImplementedError
