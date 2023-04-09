import pygame
import os
import math

# Define some colors
BLACK = (0, 0, 0)

class Rocket(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, center):
        dx, dy = center[0] - self.rect.centerx, center[1] - self.rect.centery
        self.angle = 45 - math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

def main():
    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (700, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Rocket")

    # Load the rocket image
    rocket_img = pygame.image.load(os.path.join('resources', 'rock1.png')).convert_alpha()
    
    # Create four rocket instances
    rocket1 = Rocket(rocket_img, 0, 0)
    rocket2 = Rocket(rocket_img, size[0], 0)
    rocket3 = Rocket(rocket_img, 0, size[1])
    rocket4 = Rocket(rocket_img, size[0], size[1])

    # Create a sprite group
    all_sprites = pygame.sprite.Group()
    all_sprites.add(rocket1, rocket2, rocket3, rocket4)

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while True:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # --- Game logic should go here
        center = (size[0]//2, size[1]//2)
        all_sprites.update(center)

        # --- Drawing code should go here
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # --- Go ahead and update the screen
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()

if __name__ == "__main__":
    main()
