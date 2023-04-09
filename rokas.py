import pygame
import math

pygame.init()

# set up the display window
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Class Example")

class Rocket:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 100))
        self.image.fill((255, 255, 255))
        pygame.draw.polygon(self.image, (255, 0, 0), [(0, 100), (25, 0), (50, 100)])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

rockets = []

# create rockets at all corner edges facing center
rockets.append(Rocket(0, 0))
rockets.append(Rocket(WIDTH, 0))
rockets.append(Rocket(WIDTH, HEIGHT))
rockets.append(Rocket(0, HEIGHT))

for rocket in rockets:
    angle = math.degrees(math.atan2(rocket.rect.centery - HEIGHT/2, rocket.rect.centerx - WIDTH/2))
    rocket.rotate(-angle - 45)
    rocket.draw(screen)

# run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
