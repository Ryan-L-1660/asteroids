# imports the pygame module
import pygame
from constants import PLAYER_SHOOT_SPEED, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, PLAYER_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from asteroid import Asteroid 
from asteroidfield import AsteroidField    
from circleshape import Shot      
import pygame.mixer 
import os
from os import path
import json
# imports the player class from the player file

try:
    # initalizing pygame and pygame.mixer  
    pygame.mixer.pre_init(44100, 16, -2, 1024)
    pygame.mixer.init() 
    pygame.init()
    # Sound effect storage for decreased lag. 
    small_explosion = pygame.mixer.Sound("assets/Sounds/small.wav")
    medium_explosion = pygame.mixer.Sound("assets/Sounds/medium.wav")
    large_explosion = pygame.mixer.Sound("assets/Sounds/large.wav")
    game_over_sound = pygame.mixer.Sound("assets/Sounds/gameover.wav")
    lose_life = pygame.mixer.Sound("assets/Sounds/lifelost_converted.wav")
    change_weapon = pygame.mixer.Sound("assets/Sounds/changeweapon.wav")   
    asteroid_hit_sound = pygame.mixer.Sound("assets/Sounds/asteroidhitnoise.wav")
    

    # Soundtrack loading volume and making it play in a loop infinitly 
    pygame.mixer.music.load("assets/Sounds/soundtrack.ogg")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)

    # If sounds can't be found return an error in terminal
except Exception as e:
    print(f"Sound error: {e}")
    small_explosion = medium_explosion = large_explosion = game_over_sound = lose_life = change_weapon = sound_track = asteroid_hit_sound = None

# Menu that pops up when player hits esc 
def pause_menu(screen, player):
    """ Displays a pause menu with controls, resume & exit options. """
    paused_surface = screen.copy()  # Snapshot of the game
    blur_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    blur_surface.fill((0, 0, 0, 180))  # Dark overlay for blur effect

    # Fonts
    font = pygame.font.Font(None, 50)
    controls_font = pygame.font.Font(None, 30)

    # Buttons
    resume_text = font.render("Resume", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))

    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    # Control instructions
    controls_text = [
        "CONTROLS:",
        "Move: W A S D",
        "Shoot: Spacebar",
        "Switch Weapon: LShift",
        "Pause: ESC"
    ]
    control_surfaces = [controls_font.render(line, True, (255, 255, 255)) for line in controls_text]

    pygame.mixer.music.set_volume(0.05)  # Lower volume while paused

    selected_option = 0  # 0 = Resume, 1 = Exit

    paused = True
    while paused:
        screen.blit(paused_surface, (0, 0))  # Show frozen game state
        screen.blit(blur_surface, (0, 0))  # Darken screen

        # Highlight selected option
        resume_color = (255, 255, 0) if selected_option == 0 else (255, 255, 255)
        exit_color = (255, 255, 0) if selected_option == 1 else (255, 255, 255)

        resume_text = font.render("Resume", True, resume_color)
        exit_text = font.render("Exit", True, exit_color)

        # Draw buttons
        screen.blit(resume_text, resume_rect)
        screen.blit(exit_text, exit_rect)

        # Draw controls
        y_offset = SCREEN_HEIGHT // 2 - 150
        for surface in control_surfaces:
            screen.blit(surface, (SCREEN_WIDTH // 2 - 100, y_offset))
            y_offset += 40

        pygame.display.flip()

        # Handle pause menu input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    selected_option = (selected_option + 1) % 2  # Toggle between 0 and 1
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected_option = (selected_option - 1) % 2  # Toggle between 0 and 1

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if selected_option == 0:  # Resume
                        paused = False
                    elif selected_option == 1:  # Exit
                        pygame.quit()
                        quit()

                if event.key == pygame.K_ESCAPE:  # Resume on ESC
                    paused = False

    pygame.mixer.music.set_volume(0.15)  # Restore music volume when resuming



def main(): # <---- main function declaration   
    icon = pygame.image.load('assets/Images/asteroidicon.png')    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT
    clock = pygame.time.Clock() # creates a clock object
    dt = 0 # delta time
    pygame.display.set_icon(icon) # making an icon for the game so it doesn't look so plain
    pygame.display.set_caption("Asteroid Game! --Ryan") # sets the title of the window
    


    #background
    background = pygame.image.load("assets/Images/asteroids.png").convert()  # loading background image 
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) # the background resolution which is 1920x1080
   
    # Starting messages to terminal
    print("Starting Asteroids!")

 
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
    asteroid_field = AsteroidField()  # Create it only 

    # Variables for player Score and player lives.
    #high_score = 0
    score = 0
    lives = 3



    speed_boost_level = 0
    while True: # main while loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu(screen, player)
                    
                
                
                             
                
        # Draw background and update the game 
        screen.blit(background, (0, 0))
        updateable.update(dt)


              
        # Check for collisions
        for asteroid in asteroids:
            if player.check_for_collision(asteroid) and not player.invulnerable:
                lives -= 1
                if lose_life:
                    lose_life.play()
                if lives > 0:
                    # respawn player
                    player.reset_position(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.set_invulnerable(3) # make player no die 3 seconds
                    #print(f"Lives remaining: {lives}")
                else:
                    #print("Game Over!")
                    pygame.mixer.music.stop()
                    if game_over_sound:
                        game_over_sound.play()
                        pygame.time.wait(3000)

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
                    
                    
                        # add score number based on wat size astoroid is hit
                    if asteroid.health > 0 and asteroid_hit_sound:
                        asteroid_hit_sound.play()

                    if asteroid.health <= 0:
                        if asteroid.radius <= ASTEROID_MIN_RADIUS:
                            if small_explosion:
                                small_explosion.play(fade_ms=100)
                            score += 100 # Small
                            #print("Small asteroid destroyed +100 points")
                        elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                            if medium_explosion:
                                medium_explosion.play(fade_ms=100)
                            score += 50 # Medium
                            #print("Medium asteroid destroyed +50 points")
                        else:
                            if large_explosion:
                                large_explosion.play(fade_ms=100) 
                            score += 20 # Large
                            #print("Large asteroid destroyed +20 points")
                        asteroid.split()




    
        # Display font for score, weapon type, lives, and controls
        for sprite in drawable:
            sprite.draw(screen)
        
        
        score_font = pygame.font.Font(None, 36)
        lives_text = score_font.render(f"L: {lives}", True, (255, 255, 255))
        
        score_text = score_font.render(f"S: {score}", True, (255, 255, 255))
        
        
        # Controls
        controls_font = pygame.font.Font(None, 36) # Master Font                    
        weapon_type_text = controls_font.render(f"{player.weapon_type}", True, (255, 255, 255))
        
        #move_up_text = controls_font.render(f"UP-W", True, (255, 255, 255))
        #move_down_text = controls_font.render(f"DOWN-S", True, (255, 255, 255))  
        #move_left_text = controls_font.render(f"LEFT-A", True, (255, 255, 255))
        #move_right_text = controls_font.render(f"RIGHT-D", True, (255, 255, 255))     
        #switch_weapon_text = controls_font.render("Switch Weapon-LSHIFT", True, (255, 255, 255))
        #quit_text = controls_font.render(f"Quit-ESC", True, (255, 255, 255))
        # blit the text onto the dispaly
        #screen.blit(quit_text, (5, 105))  
        #screen.blit(switch_weapon_text, (5, 85))                                         
        #screen.blit(move_up_text, (5, 5))
        #screen.blit(move_down_text, (5, 25))
       # screen.blit(move_left_text, (5, 45))
        #screen.blit(move_right_text, (5, 65))
        screen.blit(weapon_type_text, (5, 1050))
        screen.blit(score_text, (5, 990)) 
        screen.blit(lives_text, (5, 1020))
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Sets the fps to 60 and gets the delta time
        
        

if __name__ == "__main__":
    main()