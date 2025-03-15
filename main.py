# imports the pygame module
import pygame
from constants import *

pygame.init() # initializes pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT



def main(): # main function declaration
    print("Starting Asteroids!")
    print("Screen width:",SCREEN_WIDTH)
    print("Screen height:",SCREEN_HEIGHT)




while True: # main game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill((0, 0, 0)) # fills black screen
    pygame.display.flip() # updates the screen !!need to change to 60 fps!! 



























if __name__ == "__main__":
    main()