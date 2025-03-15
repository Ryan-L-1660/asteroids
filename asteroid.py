import pygame
from circleshape import CircleShape
from constants import WHITE  # Make sure WHITE is defined in constants.py

class Asteroid(CircleShape):
    containers = None 

    def __init__(self, x, y, radius):
        # initialize parent class 
        CircleShape.__init__(self, x, y, radius)
        self.radius = radius
        # velocity will be set by AsteroidField
    

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt