import pygame
import os
import sys
import time
from pygame.locals import*
import math

pygame.init()

WIDTH = 750
HEIGHT = 750
SIZE = WIDTH, HEIGHT 

BACKGROUND = pygame.transform.scale(pygame.image.load('assets/background-black.png'), (SIZE))

MAIN_SHIP = pygame.image.load('assets/ships/main_ship.png')
BLUE_SHIP = pygame.image.load('assets/ships/vert_sombre.png')
RED_SHIP = pygame.image.load('assets/ships/red_ship.png')
DRONE_ARC = pygame.image.load('assets/ships/drone_vert.png')

MAIN_LASER = pygame.image.load('assets/laser/standart_purple_laser.png')
ARC_LASER = pygame.image.load('assets/laser/quarter_circle_purple.png')


idle_color_button = (170,170,170)
hover_color_button = (100,100,100)

#Rendering Text
title_font = pygame.font.SysFont("comicsans", 70)
small_font = pygame.font.SysFont("comicsans", 25)
game_name = title_font.render("Space invader", 1, (255,255,255))
author = small_font.render("(version Maximus)", 1, (255,255,255))

class Button():
    def __init__(self, x, y, width, height,font, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.text = text
        self.color = color
        
        
    def draw(self, screen):
        pygame.draw.rect(screen,self.color, (self.x, self.y, self.width, self.height),0)
        text = self.font.render(self.text, 1, (255,255,255))
        screen.blit(text,(self.x +(self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def click(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

button_lvl = Button(60,300,50,50,small_font,"lvl 1",idle_color_button)
button_lvl_2 = Button(120,300,50,50,small_font,"lvl 2",idle_color_button)
button_lvl_3 = Button(180,300,50,50,small_font,"lvl 3",idle_color_button)
button_lvl_4 = Button(240,300,50,50,small_font,"lvl 4",idle_color_button)
button_lvl_5 = Button(300,300,50,50,small_font,"lvl 5",idle_color_button)
button_lvl_6 = Button(360,300,50,50,small_font,"lvl 6",idle_color_button)
button_lvl_7 = Button(420,300,50,50,small_font,"lvl 7",idle_color_button)
button_lvl_8 = Button(480,300,50,50,small_font,"lvl 8",idle_color_button)
button_lvl_9 = Button(540,300,50,50,small_font,"lvl 9",idle_color_button)
button_lvl0 = Button(640,300,50,50,small_font,"lvl 10",idle_color_button)

button_quit = Button(280,600,150,50,small_font,"Quittez",idle_color_button)
button_resume = Button(280,375,200,50,small_font,"Reprendre",idle_color_button)
button_main_menu = Button(280,430,200,50,small_font,"Retour au menu",idle_color_button)
button_restart_lvl = Button(280,320,200,50,small_font,"Recommencer le niveau",idle_color_button)


CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

FPS = 120
RUNNING, PAUSE = 0,1
state = RUNNING

def scrolling(scroll_speed):

    global y
    rel_y = y % BACKGROUND.get_rect().height
    screen.blit(BACKGROUND, (0,rel_y - BACKGROUND.get_rect().height))
    if rel_y < HEIGHT:
        screen.blit(BACKGROUND, (0, rel_y))
    y += scroll_speed

def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, ((int(offset_x)), ((int(offset_y)))))

def in_game(lvl_choice):

    run = True
    global player
    player = MainShip(750/2-31,600)
    state = RUNNING
    scroll_speed = 1.25
    global enemies
    enemies = []
    starting = 0
    
    
    if lvl_choice == 1:
        lvl = Level_1(enemies)
        lvl.spawn_wave_1()

    if lvl_choice == 2:
        lvl = Level_2()

    while run:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
                state = PAUSE

        if state == RUNNING:      
            scrolling(scroll_speed)
            if keys[pygame.K_z] and player.y > 0: #haut
                player.y -=5
            if keys[pygame.K_s] and player.y < 750 - 62: #bas
                player.y +=5
            if keys[pygame.K_q] and player.x > 0:#gauche
                player.x -=5
            if keys[pygame.K_d] and player.x < 750 - 36: #droite
                player.x +=5
            if keys[pygame.K_SPACE]:
                player.shoot()

            for enemy in enemies[:]:
                angle =90-math.degrees(math.atan2((player.y+player.get_height()/2 - (enemy.y+enemy.get_height()/2)),(player.x+player.get_width()/2- (enemy.x+enemy.get_width()/2))))
                enemy.rotate_ship(angle)
                enemy.draw()
                enemy.shoot(angle)
                enemy.move_lasers(player)

                if collide(enemy,player):
                    enemies.remove(enemy)
            

            player.draw()
            player.move_laser(enemies)

            lvl.animate()

            if len(enemies) <= 0:
                lvl.progression += 1
                if lvl.progression == 1:
                    lvl.spawn_wave_2()
                else:
                    run = False

            if player.health <=0:
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                button_resume.draw(screen)
                
        
        if state == PAUSE:

            button_resume.draw(screen)
            button_main_menu.draw(screen)
            button_restart_lvl.draw(screen)

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_resume.click(pos):
                    state = RUNNING
                if button_main_menu.click(pos):
                    run = False
                    enemies = []
                if button_restart_lvl.click(pos):
                    enemies =[]
                    player.x = 310
                    player.y = 600
                    if lvl_choice == 1:
                        lvl.progression = 0
                        lvl.spawn_wave_1()
                        state = RUNNING
        
        pygame.display.update()
        CLOCK.tick(FPS)

def main_menu():
    global y
    y = 0
    lvl_choice = 0
    player = MainShip(310,600)
    speed = 5
    enemies = []
    scroll_speed = 0.25

    while True:
        scrolling(scroll_speed)
        screen.blit(game_name, (WIDTH/2 - game_name.get_width()/2, 50))
        screen.blit(author, (WIDTH/2 - author.get_width()/2,100))
        button_lvl.draw(screen)
        button_lvl_2.draw(screen)
        button_lvl_3.draw(screen)
        button_lvl_4.draw(screen)
        button_lvl_5.draw(screen)
        button_lvl_6.draw(screen)
        button_lvl_7.draw(screen)
        button_lvl_8.draw(screen)
        button_lvl_9.draw(screen)
        button_lvl0.draw(screen)

        button_quit.draw(screen)


        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_lvl.click(pos):
                    in_game(1)
                if button_lvl_2.click(pos):
                    lvl_choice = 2
                    in_game()
                if button_lvl_3.click(pos):
                    lvl_3()
                if button_lvl_4.click(pos):
                    lvl_4()
                if button_lvl_5.click(pos):
                    lvl_5()
                if button_lvl_6.click(pos):
                    lvl_6()
                if button_lvl_7.click(pos):
                    lvl_7()
                if button_lvl_8.click(pos):
                    lvl_8()
                if button_lvl_9.click(pos):
                    lvl_9()
                if button_lvl0.click(pos):
                    lvl0()
                if button_quit.click(pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        CLOCK.tick(FPS)
                
    pygame.quit()

class Level_1():
    def __init__(self,enemies):
            self.enemies = enemies
            self.progression = 0

    def spawn_wave_1(self):
        pass
        self.Red_1 = Red(5,350,[(144,114),(280,114),(280,300),(750/2-31,302)],2)
        self.Red_2 = Red(350,5,[(114,144),(280,114),(280,300),(750/2-31,302)],2)
        enemies.append(self.Red_1)
        enemies.append(self.Red_2)

    def spawn_wave_2(self):
        self.Blue_1 = Blue(1,1,[(100,600)],1)
        self.Blue_2 = Blue(705,1,[(555,600)],1)
        self.Drone_1 = Drone_Arc(50,50,[(50,50)],2)
        self.Drone_2 = Drone_Arc(666,50,[(700-34,50)],2)

        enemies.append(self.Blue_1)
        enemies.append(self.Blue_2)
        enemies.append(self.Drone_1)
        enemies.append(self.Drone_2)
    
    def animate(self):
        self.Red_1.follow_path()
        self.Red_2.follow_path()
        if self.progression == 1:
            self.Blue_1.follow_path()
            self.Blue_2.follow_path()
            pass

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y,img):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = img
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (self.x, self.y)) 

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate_laser(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center = (self.x, self.y)) 
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self, obj):
        offset_x = obj.x - self.rect.left
        offset_y = obj.y - self.rect.top
        return self.mask.overlap(obj.mask, ((int(offset_x)), ((int(offset_y)))))
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= -50)

class Linear_Laser(Laser):
    def __init__(self,x,y,img):
        super().__init__(x,y,img)

    def move(self, speed):
        self.y += speed

    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))
    
    def collision(self, obj):
        return collide(self, obj)

class Targeted_Laser(Laser):
    def __init__(self,x,y,img,dx,dy):
        super().__init__(x,y,img)
        self.dx = dx
        self.dy = dy

    def move(self, speed):
        self.x += self.dx*speed
        self.y += self.dy*speed
        self.rect = self.image.get_rect(center = (self.x, self.y))

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0
        self.distance = 0
        self.checkpoint_list = -1

    def cooldown(self):
        if self.cooldown_counter >= self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def rotate_ship(self,angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.mask = pygame.mask.from_surface(self.image)

    def follow_path(self):

        if not self.distance:
            if self.checkpoint_list < (len(self.path)-1):
                self.checkpoint_list += 1

            mx, my = (self.path[self.checkpoint_list][0],self.path[self.checkpoint_list][1])

            radians = math.atan2(((self.path[self.checkpoint_list])[1] - self.y ), ((self.path[self.checkpoint_list])[0]) - self.x)
            self.distance = math.hypot(self.x - ((self.path[self.checkpoint_list])[0]), self.y - ((self.path[self.checkpoint_list])[1])) / self.speed
            self.distance = int(self.distance)
                
            self.dx = math.cos(radians) * self.speed
            self.dy = math.sin(radians) * self.speed

        if self.distance:
            self.distance -= 1
            self.x += self.dx
            self.y += self.dy

class MainShip(Ship): 
    COOLDOWN = 15
    def __init__(self, x, y):
        super().__init__(x, y)
        self.original_image = MAIN_SHIP 
        self.laser_img = MAIN_LASER
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100000
        self.laser_speed = 5
        

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    def move_laser(self,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-self.laser_speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= 10
                        if obj.health <= 0:
                            objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Linear_Laser(((self.x+(self.get_width())/2)-2.5), self.y-20, self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

class Drone_Arc(Ship):
    COOLDOWN = 40
    def __init__(self, x,y,path,speed):
        super().__init__(x,y)
        self.original_image = DRONE_ARC
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.laser_speed = 1
        self.angle = 0
        self.laser_img = ARC_LASER
        self.health = 40
        self.speed = speed
        self.path = path

    def shoot(self, angle):

        if self.cooldown_counter == 0:

            radians = math.atan2((player.y+player.get_height()/2 - (self.y+self.get_height()/2)),(player.x+player.get_width()/2- (self.x+self.get_width()/2)))
            dx = math.cos(radians)
            dy = math.sin(radians)
            
            cx, cy =  self.x + self.get_height() / 2, self.y + self.get_width()/2
            lx, ly = cx + dx * (self.get_height()/2), cy + dy * (self.get_height()/2)
            
            laser_1 = Targeted_Laser(lx, ly,self.laser_img,dx, dy)
            laser_1.rotate_laser(angle)
            self.lasers.append(laser_1)

            self.cooldown_counter = 1

    def move_lasers(self,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(self.laser_speed)
            if laser.collision(obj):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

class Blue(Ship):
    
    COOLDOWN = 40
    def __init__(self, x,y,path,speed):
        super().__init__(x,y)
        self.original_image = BLUE_SHIP
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.laser_speed = 3
        self.angle = 0
        self.laser_img = MAIN_LASER
        self.health = 40
        self.speed = speed
        self.path = path

    def shoot(self,angle):
        if self.cooldown_counter == 0:

            radians_1= math.atan2((player.y+player.get_height()/2 - (self.y+self.get_height()/2)),(player.x+player.get_width()/2- (self.x+self.get_width()/2)))
            radians_2= math.atan2((player.y+player.get_height()/2 - (self.y+self.get_height()/2)),(player.x+player.get_width()/2- (self.x+self.get_width()/2)))+0.261799
            radians_3= math.atan2((player.y+player.get_height()/2 - (self.y+self.get_height()/2)),(player.x+player.get_width()/2- (self.x+self.get_width()/2)))-0.261799

            dx_1= math.cos(radians_1)
            dy_1= math.sin(radians_1)
            dx_2= math.cos(radians_2)
            dy_2= math.sin(radians_2)
            dx_3= math.cos(radians_3)
            dy_3= math.sin(radians_3)

            cx, cy =  self.x + self.get_height() / 2, self.y + self.get_width()/2
            lx, ly = cx + dx_1 * (self.get_height()/2 + 2.5), cy + dy_1 * (self.get_height()/2 + 2.5)

            laser_1 = Targeted_Laser(lx, ly, self.laser_img,dx_1, dy_1)
            laser_2 = Targeted_Laser(lx, ly, self.laser_img,dx_2, dy_2)
            laser_3 = Targeted_Laser(lx, ly, self.laser_img,dx_3, dy_3)
            laser_1.rotate_laser(angle)
            laser_2.rotate_laser(angle-15)
            laser_3.rotate_laser(angle+15)

            self.lasers.append(laser_1)
            self.lasers.append(laser_2)
            self.lasers.append(laser_3)
            self.cooldown_counter = 1

    def move_lasers(self,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(self.laser_speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

class Red(Ship):
    COOLDOWN = 30

    def __init__(self, x,y,path,speed):
        super().__init__(x,y)
        self.original_image = RED_SHIP
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.laser_speed = 1
        self.angle = 0
        self.laser_img = MAIN_LASER
        self.health = 40
        self.speed = speed
        self.path = path

    def shoot(self,angle):
        if self.cooldown_counter == 0:
            laser = Linear_Laser((self.x+(self.get_width())/2),(self.y+(self.get_height()/2)), self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1
        
    def move_lasers(self,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(self.laser_speed)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(screen)

    def rotate_ship(self,angle):
        pass

main_menu()