import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *


pygame.init()

size = (width, height) = (1024, 768)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 155, 0)
red = (155, 0, 0)
clock = pygame.time.Clock()
FPS = 30
maxspeed = 15


#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(FULLSCREEN)

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('resources', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())


def drawearth():
     angle=0
     earth_image,earth_rect=load_image('noermal_earth.png',-1,-1)
     earth_rect.center = (width/2, height/2)
     # Rotate and draw the Earth
     rotated_earth = pygame.transform.rotate(earth_image, angle)
     rotated_rect = rotated_earth.get_rect()
     rotated_rect.center = earth_rect.center
     screen.blit(rotated_earth, rotated_rect)

     angle+=1
     if angle>=360:
         angle=0
         

class Star():
    def __init__(self) -> None:
         
         self.density=random.randint(1,3)
         self.speed=random.randint(1,2)
         self.size=random.randint(3,6)
         self.color=pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
         self.directionx=random.choice([1,-1])
         self.directiony=random.choice([-1,1])
         self.x=width/2+(random.randint(40,150)*self.directionx)
         self.y=height/2+(random.randint(40,150)*self.directionyself)
    def update(self):
         self.x+=(self.speed*self.directionx)
         self.y+=(self.speed*self.directiony)

    def draw(self):
         pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)
         self.update()