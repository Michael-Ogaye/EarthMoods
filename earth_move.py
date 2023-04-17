import os
import pygame
import sys
import time
import math
import random
from pygame.locals import *
from pygame.colordict import THECOLORS as Allcolors
from threading import Thread


pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 155, 0)
red = (155, 0, 0)
purple=Allcolors['purple']
blue=Allcolors['blue']
clock = pygame.time.Clock()
width = 1350
height = 800
screen = pygame.display.set_mode((width, height))
ico_image=pygame.image.load('resources/ico.svg')
pygame.display.set_caption('Earth_Marble')
pygame.display.set_icon(ico_image)
clock=pygame.time.Clock()




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
        self.earth_ice,self.rect_ice=load_image('p10.png',-1,-1)
        self.earth_water,self.rect_water=load_image('water1.png',-1,-1)
        self.earth_fire,self.rect_fire=load_image('earth_fire1.png',-1,-1)
        self.earth_gamma,self.rect_gamma=load_image('gamma.png',-1,-1)

    def draw(self,image):
        loaded_img,rect=load_image(image,-1,-1)
        self.rotated_earth = pygame.transform.rotate(loaded_img, self.angle)
        self.rotated_rect = self.rotated_earth.get_rect()
        self.rotated_rect.center = self.earth_rect.center
        screen.blit(self.rotated_earth, self.rotated_rect)

        self.angle+=0.1
        if self.angle>=360:
            self.angle=0
        

class Marble(pygame.sprite.Sprite):
    def __init__(self) -> None:
         pygame.sprite.Sprite.__init__(self)
         r,g,b=random.randint(0,255),random.randint(0,255),random.randint(0,255)
         self.density=random.randint(1,3)
         self.speed=random.randint(1,2)
         self.size=random.randint(3,6)
         self.color=(r,g,b)
         self.directionx=random.choice([1,-1])
         self.directiony=random.choice([-1,1])
         self.x=width/2+(random.randint(40,150)*self.directionx)
         self.y=height/2+(random.randint(40,150)*self.directiony)
         self.rect=pygame.Rect(self.x-self.size/2,self.y-self.size/2,self.size,self.size)
         self.center=(self.x,self.y)
    def update(self):
         self.x+=(self.speed*self.directionx)/self.density
         self.y+=(self.speed*self.directiony)/self.density

    def draw(self):
         pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)

         self.update()
    def destroy(self):
        self.kill()
        
class Text():

    def __init__(self,fontname='freesansbold.ttf',font_size=12) -> None:
           self.font_name=fontname
           self.font_size=font_size
           self.font=pygame.font.Font(self.font_name,self.font_size)

    def render_text(self,text,color,placement,sur_color,surf_size,surf_placement):
        surface=self.font.render(text,True,color)
        surf=pygame.Surface(surf_size,5)
        surf.fill(sur_color)
        surf_rect=surf.get_rect()
        surf_rect.topleft=surf_placement
        rect=surface.get_rect()
        rect.left=placement[0]
        rect.top=placement[1]
        surf.blit(surface,rect)
        screen.blit(surf,surf_rect)
        
  
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y,direction):
        pygame.sprite.Sprite.__init__(self)
         
        self.image =pygame.image.load('resources/rock1.png')
        self.sound=pygame.mixer.Sound('resources/bullet.wav')
        self.image=pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction=direction
        self.shot=False
        self.bullet_group=pygame.sprite.Group()
         
   
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def generate_bullets(self):
        bullets=[]
        self.shot=True
        for _ in range(20) :
            x,y=self.rect.center
            bullet=Bullet(x,y,self.direction,self.rect)
            bullets.append(bullet)
            self.bullet_group.add(bullet)
            
        return self.bullet_group
    @property
    def bullet_grouped(self):
        return self.bullet_group if self.shot else None
    def shoot(self):
        pygame.mixer.init()
        self.sound.set_volume(5.0)
        self.sound.play()
        bullets=self.generate_bullets()
        
        return bullets
           

    def check_walls(self):
        rocket_object=self.rect
        if rocket_object.left<0:
            rocket_object.left=0

        if rocket_object.right>width:
            rocket_object.right=width

    

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,rocket_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('resources/bullet1.png')
        self.rect=self.image.get_rect()
        self.rocket_rect=rocket_rect
        self.rect.center=(x,y)
        self.direction=direction
        self.x=x
        self.y=y
        self.movement=[6,7]
        if self.direction is not None:
            if self.direction[0]==-1 and self.direction[1]==-1:
                self.x=x-self.rocket_rect.width/2
                self.y=y+self.rocket_rect.height/2
                
                self.image = pygame.transform.rotate(self.image, 315)
                
                self.movement=[-15,15]
            if self.direction[0]==1 and self.direction[1]==-1:
                self.x=x+self.rocket_rect.width/2+40
                self.y=y+self.rocket_rect.height/2
                self.image = pygame.transform.rotate(self.image, 405)
                self.movement=[15,15]

            if self.direction[0]==1 and self.direction[1]==1:
                self.x=x+self.rocket_rect.width/2+40
                self.y=y-self.rocket_rect.height/2
                self.image = pygame.transform.rotate(self.image, 495)
                self.movement=[15,-15]

            if self.direction[0]==-1 and self.direction[1]==1:
                self.x=x-self.rocket_rect.width/2
                self.y=y-self.rocket_rect.height/2
                self.image = pygame.transform.rotate(self.image, 585)
                self.movement=[-15,-15]
        self.rect.center=(self.x,self.y)
        
    
    def update(self):
        (x, y) = self.rect.center
        self.x+=self.movement[0]
        self.y+=self.movement[1]
        
        self.rect.center = (self.x, self.y)

        
       
       
    def draw(self, surface):
        self.update()
        surface.blit(self.image, self.rect)
    
        

ov_score=0
def main():
    running=True
    game_over=False
   
    winning_game=False
    bg_music=pygame.mixer.Sound('resources/space.ogg')
    bg,bgrect = load_image('space.png',-1,-1)
    bg=pygame.transform.scale(bg,(width,height))
    
    earth_states={
        'ice':0,
        'fire':0,
        'water':0,
        'gamma':0

    }
   


    screen_text=Text(font_size=13)
    state_sprite='normal_earth.png'

    def get_overall_score():
        global winning_game,ov_score
        
        ov_score+=-(earth_states['fire'])+(earth_states['water'])+(earth_states['ice'])-(earth_states['gamma'])
        if ov_score<0:
            winning_game=False
        else:
            winning_game=True

        return ov_score
    
    def calculate_color(color,color1):
            is_color=False
            dr=math.sqrt((color[0]-color1[0])**2)
            dg=math.sqrt((color[1]-color1[1])**2)
            db=math.sqrt((color[2]-color1[2])**2)
            

            df=((dr)+(dg)+(db))/3.0
            
            if df<50:
                is_color=True
            return is_color

    def colorhit(color):
        color_hit=None
        if calculate_color(purple,color):
            color_hit='green'

        elif calculate_color(red,color):
            color_hit='red'
        elif calculate_color(blue,color):
            color_hit='blue'
        elif calculate_color(white,color):
            color_hit='white'

        return color_hit
    

    def update_states(color):
        color_hit=colorhit(color)
        if color_hit=='white':
            earth_states['ice']+=10
            get_overall_score()
        if color_hit=='red':
            earth_states['fire']+=10
            get_overall_score()
        if color_hit=='blue':
            earth_states['water']+=10
            get_overall_score()
        if color_hit=='purple':
            earth_states['gamma']+=10
            get_overall_score()

        
       

    def highest_state():
        highest_key=None
        highest_no=0
        for key in earth_states.keys():
            if earth_states[key]>highest_no:
                highest_no=earth_states[key]
        for k in earth_states.keys():
            if earth_states[k]==highest_no:
                highest_key=k
        
            
        return highest_key if highest_no>0 else None


    
    earth_norm=Earth()
    
    
    rockets = []
    rocket_spacing = 20
    direction=None
    bullet_group=pygame.sprite.Group()
    marble_group=pygame.sprite.Group()
    for i in range(4):
            raw_angle=(45+i*90)
            angle = math.radians(45 + i*90)
            x = int(width/2 + math.cos(angle) * (width/2 - rocket_spacing))
            y = int(height/2 - math.sin(angle) * (height/2 - rocket_spacing))
            if raw_angle==45:
             direction=[-1,-1]
            if raw_angle==135:
                direction=[1,-1]
            if raw_angle==225:
                direction=[1,1]
            if raw_angle==315:
                direction=[-1,1]
            rocket = Rocket(x, y,direction)
           
            rocket.image = pygame.transform.rotate(rocket.image, 315+i*90)
            rockets.append(rocket)
            

    def generate_marbles():
        all_stars=[]
        for _ in range(50):
            for _ in range(3):
                all_stars.append(Marble())
        pygame.display.flip()
        
        return all_stars
    
    # for marb in generate_marbles():
    #     marble_group.add(marb)
    
   

    def render_scores(text_array):
        for txt in text_array:
             txt[0].render_text(txt[1],txt[2],txt[3],txt[4],txt[5],txt[6])
             
    
    start_time=time.time()
    game_duration = 120  # 2 minutes in seconds
    while running:
        clock.tick(60)
        elapsed_time = time.time() - start_time
        remaining_time = game_duration - elapsed_time
        
        
        if int(remaining_time)<=0:
            running=False
            game_over=True
        
        if not running:
           break

        my_marbles=generate_marbles() 
        # score= get_overall_score()
        texts=[
            (screen_text,f'Overall Score:{ov_score} ',red,(2,5),white,(200,20),(width/2,20)),
            (screen_text,f'Fire score: {earth_states["fire"]}',green,(2,5),white,(200,20),(width/2,45)),
            (screen_text,f'Ice score: {earth_states["ice"]}',green,(2,5),white,(200,20),(width/2,65)),
            (screen_text,f'Gamma score: {earth_states["water"]}',green,(2,5),white,(200,20),(width/2,85)),
            (screen_text,f'Aqua score: {earth_states["gamma"]}',green,(2,5),white,(200,20),(width/2,110)),
            (screen_text,f'Time left:{int(remaining_time)} s ',white,(2,5),black,(200,25),(width-150,20)),

        ]

        highest_mood=highest_state()
        screen.blit(bg,bgrect)
        render_scores(texts)
        bg_music.play()
         
        if highest_mood is not None:
            if highest_mood=='fire':
                state_sprite='earth_fire.png'
            if highest_mood=='ice':
                state_sprite='p10.png'
            if highest_mood=='water':
                state_sprite='water1.png'
            if highest_mood=='gamma':
                state_sprite='p4.png'
        else:
          state_sprite='normal_earth.png'
                 
            
        earth_norm.draw(state_sprite)
        for marble in my_marbles:
            marble_group.add(marble)
            marble.update()
            marble.draw()
            
        for rocket in rockets:
            rocket.draw(screen)  

        if bullet_group is not None:
            bullet_group.update() 
            bullet_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
            # Shoot bullets when arrow keys are pressed
                    
                    if event.key == pygame.K_LEFT:
                        bg_music.stop()
                        rockets[0].shoot()
                        bullet_group=rockets[0].bullet_grouped

                       
                    if event.key == pygame.K_RIGHT:
                         bg_music.stop()
                         rockets[1].shoot()
                         bullet_group=rockets[1].bullet_grouped
                        
                    if event.key == pygame.K_UP:
                        bg_music.stop()
                        rockets[2].shoot()
                        bullet_group=rockets[2].bullet_grouped
                    if event.key == pygame.K_DOWN:
                        bg_music.stop()
                        rockets[3].shoot()
                        bullet_group=rockets[3].bullet_grouped
        
        for marblehit in pygame.sprite.groupcollide(marble_group,bullet_group,True,True):
            bg_music.stop()
            pygame.mixer.init()
            sound= pygame.mixer.Sound('resources/explosion.wav')
            sound.set_volume(5.0)
            sound.play()
            (x,y)=marblehit.center
            fire_image=pygame.image.load('resources/fire.png')
            fire_image=pygame.transform.rotate(fire_image,90)
            fire_image=pygame.transform.scale(fire_image,(50,50))
            fire_image_rect=fire_image.get_rect()
            fire_image_rect.center=(x,y)
            screen.blit(fire_image,fire_image_rect)
            update_states(marblehit.color)
                    
                
      
        pygame.display.flip()
        
        
    while game_over:
        screen.fill(black)
        over_text=Text(font_size=18)
        outcome='You had no impact' if ov_score<=0 else "Hurray you Won,"
        
            
        content=[(over_text,'Game Over !!',red,(50,2),black,(300,170),(width/2-100,height/2)),
                 (over_text,f'{outcome}',purple,(50,2),black,(300,170),(width/2-100,height/2+100)),
                 (over_text,'Press Enter to start Again or Q to exit',white,(50,2),black,(400,170),(width/2-200,height/2+150)),
                 ]
        render_scores(content)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type==KEYDOWN:
                if event.key==pygame.K_RETURN:
                    running=True
                    game_over=False
                    main()
                  
                if event.key==pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

    pygame.quit()


main()