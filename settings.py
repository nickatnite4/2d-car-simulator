
import sys
import time
from math import sin, radians, degrees, copysign, floor, ceil
import pygame

from car import Car


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car Tutorial")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        car = Car(100/32,75/32)
        image = pygame.image.load('car4.png').convert_alpha()

        wheel_rpm = car.rpm / (car.current_gear * car.differential_gear * 60 / 2 * 3.14)
        print(wheel_rpm)

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            
            # User input
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 1 * dt
            
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 1 * dt
            elif pressed[pygame.K_SPACE]:
                if car.velocity.x != 0:
                    car.acceleration = copysign(car.max_acceleration, -car.velocity.x)
            else:
                car.acceleration = 0
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 45 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 45 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt) 

            # Drawing
            self.screen.fill((0,0,0))
            rotate = pygame.transform.rotate(image, car.angle)
            rect = rotate.get_rect()
            ppu = 32
            self.screen.blit(rotate, car.position * ppu - (rect.width / 2, rect.height / 2))
            
            pygame.display.flip()

            self.clock.tick(self.ticks)
        
        pygame.quit()




def interpolate(x):
    rpm = [1000, 2000, 3000, 4000, 5000, 6000]
    torque = [290, 325, 340, 350, 345, 290]

    if x not in rpm:
        temp = floor(x/1000)
        x_1 = temp * 1000
        temp = ceil(x/1000)
        x_2 = temp * 1000
        y_1 = torque[rpm.index(x_1)]
        y_2 = torque[rpm.index(x_2)]
        instant_torque = y_1 + (x - x_1) * ((y_2- y_1)/(x_2-x_1))
    else:
        instant_torque = torque[rpm.index(x)]
    
    return instant_torque