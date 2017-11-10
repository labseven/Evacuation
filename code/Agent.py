class Agent():
	def __init__(self, size, mass, pos, goal, desiredSpeed = 4):
		"""
		"""
		self.size = size
		self.mass = mass
		self.pos = pos
		self.velocity = Point(0,0)
		self.desiredSpeed = desiredSpeed
		self.goal = goal

class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

	# TODO: Addition subtraction
