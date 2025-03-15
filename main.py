# imports the pygame module
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT # imports the constants from the constants file
from player import Player



def main(): # main function declaration
    pygame.init() # initializes pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT
    clock = pygame.time.Clock() # creates a clock object
    dt = 0 # delta time
    pygame.display.set_caption("Asteroids!") # sets the title of the window
    pygame.display.set_icon(pygame.image.load("assets/2531022.png")) # sets the icon of the window

    print("Starting Asteroids!")
    print("Screen width:",SCREEN_WIDTH)  # prints the screen width and height and starting message
    print("Screen height:",SCREEN_HEIGHT)

 
    updateable = pygame.sprite.Group() # creates a group for the player
    drawable = pygame.sprite.Group() # creates a group for the player
    Player.containers = (updateable, drawable) # sets the containers for the player   
    
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Player is added to both groups here

    while True: # main game Loop
        for event in pygame.event.get(): # gets all the events that are happening and when user quits it wont throw an error
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        
        updateable.update(dt)
        screen.fill((0, 0, 0)) # fills black screen
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip() # updates the screen with the new changes
        dt = clock.tick(60) / 1000 # sets the fps to 60 and gets the delta time
        
        
       



























if __name__ == "__main__":
    main()