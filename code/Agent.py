from Environment import Point

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

	def getDesiredVector(self):
		"""
		Calculates the vector pointing towards the goal.
		"""
		p1 = self.goal.parameters['p1']
		p2 = self.goal.parameters['p2']

		# Test if vertical or horizontal
		if p1.x == p2.x:
			if self.pos.y < p1.y:
				return self.getVectorTo(p1).norm()

			elif self.pos.y > p2.y:
				return self.getVectorTo(p2).norm()

			else:
				direction = 1 if self.pos.x < p1.x else -1
				return Point(direction, 0)
		else:
			if self.pos.x < p1.x:
				return self.getVectorTo(p1).norm()

			elif self.pos.x > p2.x:
				return self.getVectorTo(p2).norm()

			else:
				direction = 1 if self.pos.y < p1.y else -1
				return Point(0, direction)

	def getVectorTo(self, point):
		return point - self.pos
