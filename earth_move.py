import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *


pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 155, 0)
red = (155, 0, 0)
clock = pygame.time.Clock()
width = 1000
height = 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Earth_Marble')


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
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())



        
       
       

     
class Earth(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.angle=0
        self.earth_image,self.earth_rect=load_image('normal_earth.png',-1,-1)
        self.earth_rect.center = (width/2, height/2)

    def draw(self):
        self.rotated_earth = pygame.transform.rotate(self.earth_image, self.angle)
        self.rotated_rect = self.rotated_earth.get_rect()
        self.rotated_rect.center = self.earth_rect.center
        screen.blit(self.rotated_earth, self.rotated_rect)

        self.angle+=0.1
        if self.angle>=360:
            self.angle=0
        

class Star():
    def __init__(self) -> None:
         
         self.density=random.randint(1,3)
         self.speed=random.randint(1,2)
         self.size=random.randint(3,6)
         self.color=pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
         self.directionx=random.choice([1,-1])
         self.directiony=random.choice([-1,1])
         self.x=width/2+(random.randint(40,150)*self.directionx)
         self.y=height/2+(random.randint(40,150)*self.directiony)
    def update(self):
         self.x+=(self.speed*self.directionx)/self.density
         self.y+=(self.speed*self.directiony)/self.density

    def draw(self):
         pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)
         self.update()

  
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y,direction):
        pygame.sprite.Sprite.__init__(self)
         
        self.image =pygame.image.load('resources/rock1.png')
        self.sound=pygame.mixer.Sound('resources/bullet.wav')
        self.image=pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction=direction
         
   
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def generate_bullets(self):
        bullets=[]
        for _ in range(50) :
            x,y=self.rect.center
            bullet=Bullet(x,y,self.direction,self.rect)
            bullets.append(bullet)
        return bullets
    def shoot(self):
        bullets=self.generate_bullets()
        for bullet in bullets:
            self.sound.play()
            bullet.update()
            bullet.draw(screen)
           

    def check_walls(self):
        rocket_object=self.rect
        if rocket_object.left<0:
            rocket_object.left=0

        if rocket_object.right>width:
            rocket_object.right=width

    

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,rocket_rect):
        self.image=pygame.image.load('resources/bullet1.png')
        self.rect=self.image.get_rect()
        self.rocket_rect=rocket_rect
        self.rect.center=(x,y)
        self.direction=direction
        if self.direction==[-1,-1]:
          self.x=x-self.rocket_rect.width/2
          self.y=y+self.rocket_rect.height/2
          self.image = pygame.transform.rotate(self.image, 315)
          self.movement=[-2,2]
        if self.direction==[1,-1]:
          self.x=x+self.rocket_rect.width/2
          self.y=y+self.rocket_rect.height/2
          self.image = pygame.transform.rotate(self.image, 405)
          self.movement=[2,2]

        if self.direction==[1,1]:
          self.x=x+self.rocket_rect.width/2
          self.y=y-self.rocket_rect.height/2
          self.image = pygame.transform.rotate(self.image, 495)
          self.movement=[2,-2]

        if self.direction==[-1,1]:
          self.x=x-self.rocket_rect.width/2
          self.y=y-self.rocket_rect.height/2
          self.image = pygame.transform.rotate(self.image, 585)
          self.movement=[-2,-2]
        self.rect.center=(self.x,self.y)
        
    
    def update(self):
        pass
        # angle_rad = math.radians(self.angle)
        # self.x += math.cos(angle_rad) * 10
        # self.y += math.sin(angle_rad) * 10
    def draw(self, surface):

       
        surface.blit(self.image, self.rect)
        


def main():
    running=True
    bg_music=pygame.mixer.Sound('resources/space.ogg')
    bg,bgrect = load_image('bg1.png',-1,-1)
    earth_norm=Earth()
    
    
    rockets = []
    rocket_spacing = 20
    direction=None
    for i in range(4):
            
            angle = math.radians(45 + i*90)
            x = int(width/2 + math.cos(angle) * (width/2 - rocket_spacing))
            y = int(height/2 - math.sin(angle) * (height/2 - rocket_spacing))
            if angle==45:
             direction=[-1,-1]
            elif angle==135:
                direction=[1,-1]
            elif angle==225:
                direction=[1,1]
            elif angle==225:
                direction=[-1,1]
            rocket = Rocket(x, y,direction)
            rocket.image = pygame.transform.rotate(rocket.image, 315+i*90)
            rockets.append(rocket)
            

    def generate_stars():
        all_stars=[]
        for _ in range(50):
            for _ in range(3):
                all_stars.append(Star())
        
        return all_stars

    
    while running:
    
        screen.blit(bg,bgrect)
        bg_music.play()
        earth_norm.draw()
        for star in generate_stars():
            star.update()
            star.draw()
            
        for rocket in rockets:
            rocket.draw(screen)   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
            # Shoot bullets when arrow keys are pressed
                
                    if event.key == pygame.K_LEFT:
                        rockets[0].shoot()

                       
                    elif event.key == pygame.K_RIGHT:
                         rockets[1].shoot()
                        
                    elif event.key == pygame.K_UP:
                        rockets[2].shoot()
                    elif event.key == pygame.K_DOWN:
                        rockets[3].shoot()
                    
                
               

        pygame.display.flip()
    pygame.quit()


main()