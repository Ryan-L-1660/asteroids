from circleshape import CircleShape
import pygame
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, 20)
        self.velocity = pygame.Vector2(0, 0)
        
