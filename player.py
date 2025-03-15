from circleshape import CircleShape
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_TURN_SPEED, PLAYER_RADIUS, PLAYER_SPEED

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self)
       
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        

        pygame.draw.polygon(self.image, (255, 255, 255), self.triangle(), 2)
        

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    
    
    
    
    
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)


        if keys[pygame.K_d]:
            self.rotate(+dt)

        if keys[pygame.K_w]:
            self.move(dt)
 
        
        if keys[pygame.K_s]:
            self.move(-dt)


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

        print(self.position)

        
        self.updatables = pygame.sprite.Group()
        self.drawables = pygame.sprite.Group()

        self.updatables.add(self)
        self.drawables.add(self)

    
    
    
    
    
    
    
    
    
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
            
        
