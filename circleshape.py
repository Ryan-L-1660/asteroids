# imports
import pygame
from constants import SHOT_RADIUS, PLAYER_SHOOT_SPEED

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def check_for_collision(self, other):
        return self.position.distance_to(other.position) < self.radius + other.radius
    
class Shot(CircleShape):
    containers = None
    
    def __init__(self, x, y):
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)  # This will be set by Player's shoot method
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius)
    
    def update(self, dt):
        self.position += self.velocity * dt