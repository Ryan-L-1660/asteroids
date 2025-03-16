from circleshape import CircleShape, Shot
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_TURN_SPEED, PLAYER_RADIUS, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
class Player(CircleShape, pygame.sprite.Sprite):  # Multiple inheritance
    def __init__(self, x, y):
        self.weapon_type = "cannon"
        self.r_key_pressed = False
        self.shot_cooldown = 0
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

        # add invulnerability to player 
        self.invulnerable = False
        self.invulnerable_timer = 0

        

    def switch_weapon(self):
        if self.weapon_type == "cannon":
            self.weapon_type = "minigun"
            print("Switched to minigun fire")
        else:
            self.weapon_type = "cannon"
            print("Switched to cannon fire")
        
       

    def reset_position(self, x, y):
        """Reset the player's position to the specified coordinates."""
        self.position = pygame.Vector2(x, y)
        self.rect.center = (x, y)

    def set_invulnerable(self, seconds):
        """Make the player invulnerable for the specified number of seconds"""
        self.invulnerable = True
        self.invulnerable_timer = seconds

    
    def draw(self, screen):
        if self.invulnerable:
            if int(pygame.time.get_ticks() / 200) % 2 == 0:               
                pygame.draw.polygon(screen, "white", self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, "white", self.triangle(), 0)


        # Debug to see hitbox
        # pygame.draw.polygon(screen, "red", self.triangle(), 1)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def update(self, dt):

        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.invulnerable_timer = 0
        
        if self.shot_cooldown > 0:
            self.shot_cooldown -= dt
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
        
        if keys[pygame.K_r] and not self.r_key_pressed:
            self.switch_weapon()
        self.r_key_pressed = keys[pygame.K_r]
        
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

        self.rect.center = (self.position.x, self.position.y)

    def shoot(self):
        if self.shot_cooldown <= 0:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            nose_position = self.position + forward * self.radius
            
            # Create a new shot and make sure it's added to the containers
            shot = Shot(nose_position.x, nose_position.y)
            Shot.containers[0].add(shot)  # Add to shots_group
            Shot.containers[1].add(shot)  # Add to updateable
            Shot.containers[2].add(shot)  # Add to drawable
            Shot.containers[3].add(shot)  # Add to all_sprites
            
            # Set velocity
            shot.velocity = forward * PLAYER_SHOOT_SPEED

            # Set damage and cooldown based on weapon type
            if self.weapon_type == "cannon":
                shot.damage = 50
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            else:  # rapid
                shot.damage = 10
                self.shot_cooldown = PLAYER_SHOOT_COOLDOWN / 5
            
            return shot
        return None


    # 
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
            
        
