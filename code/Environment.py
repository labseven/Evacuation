import pygame
from pygame.locals import *
from pygame.color import *

class Environment():
	def __init__(self, N=100, wall, conditions):
		self.N = N

	def step(self):
		raise NotImplementedError


class EnvironmentViewer():
	def __init__(self, environment):
		self.environment = environment

	def draw(self):
		raise NotImplementedError
