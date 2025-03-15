# imports the pygame module
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT # imports the constants from the constants file
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


    print("Starting Asteroids!")
    print("Screen width:",SCREEN_WIDTH)  # prints the screen width and height and starting message
    print("Screen height:",SCREEN_HEIGHT)

    Shot.containers = (shots_group, updateable, drawable, all_sprites)  # Add shots to updateable and drawable too
    
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

    
    while True: # main game Loop
        for event in pygame.event.get(): # gets all the events that are happening and when user quits it wont throw an error
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        updateable.update(dt)

        # dectect asteroids
        for asteroid in asteroids:
            if player.check_for_collision(asteroid):
                print("Game Over!")
                pygame.quit()
                quit()
        screen.fill((0, 0, 0)) # fills black screen
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip() # updates the screen with the new changes
        dt = clock.tick(60) / 1000 # sets the fps to 60 and gets the delta time
        
        
       



























if __name__ == "__main__":
    main()