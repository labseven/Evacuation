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
	self.conditions = { 'k': 1.2 * 10**5, 'ka': 2.4 * 10**5 }

	def __init__(self, N=100, walls, exits, agents, conditions):
		self.N = N
		self.walls = walls
		self.exits = exits
		self.agents = agents
		# Conditions: Agent force, Agent repulsive distance, acceleration time, step length,
		self.conditions.update(conditions)


	def step(self):
		raise NotImplementedError


class EnvironmentViewer():
	def __init__(self, environment):
		self.environment = environment

	def draw(self):
		raise NotImplementedError
