# imports the pygame module
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SHOOT_SPEED, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS # imports the constants from the constants file
from player import Player
from asteroid import Asteroid 
from asteroidfield import AsteroidField    
from circleshape import Shot                              
# imports the player class from the player file



def main(): # main function declaration
    pygame.init() # initializes pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT
    clock = pygame.time.Clock() # creates a clock object
    dt = 0 # delta time
    pygame.display.set_caption("Asteroids!") # sets the title of the window

    #background
    background = pygame.image.load("background.png").convert()  
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

    # score
    score = 0

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Handle continuous shooting with the spacebar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            shot = player.shoot()
            # Shot is automatically added to shots_group through containers
        
        
        screen.blit(background, (0, 0)) # draw background
        
        updateable.update(dt)
        
        # Check for collisions
        for asteroid in asteroids:
            if player.check_for_collision(asteroid):
                print("Game Over!")
                game_over_font = pygame.font.Font(None, 72)
                game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
                pygame.display.flip()
                pygame.time.wait(5000)
                pygame.quit()
                quit()

        # Check for collisions between shots and asteroids
        for shot in shots_group:
            for asteroid in asteroids:
                if shot.check_for_collision(asteroid):
                    asteroid.split()
                    shot.kill()
                    # add score number based on wat size astoroid is hit
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 100 # Small
                        print("Small asteroid destroyed +100 points")
                    elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                        score += 50 # Medium
                        print("Medium asteroid destroyed +50 points")
                    else: 
                        score += 20 # Large
                        print("Large asteroid destroyed +20 points")


        

        
        
        for sprite in drawable:
            sprite.draw(screen)

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10)) 
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Sets the fps to 60 and gets the delta time
        
        
       



























if __name__ == "__main__":
    main()