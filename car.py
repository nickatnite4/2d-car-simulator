from math import sin, radians, degrees, copysign
from pygame.math import Vector2

class Car:
    def __init__(self, x, y, angle=0.0, length=4, max_steering=30,max_acceleration=5.0):
        self.position = Vector2(x,y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering

        self.acceleration = 0.0
        self.steering = 0.0
        self.brake_deceleration = 10
        self.rpm = 1000

    def update(self, dt):
        self.velocity += (self.acceleration * dt , 0)
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
        
        if self.position.x*32 > 1280:
            self.position.x = 1280/32
            self.velocity.x = 0
            self.velocity.y = 0
        elif self.position.x*32 < 0:
            self.position.x = 0
            self.velocity.x = 0
            self.velocity.y =0
        elif self.position.y*32 > 720:
            self.position.y = 720/32
            self.velocity.x = 0
            self.velocity.y = 0
        elif self.position.y*32 < 0:
            self.position.y = 0
            self.velocity.x = 0
            self.velocity.y = 0
        else:
            self.position += self.velocity.rotate(-self.angle) * dt
            self.angle += degrees(angular_velocity) * dt