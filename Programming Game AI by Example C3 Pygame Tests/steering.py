from vector2d import Vector2D

from enum import Enum
from enum import IntEnum
import random
import math

class LineSegment():
    def __init__(self, id, x1, y1, x2, y2):
        self.m_id = id
        self.start_point = Vector2D(x1,y1)
        self.end_point = Vector2D(x2,y2)
        self.normal = Vector2D(x2-x1, y2-y1).perpendicular()

class Behaviour(Enum):
    SEEK = 0
    FLEE = 1
    ARRIVE = 2
    WANDER = 3
    STANDBY = 99

class Deceleration(IntEnum):
    SLOW = 0
    NORMAL = 2
    FAST = 4



class SteeringBehaviour:

    def __init__(self, m_vehicle):
        self.vehicle = m_vehicle
        self.behaviour = Behaviour.ARRIVE

        self.wander_radius = 20
        self.wander_distance = 40
        self.wander_jitter = 0.7
        #self.wander_target = self.vehicle.m_heading * (self.wander_distance + self.wander_radius)

        self.wander_target = Vector2D(math.cos(random.randrange(-1,1)) * self.wander_radius, math.sin(random.randrange(-1,1)) * self.wander_radius)
        self.wander_target += self.vehicle.m_heading * (self.wander_distance - self.wander_radius)

        #self.new_target = Vector2D(0,0)

        self.wander_interval = 2
        self.wander_counter = 0
        self.change = Vector2D(0,0)


        self.feeler_list = []
        self.feeler_detection_length = 50


    def Seek(self, target_pos):

        if self.vehicle.position.distance_to(target_pos) < 0.5:
            self.vehicle.m_velocity = Vector2D(0,0)
            return Vector2D(0,0)
            #return - self.vehicle.m_velocity

        desired_velocity = Vector2D(target_pos.x - self.vehicle.position.x, target_pos.y - self.vehicle.position.y).normalize()
        desired_velocity *= self.vehicle.m_max_speed

        return desired_velocity - self.vehicle.m_velocity


    def Flee(self, target_pos):

        panic_distance = 300
        if self.vehicle.position.distance_to(target_pos) > panic_distance:
            #print("Not scared")
            return - self.vehicle.m_velocity

        #print("scared")
        desired_velocity = Vector2D(self.vehicle.position.x - target_pos.x, self.vehicle.position.y - target_pos.y).normalize()
        desired_velocity *= self.vehicle.m_max_speed

        return desired_velocity - self.vehicle.m_velocity


    def Arrive(self, target_pos, decelerate):

        to_target = Vector2D(target_pos.x - self.vehicle.position.x, target_pos.y - self.vehicle.position.y)

        to_target_dist = abs(to_target)

        if to_target_dist > 0.5:
            deceleration_tweaker = 0.5

            speed = to_target_dist / deceleration_tweaker * int(decelerate)
            speed = min(speed, self.vehicle.m_max_speed)
            desired_velocity = to_target * speed / to_target_dist
            return desired_velocity - self.vehicle.m_velocity

        #if self.vehicle.position.distance_to(target_pos) < 0.5:
        self.vehicle.m_velocity = Vector2D(0,0)
        return Vector2D(0,0)

        #return Vector2D(0,0)

    def Wander(self):
        self.wander_counter += 1

        if self.wander_counter == self.wander_interval:
            self.wander_counter = 0
            self.change = Vector2D(random.uniform(-1,1) * self.wander_jitter, random.uniform(-1, 1) * self.wander_jitter)
            self.wander_target += self.change
            self.wander_target = self.wander_target.normalize() * (self.wander_radius)

            #self.wander_target += self.vehicle.m_heading * self.wander_distance

            # performs better without this hmm why
            self.wander_target += self.vehicle.m_velocity.normalize() * (self.wander_distance - self.wander_radius)


            final_target = (self.wander_target).normalize() * self.vehicle.m_max_speed - self.vehicle.m_velocity

            #print("heading: " + str(self.vehicle.m_heading))

            #    print("wander: " + str(final_target))

            return final_target

        #return (final_target).normalize() * self.vehicle.m_max_speed - self.vehicle.m_velocity
        return Vector2D(0,0)


    def Calculate(self):

        if self.behaviour == Behaviour.SEEK:
            return self.Seek(self.vehicle.target)
        if self.behaviour == Behaviour.FLEE:
            return self.Flee(self.vehicle.target)
        if self.behaviour == Behaviour.ARRIVE:
            return self.Arrive(self.vehicle.target, Deceleration.NORMAL)
        if self.behaviour == Behaviour.WANDER:
            return self.Wander()
        else: #self.behaviour == Behaviour.STANDY:
            return Vector2D(0,0)

    def CreateFeelers(self):
        self.feeler_list.clear()
        feeler = Vector2D(self.vehicle.m_heading.x, self.vehicle.m_heading.y).normalize() * self.feeler_detection_length
        self.feeler_list.append(feeler)

        feeler += Vector2D(self.vehicle.m_side.x, self.vehicle.m_side.y) * self.feeler_detection_length / 2;
        feeler = feeler.normalize() * self.feeler_detection_length
        self.feeler_list.append(feeler)

        feeler -= Vector2D(self.vehicle.m_side.x, self.vehicle.m_side.y) * self.feeler_detection_length;
        feeler = feeler.normalize() * self.feeler_detection_length
        self.feeler_list.append(feeler)

    def WallAvoidance(self, wall_list):
        self.CreateFeelers()

        dist_to_this_ip = 0
        dist_to_closest_ip = math.inf

        closest_wall = None

        steering_force = Vector2D(0,0)
        pt = Vector2D(0,0)
        closest_point = Vector2D(0,0)

        for f in self.feeler_list:
            for wall in wall_list:
                intersected, dist_to_this_ip, cp = self.LineIntersection2D(self.vehicle.position, Vector2D(self.vehicle.position.x + f.x, self.vehicle.position.y + f.y), wall.start_point, wall.end_point)

                if intersected:
                    print("Intersected1")
                    if dist_to_this_ip < dist_to_closest_ip:
                        dist_to_closest_ip = dist_to_this_ip
                        closest_wall = wall
                        closest_point = cp

            if closest_wall:
                overshoot = Vector2D(f.x - closest_point.x, f.y - closest_point.y)
                steering_force = closest_wall.normal * abs(overshoot)

            # end wall for loop
        # end feeler for loop

        return steering_force



    def LineIntersection2D(self, A, B, C, D):
        denominator = (B.x-A.x)*(D.y-C.y)-(B.y-A.y)*(D.x-C.x)

        if denominator == 0:
            return False, 0, 0

        rTop = (A.y-C.y)*(D.x-C.x)-(A.x-C.x)*(D.y-C.y)
        sTop = (A.y-C.y)*(B.x-A.x)-(A.x-C.x)*(B.y-A.y)

        #pxTop = (A.x * B.y - A.y*B.x) * (C.x - D.x) - (A.x - B.x) * (C.x*D.y - C.y*D.x)
        #pyTop = (A.x * B.y - A.y*B.x) * (C.y - D.y) - (A.y - B.y) * (C.x*D.y - C.y*D.x)

        r = rTop / denominator
        s = sTop / denominator

        #print("s: " + str(s))
        #print("d: " + str(denominator))

        if ((r > 0) and (r < 1) and (s > 0) and (s < 1)):
            print("r: " + str(r))
            #intersection_pt =  AB * r
            #print("Intersected")
            self.vehicle.reference_pt = Vector2D(A.x + (B.x - A.x)*r, A.y + (B.y - A.y)*r)
            return True, A.distance_to(B) * r, Vector2D(A.x + (B.x - A.x)*r, A.y + (B.y - A.y)*r)

        return False, 0, 0
