import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the Earth images
earth_land_image = pygame.image.load("earth_land.png")
earth_ice_image = pygame.image.load("earth_ice.png")
earth_water_image = pygame.image.load("earth_water.png")

# Load the explosion sound and bullet sound
explosion_sound = pygame.mixer.Sound("explosion.wav")
bullet_sound = pygame.mixer.Sound("bullet.wav")

# Set up the initial position and rotation of the Earth
earth_rect = earth_land_image.get_rect()
earth_rect.center = (screen_width/2, screen_height/2)
rotation_angle = 0

# Set up the rocket and bullet
rocket_image = pygame.image.load("rocket.png")
rocket_rect = rocket_image.get_rect()
rocket_rect.centerx = screen_width/2
rocket_rect.bottom = screen_height - 10
bullet_image = pygame.image.load("bullet.png")
bullet_rect = bullet_image.get_rect()
bullet_rect.center = rocket_rect.center
bullet_speed = 10
bullet_state = "ready"

# Set up game variables
score = 0
game_font = pygame.font.Font(None, 36)

# Set up the game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_state = "fire"
                bullet_rect.center = rocket_rect.center
                bullet_sound.play()

    # Move the rocket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rocket_rect.left > 0:
        rocket_rect.move_ip(-5, 0)
    elif keys[pygame.K_RIGHT] and rocket_rect.right < screen_width:
        rocket_rect.move_ip(5, 0)

    # Move the bullet
    if bullet_state == "fire":
        bullet_rect.move_ip(0, -bullet_speed)
        if bullet_rect.bottom < 0:
            bullet_state = "ready"

    # Check for collisions between bullet and Earth
    if bullet_state == "fire" and bullet_rect.colliderect(earth_rect):
        bullet_state = "ready"
        explosion_sound.play()
        score += 1
        # Randomly change the Earth image and play the corresponding sound
        rand = random.randint(1, 3)
        if rand == 1:
            earth_rect = earth_land_image.get_rect()
            earth_rect.center = (screen_width/2, screen_height/2)
            pygame.mixer.Sound("land.wav").play()
        elif rand == 2:
            earth_rect = earth_ice_image.get_rect()
            earth_rect.center = (screen_width/2, screen_height/2)
            pygame.mixer.Sound("ice.wav").play()
        else:
            earth_rect = earth_water_image.get_rect()
            earth_rect.center = (screen_width/2, screen_height/2)
            pygame.mixer.Sound("water.wav").play()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Rotate and draw the Earth
    rotated_earth = pygame.transform.rotate(earth_land_image, rotation_angle)
    rotated_rect = rotated_earth.get_rect()
    rotated_rect.center = earth_rect.center
    screen.blit(rotated_earth, rotated_rect)

    # Draw the rocket
    screen.blit(rocket_image)