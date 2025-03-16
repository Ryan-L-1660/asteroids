import pygame
from circleshape import CircleShape
from constants import WHITE, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS # Make sure WHITE is defined in constants.py
import random
import math

class Asteroid(CircleShape):
    containers = None 

    def __init__(self, x, y, radius):
        # initialize parent class 
        CircleShape.__init__(self, x, y, radius)

        self.vertices_offsets = []
        num_vertices = random.randint(6, 10)
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices
            # Vary the radius a bit for each vertex to create lumpiness
            jitter = random.uniform(0.8, 1.2)
            offset_x = self.radius * jitter * math.cos(angle)
            offset_y = self.radius * jitter * math.sin(angle)
            self.vertices_offsets.append((offset_x, offset_y))
    
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
        vertices = []

        
        for offset_x, offset_y in self.vertices_offsets:
            x = int(self.position.x + offset_x)
            y = int(self.position.y + offset_y)
            vertices.append((x, y))



        pygame.draw.polygon(screen, WHITE, vertices, 2)

    def update(self, dt):
        self.position += self.velocity * dt