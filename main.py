'''
Spaceship pixel art cuz im bad at art...
https://www.pixilart.com/photo/spaceship-dab5127eb1fe665
https://tinyurl.com/ydafylpp
'''
from dataclasses import dataclass #imports
import sys, os, math, time, random #imports
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Enable print
def enablePrint():
    sys.stdout = sys.__stdout__
blockPrint()
import pygame
enablePrint()

pygame.init()
clock = pygame.time.Clock()

window_size=(1280, 720)

window = pygame.display.set_mode(window_size)
pygame.display.set_caption("SpaceBoi")
#pygame.mixer.music.load("assets/Track1.wav")
#pygame.mixer.music.play(-1)
bgcolor = (45, 49, 52)
player_image = pygame.image.load("assets/ship.png").convert_alpha()
scout_image = pygame.image.load("assets/scout.png").convert_alpha()
scout_image_damaged = pygame.image.load("assets/scout_damaged.png").convert_alpha()
button_down_main = False
button_down_secondary = False
font = pygame.font.Font("freesansbold.ttf", 32)
missile_delay=0
@dataclass
class Enemies:
    scouts=[]
@dataclass
class Bullets:
    missiles = [] 
    bullets = []
@dataclass
class player_health():
    shields = 25
    health = 100
@dataclass
class player_location():
    x = (window.get_width()/2)-40
    y = (window.get_height()/2)-40
@dataclass
class player_moving(): 
    left = False 
    right = False 
    up = False 
    down = False
@dataclass
class last_shot():
    machine_gun = time.time()
    missile = time.time()

def player_movement():
    if player_moving.left:
        player_location.x -= 6
    if player_moving.right:
        player_location.x += 6
    if player_moving.up:
        player_location.y -= 6
    if player_moving.down:
        player_location.y += 6

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y,speed, color):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = speed
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle)*self.speed
        self.y_vel = math.sin(self.angle)*self.speed
        self.color = color
        self.rect = None
    def main(self, window):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        #0, 129, 250
        self.rect=pygame.draw.circle(window, self.color, (self.x, self.y), 5)
#Scout enemy
class Scout:
    def __init__(self):
        self.x = random.randint(0, 1280)
        self.y = 0
        self.speed = 2
        self.angle = math.atan2(self.y-player_location.y, self.x-player_location.x)
        self.x_vel = math.cos(self.angle)*self.speed
        self.y_vel = math.sin(self.angle)*self.speed
        self.color = (255, 166, 0)
        self.shields = 30
        self.health = 20
        self.rect = None
        self.damage = False
        self.type = "scout"
    def main(self, window):
        self.angle = math.atan2(self.y-player_location.y, self.x-player_location.x)
        self.x_vel = math.cos(self.angle)*self.speed
        self.y_vel = math.sin(self.angle)*self.speed
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        rel_x, rel_y = player_location.x - self.x, player_location.y - self.y
        angle_to_pointer =(180 / math.pi) * -math.atan2(rel_y, rel_x)
        angle_to_pointer += 90
        if not self.damage:
            img_copy = pygame.transform.rotate(scout_image, angle_to_pointer)
        else:
            img_copy = pygame.transform.rotate(scout_image_damaged, angle_to_pointer)
            self.damage = False
        window.blit(img_copy, (self.x-int(img_copy.get_width()/2), self.y-int(img_copy.get_height()/2)))
        self.rect = pygame.Rect((self.x-20, self.y-20), (scout_image.get_width(), scout_image.get_height()))
#event handler
def event_handler(event):
    global button_down_main, button_down_secondary
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a: 
            player_moving.left = True
        if event.key == pygame.K_d:
            player_moving.right = True
        if event.key == pygame.K_w:
            player_moving.up = True
        if event.key == pygame.K_s:
            player_moving.down = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            player_moving.left = False
        if event.key == pygame.K_d:
            player_moving.right = False
        if event.key == pygame.K_w: 
            player_moving.up = False
        if event.key == pygame.K_s: 
            player_moving.down = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            button_down_main = True
        if event.button == 3:
            button_down_secondary = True
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            button_down_main = False
        if event.button == 3:
            button_down_secondary = False
#guns
class gun:
    def machine_gun():
        current_time=time.time()
        delay = current_time - last_shot.machine_gun
        #print(delay)
        if delay > 0.1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            Bullets.bullets.append(PlayerBullet(player_location.x, player_location.y, mouse_x, mouse_y, 15, (250, 208, 0)))
            last_shot.machine_gun = time.time()
    def machine_gun_bullets(enemy):
        for bullet in Bullets.bullets:
            if bullet.rect.colliderect(enemy.rect):
                enemy.damage = True
                Bullets.bullets.remove(bullet)
                if enemy.type == "scout":
                    if enemy.shields <= 0:
                        enemy.health -= 5
                    else:
                        enemy.shields -= 5
                    if scout.health <= 0:
                        Enemies.scouts.remove(enemy)
    def missile():
        global missile_delay
        current_time=time.time()
        missile_delay = current_time - last_shot.missile
        #print(delay)
        if missile_delay > 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            Bullets.missiles.append(PlayerBullet(player_location.x, player_location.y, mouse_x, mouse_y, 15, (0, 129, 250)))
            last_shot.missile = time.time()
    def missile_logic(enemy):
        for missile in Bullets.missiles:
            if missile.rect.colliderect(enemy.rect):
                enemy.damage = True
                Bullets.missiles.remove(missile)
                if enemy.type == "scout":
                    Enemies.scouts.remove(enemy)     

while True:
    window.fill(bgcolor) #clear screen with backround color
    #---------------run event handler---------------
    for event in pygame.event.get():
        event_handler(event)
    #-----------------------------------------------
    #--------------trigger(literally)---------------
    if button_down_main:
        gun.machine_gun()
    if button_down_secondary:
        gun.missile()
    for bullet in Bullets.bullets:
        bullet.main(window)
    for missile in Bullets.missiles:
        missile.main(window)
    #-----------------------------------------------
    player_movement() #do player movement
    #------rotate player image to mouse cursor-------
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - player_location.x, mouse_y - player_location.y
    angle_to_pointer =(180 / math.pi) * -math.atan2(rel_y, rel_x)
    angle_to_pointer -= 90
    img_copy = pygame.transform.rotate(player_image, angle_to_pointer)
    window.blit(img_copy, (player_location.x-int(img_copy.get_width()/2), player_location.y-int(img_copy.get_height()/2)))
    #-------------------------------------------------
    #Enemy spawning (Temporary)
    if random.randint(1, 100) > 99:
        Enemies.scouts.append(Scout())

    for scout in Enemies.scouts:
        scout.main(window)
        pygame.draw.rect(window, (0,0,0), scout.rect, 1)
        gun.machine_gun_bullets(scout)
        gun.missile_logic(scout)

    #Bonk
    pygame.display.update() #update *ENTIRE* display
    clock.tick(60) #60 FPS gamers 