import pygame
import math

# Initialize pygame
pygame.init()

# Set the width and height of the screen
width = 600
height = 600
screen = pygame.display.set_mode((width, height))

# Set the title of the window
pygame.display.set_caption("Rockets facing center")

# Define colors
white = (255, 255, 255)

# Load the rocket image and scale it
rocket_img = pygame.image.load("resources/rock1.png")
rocket_img = pygame.transform.scale(rocket_img, (50, 100))

# Define the Rocket class
class Rocket:
    def __init__(self, x, y):
        self.image = rocket_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Create four Rocket instances
rockets = []
rocket_spacing = 0
for i in range(4):
    angle = math.radians(45 + i*90)
    x = int(width/2 + math.cos(angle) * (width/2 - rocket_spacing))
    y = int(height/2 - math.sin(angle) * (height/2 - rocket_spacing))
    rocket = Rocket(x, y)
    rocket.image = pygame.transform.rotate(rocket.image, 315+i*90)
    rockets.append(rocket)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white color
    

    # Draw the rockets
    for rocket in rockets:
        rocket.draw(screen)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
