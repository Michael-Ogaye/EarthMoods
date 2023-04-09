import pygame
import math

# Define the window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Initialize Pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Load the rocket image
rocket_img = pygame.image.load("resources/rock1.png")

class Rocket:
    def __init__(self, x, y):
        # Set the initial position of the rocket
        self.x = x
        self.y = y

        # Set the angle at which the rocket is facing
        self.angle = 45

        # Rotate the rocket image to face the center
        self.image = pygame.transform.rotate(rocket_img, self.angle)

    def update(self):
        pass

    def draw(self, surface):
        # Draw the rocket on the surface at the current position
        surface.blit(self.image, (self.x, self.y))

# Create the four rockets at the corner edges of the screen
rockets = [
    Rocket(0, 0),
    Rocket(WINDOW_WIDTH - rocket_img.get_width(), 0),
    Rocket(0, WINDOW_HEIGHT - rocket_img.get_height()),
    Rocket(WINDOW_WIDTH - rocket_img.get_width(), WINDOW_HEIGHT - rocket_img.get_height())
]

# Run the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the rockets on the screen
    for rocket in rockets:
        rocket.draw(screen)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
