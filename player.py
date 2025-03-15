from circleshape import CircleShape, Shot
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_TURN_SPEED, PLAYER_RADIUS, PLAYER_SPEED, PLAYER_SHOOT_SPEED


class Player(CircleShape, pygame.sprite.Sprite):  # Multiple inheritance
    def __init__(self, x, y):
        # Initialize parent classes
        CircleShape.__init__(self, x, y, PLAYER_RADIUS)
        pygame.sprite.Sprite.__init__(self)

        # Rotation angle and position
        self.rotation = 0
        self.position = pygame.Vector2(x, y)

        # Create a transparent image for the sprite
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        

        # Create a rect for positioning and set its center
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

        if keys[pygame.K_SPACE]:
            self.shoot()


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_cooldown <= 0:
            # Create a new shot at the player's position
            shot = Shot(self.position.x, self.position.y)
            
            # Set the shot's velocity based on the player's direction
            direction = pygame.Vector2(0, -1)
            direction = direction.rotate(-self.rotation)  # Assuming rotation is in degrees
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self.shot_cooldown = 0.25
            return shot
        return None
        


    
    
    
    
    
    
    
    
    
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
            
        
