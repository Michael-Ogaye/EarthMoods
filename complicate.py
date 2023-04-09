import pygame
import math

pygame.init()

# Set up the display
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Rocket game")

# Set up the rocket
ROCKET_WIDTH = 60
ROCKET_HEIGHT = 100
rocket_image = pygame.Surface((ROCKET_WIDTH, ROCKET_HEIGHT), pygame.SRCALPHA)
pygame.draw.polygon(rocket_image, pygame.Color('blue'), [(0,ROCKET_HEIGHT), (ROCKET_WIDTH/2,0), (ROCKET_WIDTH,ROCKET_HEIGHT)])
rocket_rect = rocket_image.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

# Set up the bullet
BULLET_RADIUS = 10
bullet_image = pygame.Surface((BULLET_RADIUS*2, BULLET_RADIUS*2), pygame.SRCALPHA)
pygame.draw.circle(bullet_image, pygame.Color('red'), (BULLET_RADIUS, BULLET_RADIUS), BULLET_RADIUS)
bullet_rect = bullet_image.get_rect(center=(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))

# Set up the clock
clock = pygame.time.Clock()

# Set up the initial values for the rocket and bullet
rocket_angle = 0
bullet_speed = 10

# Function to handle key presses
def handle_key_events():
    global rocket_angle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket_angle += 5
    if keys[pygame.K_RIGHT]:
        rocket_angle -= 5

# Function to move bullet towards the center from the rocket's outermost points
def move_bullet():
    bullet_radius=5
    global bullet_rect, bullet_speed, rocket_rect, rocket_angle
    angle_radians = math.radians(rocket_angle)
    outermost_point = rocket_rect.inflate(-ROCKET_WIDTH/4, -ROCKET_HEIGHT/4).move(-bullet_radius, 0).center
    dx = (WINDOW_SIZE[0]/2 - outermost_point[0])
    dy = (WINDOW_SIZE[1]/2 - outermost_point[1])
    distance_to_center = math.sqrt(dx**2 + dy**2)
    bullet_speed_x = bullet_speed * dx / distance_to_center
    bullet_speed_y = bullet_speed * dy / distance_to_center
    bullet_rect.move_ip(bullet_speed_x, bullet_speed_y)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle key presses
    handle_key_events()

    # Move the bullet
    move_bullet()

    # Draw everything
    screen.fill(pygame.Color('black'))
    rotated_rocket = pygame.transform.rotate(rocket_image, rocket_angle)
    rocket_rect = rotated_rocket.get_rect(center=rocket_rect.center)
    screen.blit(rotated_rocket, rocket_rect)
    screen.blit(bullet_image, bullet_rect)
    pygame.display.flip()

    # Tick the clock
    clock.tick(60)

# Quit the game
pygame.quit()
