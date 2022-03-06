import random
import math
from vector2d import Vector2D





class LineSegment:

    number_of_lines = 0
    def __init__(self, sx, sy, ex, ey, radius):
        self.start_pt = Vector2D(sx, sy)
        self.end_pt = Vector2D(ex, ey)
        self.radius = radius

        self.id = LineSegment.number_of_lines
        LineSegment.number_of_lines += 1

class Ball:

    number_of_balls = 0

    def __init__(self, x, y, radius):
        self.position = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.acceleration = Vector2D(0, 0)
        self.o_position = Vector2D(0, 0)
        self.radius = radius
        self.mass = 10 * self.radius

        self.sim_time_remaining = 0
        self.id = Ball.number_of_balls
        Ball.number_of_balls += 1
