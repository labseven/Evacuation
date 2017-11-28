from Environment import Point
import math


class Agent:
    def __init__(self, size, mass, pos, goal, desiredSpeed=4):
        self.size = size  # radius
        self.mass = mass
        self.pos = pos                    # current position: Point object
        self.velocity = Point(0, 0)       # current velocity: Point object
        self.desiredSpeed = desiredSpeed  # preferred speed: float
        self.goal = goal                  # exit: Goal object
        # TODO: add maximum of velocity?

    @property
    def desiredDirection(self):
        """ Calculates the unit vector pointing towards the goal. """
        p1 = self.goal.parameters['p1']
        p2 = self.goal.parameters['p2']

        # Test if vertical or horizontal
        if p1.x == p2.x:
            if self.pos.y < p1.y:
                return self.vectorTo(p1).norm()

            elif self.pos.y > p2.y:
                return self.vectorTo(p2).norm()

            else:
                direction = 1 if self.pos.x < p1.x else -1
                return Point(direction, 0)
        else:
            if self.pos.x < p1.x:
                return self.vectorTo(p1).norm()

            elif self.pos.x > p2.x:
                return self.vectorTo(p2).norm()

            else:
                direction = 1 if self.pos.y < p1.y else -1
                return Point(0, direction)

    def vectorTo(self, point):
        return point - self.pos

    def move(self, force):
        """ update step - move to goal during unit time """
        time = 1  # TODO: needed to define in simulator
        self.pos = self.pos + self.velocity * time
        self.velocity = self.velocity + force / self.mass * time

    def wallForce(self, wall):

        # psychological force
        # young and tangential force

    def interactionFoce(self, other):
        distance = (self.pos - other.pos).mag
        # psychological force
        # young and tangential force

    def selfDrive(self):
        desiredVelocity = self.desiredDirection * self.desiredSpeed
        delta = desiredVelocity - self.velocity


    def wallPsychologicalForce(self, r):
        # coefficient

        # TODO: what is r?
        A = 0.25
        B = 0.08
        return A * math.exp(-(r-0.5*self.size)/B)