import pygame

# Initialize Pygame
pygame.init()

# Set up the display window
screen_width = 1200
screen_height = 890
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the Earth image
earth_image = pygame.image.load("resources/normal_earth.png")

# Set up the initial position and rotation of the Earth
earth_rect = earth_image.get_rect()
earth_rect.center = (screen_width/2, screen_height/2)

rotation_angle = 0

# Set up the game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Rotate and draw the Earth
    rotated_earth = pygame.transform.rotate(earth_image, rotation_angle)
    rotated_rect = rotated_earth.get_rect()
    rotated_rect.center = earth_rect.center
    screen.blit(rotated_earth, rotated_rect)

    # Update the rotation angle
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Clean up
pygame.quit()
