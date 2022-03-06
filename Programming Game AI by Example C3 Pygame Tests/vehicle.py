
import pygame
import random
import math
from vector2d import Vector2D
from steering import SteeringBehaviour
from steering import Behaviour




class BaseGameEntity:

    m_next_id = None

    def __init__(self, id, x, y):
        self.m_id = id
        self.position = Vector2D(x,y)    # x,y
        self.scale = 20
        self.bounding_radius = 20


    def Update(self):
        raise NotImplementedError()


class MovingEntity(BaseGameEntity):
    m_velocity = Vector2D(0,0)
    m_heading = Vector2D(0,-1)
    m_side = Vector2D(0,0)
    m_mass = 1
    m_max_speed = 10
    m_max_force = 1
    m_max_turn_rate = 3

class Vehicle(MovingEntity):

    def __init__(self, id, x, y):
        BaseGameEntity.__init__(self, id, x, y)
        self.front_pt = self.position + self.m_heading * self.scale;
        self.port_pt = self.position - self.m_heading * self.scale * 0.5 - self.m_heading.perpendicular() * self.scale * 0.5
        self.starboard_pt = self.position - self.m_heading * self.scale * 0.5 + self.m_heading.perpendicular() * self.scale *0.5

        self.steer = SteeringBehaviour(self)
        self.target = None


        self.reference_pt = Vector2D(0,0)
        

    def Update(self, time, wall_list):
        #print("Time: " + str(time))

        steering_force = self.steer.Calculate()

        steering_force += self.steer.WallAvoidance(wall_list)

        #if (self.steer.behaviour != Behaviour.WANDER):
        acceleration = steering_force / self.m_mass
        self.m_velocity += acceleration * time

        self.position += self.m_velocity * time

        if self.m_velocity.lengthsqrd() > 0.0001:
            self.m_heading = Vector2D(self.m_velocity.x, self.m_velocity.y).normalize()
            self.m_side = self.m_heading.perpendicular()

        self.UpdateHeading()



    def UpdateHeading(self):
        self.front_pt = self.position + self.m_heading * self.scale;
        self.port_pt = self.position - self.m_heading * self.scale * 0.5 - self.m_heading.perpendicular() * self.scale * 0.5
        self.starboard_pt = self.position - self.m_heading * self.scale * 0.5 + self.m_heading.perpendicular() * self.scale *0.5


class TargetCircle(BaseGameEntity):
    def __init__(self, id, x, y):
        BaseGameEntity.__init__(self, id, x, y)
        self.m_id = id
        self.position = Vector2D(x,y)    # x,y
        self.scale = 100
        self.bounding_radius = 2

    def Update(self, time):
        self.scale = (math.sin(time)+1) * 5

        #print("scale: " + str(self.scale))

        #self.scale = 10
