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

		# If past the goal move right
		if self.pos.x >= p1.x:
			return Point(1, 0)

		# If above the goal, move to top point
		elif self.pos.y < p1.y:
			return self.getVectorTo(p1).norm()

		# If below the goal, move to bottom point
		elif self.pos.y > p2.y:
			return self.getVectorTo(p2).norm()

		# If directly in front of the goal, move right
		else:
			return Point(1, 0)


	def getVectorTo(self, point):
		return point - self.pos
