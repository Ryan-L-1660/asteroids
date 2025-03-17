# imports the pygame module
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SHOOT_SPEED, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, PLAYER_SPEED 
from player import Player
from asteroid import Asteroid 
from asteroidfield import AsteroidField    
from circleshape import Shot      
import pygame.mixer                     
# imports the player class from the player file
try:
    pygame.mixer.init()
    small_explosion = pygame.mixer.Sound("assets/small.mp3")
    medium_explosion = pygame.mixer.Sound("assets/medium.mp3")
    large_explosion = pygame.mixer.Sound("assets/large.mp3")
except Exception as e:
    print(f"Sound error: {e}")
    small_explosion = medium_explosion = large_explosion = None

   

def main(): # main function declaration
    
    pygame.init() # initializes pygame
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT
    clock = pygame.time.Clock() # creates a clock object
    dt = 0 # delta time
    pygame.display.set_caption("Asteroids!") # sets the title of the window

    #background
    background = pygame.image.load("assets/background.png").convert()  
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
   
    # starting message
    print("Starting Asteroids!")
    print("Screen width:",SCREEN_WIDTH)  # prints the screen width and height and starting message
    print("Screen height:",SCREEN_HEIGHT)
 
    # Initialize groups first
    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots_group = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # Set containers
    Player.containers = (updateable, drawable)
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable,)
    Shot.containers = (shots_group, updateable, drawable, all_sprites)

    # Then create instances
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()  # Create it only once

    # score and lives
    score = 0
    lives = 10



    speed_boost_level = 0
    while True: # main while loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()              
                
        # Draw background and update the game 
        screen.blit(background, (0, 0))
        updateable.update(dt)

        current_speed_level = score // 500

        if current_speed_level > speed_boost_level:
            global PLAYER_SPEED
            player.speed += 50
            speed_boost_level = current_speed_level
            print(f"Speed boost! New speed: {player.speed}")
              
        # Check for collisions
        for asteroid in asteroids:
            if player.check_for_collision(asteroid) and not player.invulnerable:
                lives -= 1
                if lives > 0:
                    # respawn player
                    player.reset_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.set_invulnerable(3) # make player no die 3 seconds
                    print(f"Lives remaining: {lives}")
                else:
                    print("Game Over!")
                    game_over_font = pygame.font.Font(None, 72)
                    game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
                    game_over_score_font = pygame.font.Font(None, 72)
                    game_over_score_text = game_over_score_font.render(f"Score: {score}", True, (255, 255, 255))
                    screen.blit(game_over_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
                    pygame.display.flip()
                    pygame.time.wait(5000)
                    pygame.quit()
                    quit()

        # Check for collisions between shots and asteroids
        for shot in shots_group:
            for asteroid in asteroids:
                if shot.check_for_collision(asteroid):
                    asteroid.health -= shot.damage
                    shot.kill()                                            
                    
                    if asteroid.health <= 0:
                        # add score number based on wat size astoroid is hit
                        if asteroid.radius <= ASTEROID_MIN_RADIUS:
                            if small_explosion:
                                small_explosion.play()
                            score += 100 # Small
                            print("Small asteroid destroyed +100 points")
                        elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                            if medium_explosion:
                                medium_explosion.play()
                            score += 50 # Medium
                            print("Medium asteroid destroyed +50 points")
                        else:
                            if large_explosion:
                                large_explosion.play() 
                            score += 20 # Large
                            print("Large asteroid destroyed +20 points")
                        asteroid.split()




    
        
        for sprite in drawable:
            sprite.draw(screen)

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = score_font.render(f"Lives: {lives}", True, (255, 255, 255))
        speed_font = pygame.font.Font(None, 36)
        speed_text = speed_font.render(f"Speed: {PLAYER_SPEED:.1f}", True, (255, 255, 255))
        weapon_type_font = pygame.font.Font(None, 36)                      
        weapon_type_text = weapon_type_font.render(f"Weapon Type: {player.weapon_type}", True, (255, 255, 255)) 
        screen.blit(weapon_type_text, (595, 70))
        screen.blit(score_text, (595, 10)) 
        screen.blit(lives_text, (595, 40))
        screen.blit(speed_text, (600, 600))
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Sets the fps to 60 and gets the delta time
        

if __name__ == "__main__":
    main()