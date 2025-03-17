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
    game_over_sound = pygame.mixer.Sound("assets/gameover.mp3")
    lose_life = pygame.mixer.Sound("assets/lifelost.wav")
    change_weapon = pygame.mixer.Sound("assets/changeweapon.wav")
    sound_track = pygame.mixer.music.load("assets/soundtrack.flac")
    asteroid_hit_sound = pygame.mixer.Sound("assets/asteroidhitnoise.wav")

    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Sound error: {e}")
    small_explosion = medium_explosion = large_explosion = game_over_sound = lose_life = change_weapon = None

   

def main(): # main function declaration    
    icon = pygame.image.load('assets/asteroidicon.png')
    pygame.init() # initializes pygame    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # makes a screen with the dimensions of SCREEN_WIDTH and SCREEN_HEIGHT
    clock = pygame.time.Clock() # creates a clock object
    dt = 0 # delta time
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Asteroid Game!") # sets the title of the window

    #background
    background = pygame.image.load("assets/asteroids.png").convert()  
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
    lives = 3



    speed_boost_level = 0
    while True: # main while loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()              
                
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
                                small_explosion.play()
                            score += 100 # Small
                            #print("Small asteroid destroyed +100 points")
                        elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                            if medium_explosion:
                                medium_explosion.play()
                            score += 50 # Medium
                            #print("Medium asteroid destroyed +50 points")
                        else:
                            if large_explosion:
                                large_explosion.play() 
                            score += 20 # Large
                            #print("Large asteroid destroyed +20 points")
                        asteroid.split()




    
        
        for sprite in drawable:
            sprite.draw(screen)

        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"S: {score}", True, (255, 255, 255))
        lives_text = score_font.render(f"L: {lives}", True, (255, 255, 255))
        weapon_type_font = pygame.font.Font(None, 36)                      
        weapon_type_text = weapon_type_font.render(f"{player.weapon_type}", True, (255, 255, 255))
        move_up_font = pygame.font.Font(None, 30)
        move_up_text = move_up_font.render("Up-W", True, (255, 255, 255))
        move_down_font = pygame.font.Font(None, 30)
        move_down_text = move_down_font.render("Down-S", True, (255, 255, 255))
        move_left_font = pygame.font.Font(None, 30)
        move_left_text = move_left_font.render("Left-A", True, (255, 255, 255))
        move_right_font = pygame.font.Font(None, 30)
        move_right_text = move_right_font.render("Right-D", True, (255, 255, 255))
        switch_weapon_font = pygame.font.Font(None, 30)
        switch_weapon_text = switch_weapon_font.render("Switch Weapon-LSHIFT", True, (255, 255, 255))  
        screen.blit(switch_weapon_text, (5, 85))                                         
        screen.blit(move_up_text, (5, 5))
        screen.blit(move_down_text, (5, 25))
        screen.blit(move_left_text, (5, 45))
        screen.blit(move_right_text, (5, 65))
        screen.blit(weapon_type_text, (5, 1050))
        screen.blit(score_text, (5, 990)) 
        screen.blit(lives_text, (5, 1020))
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Sets the fps to 60 and gets the delta time
        

if __name__ == "__main__":
    main()