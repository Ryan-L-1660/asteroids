
import pygame
from constants import PLAYER_SHOOT_SPEED, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS, PLAYER_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from asteroid import Asteroid 
from asteroidfield import AsteroidField    
from circleshape import Shot      
import pygame.mixer 





  



try: 
    pygame.mixer.pre_init(44100, 16, -2, 1024)
    pygame.mixer.init() 
    pygame.init()
    # Sound effect storage  
    small_explosion = pygame.mixer.Sound("assets/Sounds/small.wav")
    medium_explosion = pygame.mixer.Sound("assets/Sounds/medium.wav")
    large_explosion = pygame.mixer.Sound("assets/Sounds/large.wav")
    game_over_sound = pygame.mixer.Sound("assets/Sounds/gameover.wav")
    lose_life = pygame.mixer.Sound("assets/Sounds/lifelost_converted.wav")
    change_weapon = pygame.mixer.Sound("assets/Sounds/changeweapon.wav")   
    asteroid_hit_sound = pygame.mixer.Sound("assets/Sounds/asteroidhitnoise.wav")
    

    pygame.mixer.music.load("assets/Sounds/soundtrack.ogg")
    pygame.mixer.music.set_volume(0.17)
    pygame.mixer.music.play(-1)

    # If sounds can't be found return an error in terminal
except Exception as e:
    print(f"Sound file cannot be found in the directory.{e}")
    small_explosion = medium_explosion = large_explosion = game_over_sound = lose_life = change_weapon = sound_track = asteroid_hit_sound = None




def main():   
    icon = pygame.image.load('assets/Images/asteroidicon.png')    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock() 
    dt = 0 
    pygame.display.set_icon(icon) 
    pygame.display.set_caption("Asteroid Game! --Ryan")
    
    #background
    background = pygame.image.load("assets/Images/asteroids.png").convert()  # loading background image 
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)) # the background resolution which is 1920x1080
   
 
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


    while True: # main while loop 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.time.wait(350)
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
                        pygame.mixer.music.stop()
                        pygame.mixer.pause()
                        game_over_sound.play()
                     
                    

                    pygame.mixer.music.stop()
                    game_over_font = pygame.font.Font(None, 72)
                    game_over_text = game_over_font.render("Game Over!", True, red)
                    message = game_over_font.render("Thanks for playing! - Ryan", True, white)
                    game_over_score_font = pygame.font.Font(None, 72)
                    game_over_score_text = game_over_score_font.render(f"Score: {score}", True, white)
                    screen.blit(message, (450, 10))
                    screen.blit(game_over_score_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
                    pygame.display.flip()
                    pygame.time.wait(3000)
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




    
        # Display font for score, weapon type, lives, and controls
        for sprite in drawable:
            sprite.draw(screen)
        
        
        
        white = (255, 255, 255)
        red = (255, 0, 0)
        
        master_font = pygame.font.Font(None, 22) # Master Font   
        # Control text displayment
               
        
        move_up_text = master_font.render(f"UP-W", True, white)
        move_down_text = master_font.render(f"DOWN-S", True, white)  
        move_left_text = master_font.render(f"LEFT-A", True, white)
        move_right_text = master_font.render(f"RIGHT-D", True, white)     
        switch_weapon_text = master_font.render("Switch Weapon-LSHIFT", True, white)
        quit_text = master_font.render(f"Quit-ESC", True, white)
        screen.blit(move_up_text, (5, 5))
        screen.blit(move_down_text, (5, 25))
        screen.blit(move_left_text, (5, 45))
        screen.blit(move_right_text, (5, 65))
        screen.blit(switch_weapon_text, (5, 85))
        screen.blit(quit_text, (5, 105))
        
        
        # lives and score text
        lives_score_font = pygame.font.Font(None, 40) 
        score_text = lives_score_font.render(f"{score}", True, white)   
        weapon_type_text = lives_score_font.render(f"{player.weapon_type}", True, white)
        screen.blit(weapon_type_text, (5, 1050))
        screen.blit(score_text, (960, 5)) 
        
        
        if lives <= 2:
            lives_text = lives_score_font.render(f"L: {lives}", True, red)  
        else:
             lives_text = lives_score_font.render(f"L: {lives}", True, white)   
        screen.blit(lives_text, (5, 1020))  

        
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Sets the fps to 60 and gets the delta time
        
        

if __name__ == "__main__":
    main()