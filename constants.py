SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080 # Screen Resoulution this is 1080p You can change it to whatever you want it to be 

# PLAYER SETTINGS
PLAYER_TURN_SPEED = 300 # degrees per second
PLAYER_SPEED = 100  # pixels per second
PLAYER_SHOOT_SPEED = 650 # <--- Projectile movement speed 
PLAYER_SHOOT_COOLDOWN = 0.9 # <--- Cooldown on shooting
PLAYER_RADIUS = 20 # <--- how big the player radius is 
SHOT_RADIUS = 2.5 # <--- How big each projectile is 
RAPID_SHOOT_SPEED = 800 


#COLOUR SETTINGS
WHITE = (255, 255, 255) # <--- white colour for ship and asteroids

# ASTEROID SETTINGS
ASTEROID_MIN_RADIUS = 22 # <--- smallest size of asteroid possible
ASTEROID_KINDS = 3 # Small, Medium, Large
ASTEROID_SPAWN_RATE = 1  # spawn rate
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # radius size

