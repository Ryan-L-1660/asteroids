import pygame
from circleshape import CircleShape # importing the only thing I need from cricleshape.py
from constants import WHITE, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH # Importing only the things I need from constants.py
import random 
import math

class Asteroid(CircleShape): # The parent asteroid class    
    containers = None 

    # Defining the radius and size of the asteroid
    def __init__(self, x, y, radius, size):
        # initialize parent class 
        CircleShape.__init__(self, x, y, radius)
        # How much health each size of asteroid has large has 65, medium has 45, small has 25.
        if size == "large": 
            self.max_health = self.health = 65
        elif size == "medium":
            self.max_health = self.health = 45
        else: # small since it is easier to do this than find the size of small.
            self.max_health = self.health = 25
        

        self.vertices_offsets = []
        num_vertices = random.randint(6, 10)
        # Making the asteroids lumpy and imperfect instead of perfect circles for more realistic asteroids. 
        for i in range(num_vertices):
            angle = 2 * math.pi * i / num_vertices           
            jitter = random.uniform(0.8, 1.2)
            offset_x = self.radius * jitter * math.cos(angle)
            offset_y = self.radius * jitter * math.sin(angle)
            self.vertices_offsets.append((offset_x, offset_y))
    # added splitting into the smaller and smaller asteroids large = 2 medium, medium = 2 small.
    def split(self):
        self.kill()

        # if the radius is too small, don't split
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # determine new size
        new_size = ""
        if self.max_health == 100:
            new_size = "medium"
        else:
            new_size = "small"
        # caluculates new raidus
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # generate rng
        random_angle = random.uniform(20, 50)

        # Create 2 new asteroids

        for angle_multiplier in [1, -1]:
            asteroid = Asteroid(self.position.x, self.position.y, new_radius, new_size)

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


        min_y = min(vertex[1] for vertex in vertices)

        bar_width = self.radius * 2
        bar_height = 5

        health_percentage = self.health / self.max_health

        bar_x = self.position.x - bar_width/2
        bar_y = min_y - 15

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_percentage, bar_height))

    def update(self, dt):
        self.position += self.velocity * dt

        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius


        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius