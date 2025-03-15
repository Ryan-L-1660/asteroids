import pygame
from circleshape import CircleShape
from constants import WHITE, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS # Make sure WHITE is defined in constants.py
import random

class Asteroid(CircleShape):
    containers = None 

    def __init__(self, x, y, radius):
        # initialize parent class 
        CircleShape.__init__(self, x, y, radius)
    
    def split(self):
        self.kill()

        # if the radius is too small, don't split
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # caluculates new raidus
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # generate rng
        random_angle = random.uniform(20, 50)

        # Create 2 new asteroids

        for angle_multiplier in [1, -1]:
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)

            new_velocity = self.velocity.rotate(random_angle * angle_multiplier)
            new_velocity *= 1.2
            asteroid.velocity = new_velocity

            for container in Asteroid.containers:
                container.add(asteroid)

    

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt