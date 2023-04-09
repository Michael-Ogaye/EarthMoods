import pygame
import math

pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Four Rockets")

# Load the rocket image
rocket_img = pygame.image.load("resources/rock1.png")

# Define the Rocket class
class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = rocket_img
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = -45

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)

# Create four rockets
rockets = [
    Rocket(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4),
    Rocket(SCREEN_WIDTH // 4 * 3, SCREEN_HEIGHT // 4),
    Rocket(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 * 3),
    Rocket(SCREEN_WIDTH // 4 * 3, SCREEN_HEIGHT // 4 * 3),
]

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black color
    screen.fill((0, 0, 0))

    # Draw the four rockets
    for rocket in rockets:
        rocket.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
