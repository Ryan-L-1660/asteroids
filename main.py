# imports the pygame module
import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT) # imports the constants from the constants file
from player import Player



def main(): # main function declaration
    pygame.init() # initializes pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT
    clock = pygame.time.Clock() # creates a clock object
    dt = 0 # delta time

    print("Starting Asteroids!")
    print("Screen width:",SCREEN_WIDTH)  # prints the screen width and height and starting message
    print("Screen height:",SCREEN_HEIGHT)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # creates a player object


    while True: # main game Loop
        for event in pygame.event.get(): # gets all the events that are happening and when user quits it wont throw an error
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((0, 0, 0)) # fills black screen
        player.draw(screen) # draws the player
        pygame.display.flip() # updates the screen with the new changes
        dt = clock.tick(60) / 1000 # sets the fps to 60 and gets the delta time
        player.update(dt) # updates the player
       



























if __name__ == "__main__":
    main()