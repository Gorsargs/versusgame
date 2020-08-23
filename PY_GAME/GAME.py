import pygame
from animation import animation_png
import threading
import time
pygame.init()
clock = pygame.time.Clock()
winX = 800
winY = 400
win = pygame.display.set_mode((winX,winY))
isleft = False
isright = True
animcount = 0
diecount = 0
animstop = False

pygame.display.set_caption("Retro V")
#####png for animation




class Health():
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    def draw(self):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
HP_1 = Health(26,25,120,12,(255,20,147))
HP_2 = Health(646,25,120,12,(255,20,147))



class Png_animation():
    def __init__(self,png,x,y):
        self.png = png
        self.x = x
        self.y = y
        #self.vel = vel
        self.sunline = True
        self.x_copy = x
        self.y_copy = y
        self.isright = False
        self.isleft = True
        self.x_vel = 0.8
        self.y_vel = 0.8
    def static_draw(self):
        win.blit(self.png,(self.x,self.y))

    def draw(self):
        win.blit(self.png,(self.x,self.y))
        if self.sunline == True:
            self.x += self.x_vel
            self.y -= self.y_vel
            self.y_vel -= 0.001

        if self.x > (winX+20):
            self.sunline = False
        if self.sunline == False:
            time.sleep(3)
            self.x = self.x_copy
            self.y = self.y_copy
            self.y_vel = 1
            self.sunline = True
    def choosing_draw(self):
        self.left = keys[pygame.K_LEFT]
        self.right = keys[pygame.K_RIGHT]
        win.blit(self.png,(self.x,self.y))
        if self.left:
            self.isleft = True
            self.isright = False
            self.x = replay_yes.x - 5
            self.y = replay_yes.y - 5
        elif self.right:
            self.isleft = False
            self.isright = True
            self.x = replay_no.x - 5
            self.y = replay_no.y - 5

def replay_press_yes_or_no(character,character1):
    global run
    global replay
    life = 10
    if replay_choosing.isleft:
        if keys[pygame.K_KP_ENTER]:
            replay = False
            character.life = life
            character1.life = life
    elif replay_choosing.isright:
        if keys[pygame.K_KP_ENTER]:
            pygame.QUIT = True
            run = False





sun = Png_animation(animation_png.sun,-200,300)
left_health = Png_animation(animation_png.left_health,20,20)
#health_box = Png_animation(animation_png.left_health_box,25,25)
right_health = Png_animation(animation_png.right_health,winX - 160,20)
#right_health_box = Png_animation(animation_png.right_health_box,winX - 154,25)
######### HERE IS PNGs for Replay
replay_black_screen = Png_animation(animation_png.replay_black_screen,0,0)
replay_yes = Png_animation(animation_png.replay_yes,winX//2-150,winY-100)
replay_no = Png_animation(animation_png.replay_no,winX//2 +100,winY-100)
replay_choosing = Png_animation(animation_png.replay_choosing,replay_yes.x-5,replay_yes.y-5)
replay_game = Png_animation(animation_png.replay,winX-500,winY-300)






class Bomb():
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 4*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class Character():
    def __init__(self,x,width,height,vel,color,isright = True,isleft = False,jumpcount = 15,life = 10,hitcount = 10):
        self.isjump = False
        self.gravity = 10
        self.jumpcount = jumpcount
        self.width = width
        self.height = height
        self.vel = vel
        self.x = x
        self.y = winY - self.height - 10
        self.b = jumpcount
        self.isleft = isleft
        self.isright = isright
        self.isfire = False
        self.facing = 0
        self.bullets = []
        self.bullets2 = []
        self.color = color
        self.life = life
        self.die = False
        self.life_temp = life
    def move(self,a,d,w,space):
        global replay
        self.hitbox = (self.x+10, self.y+5,self.width -20,self.height - 10)
        if not(replay):
            if not(self.die):
                self.left = keys[a]
                self.right = keys[d]
                self.up = keys[w]
                self.fire = keys[space]
                if self.left  and self.x > 5:
                    self.x -= self.vel
                    self.isleft = True
                    self.isright = False
                if self.right and self.x < winX  - self.width - 5:
                    self.x += self.vel
                    self.isleft = False
                    self.isright = True
                    bomb = None
                if self.up:
                    self.isjump = True
                if self.isjump:
                    if self.jumpcount >= -(self.b):
                        if self.jumpcount < 0:
                            self.y += (self.jumpcount**2)//self.gravity
                        else:
                            self.y -= (self.jumpcount**2)//self.gravity
                        self.jumpcount -= 1
                    else:
                        self.isjump = False
                        self.jumpcount = self.b
                if self.fire:
                    if self.isleft:
                        self.facing = -4
                        if len(self.bullets2) < 1:
                            self.bullets2.append(Bomb(round(self.x + self.width // 2 - 50),round(self.y +
                                            self.height // 2 + 5 ),5,self.color,facing = self.facing))

                    elif self.isright:
                        self.facing = 4
                        if len(self.bullets) < 1:
                            self.bullets.append(Bomb(round(self.x + self.width // 2 + 50),round(self.y +
                                            self.height // 2 + 5 ),5,self.color,facing = self.facing))
        if replay:
            if self.isjump:
                if self.jumpcount >= -(self.b):
                    if self.jumpcount < 0:
                        self.y += (self.jumpcount**2)//self.gravity
                    else:
                        self.y -= (self.jumpcount**2)//self.gravity
                    self.jumpcount -= 1
                else:
                    self.isjump = False
                    self.jumpcount = self.b

    def get_hited(self):
        global replay
        if self.life >= 1:
            self.life -= 1
        if self.life < 1:
            self.die = True
            replay = True
    def health(self,hp):
        hp.width = (self.life) * 12
        hp.draw()

def touch_line(character,character1):
    if character.right:
        if character.x + character.width > character1.x + character1.width//1.5 and character.x + character.width < character1.x + character1.width:
            if character.y > character1.y - character1.height and character1.y + character1.height > character.y:
                character.x -= character.vel

    elif character.left:
        if character.x < character1.x + character1.width//3 and character.x + character.width > character1.x + character1.width:
            if character.y > character1.y - character1.height and character1.y + character1.height > character.y:
                character.x += character.vel








def shooting(character,character1):
    for bullet in character.bullets:
        if bullet.y - bullet.radius < character1.hitbox[1] + character1.hitbox[3] and bullet.y + bullet.radius > character1.hitbox[1]:
            if character1.die == False:
                if bullet.x + bullet.radius > character1.hitbox[0] + character1.hitbox[2]//2 - 20 and bullet.x - bullet.radius < character1.hitbox[0] + character1.hitbox[2]:
                    character.bullets.pop(character.bullets.index(bullet))
                    character1.get_hited()
                    if character1.x > 5 and character1.x + character1.width < winX - 30:
                        character1.x += 30

        if bullet.x < character.x + winX: #and bullet.x > 0:
            bullet.x += bullet.vel
        if bullet.x > character.x + winX:
            character.bullets.pop(character.bullets.index(bullet))
    for bullet in character.bullets2:
        if bullet.y - bullet.radius < character1.hitbox[1] + character1.hitbox[3] and bullet.y + bullet.radius > character1.hitbox[1]:
            if character1.die == False:
                if bullet.x + bullet.radius > character1.hitbox[0] + character1.hitbox[2]//2 - 10  and bullet.x - bullet.radius < character1.hitbox[0] + character1.hitbox[2]:
                    character.bullets2.pop(character.bullets2.index(bullet))
                    character1.get_hited()
                    if character1.x > 5 and character1.x < winX - character1.width :
                        character1.x -= 30


        if bullet.x > character.x - winX:
            bullet.x += bullet.vel
        if bullet.x < character.x - winX:
            character.bullets2.pop(character.bullets2.index(bullet))
    touch_line(character,character1)






def animation(character):
    global animcount
    global animstop
    global diecount
    if not(character.die):
        if character.left and not character.isjump:
            if character.fire:
                win.blit(animation_png.left_walk_shoot[animcount // 4],(character.x,character.y))
            else:
                win.blit(animation_png.left_walk[animcount // 4],(character.x,character.y))
        elif character.right and not character.isjump:
            if character.fire:
                win.blit(animation_png.right_walk_shoot[animcount // 4],(character.x,character.y))
            elif not character.fire:
                win.blit(animation_png.right_walk[animcount // 4],(character.x,character.y))
        elif character.isleft and not character.isjump and not character.left:
            if character.fire:
                win.blit(animation_png.left_shoot[0],(character.x,character.y))
            elif not character.fire:
                win.blit(animation_png.left_idle[animcount // 3],(character.x,character.y))
        if character.isleft and character.isjump:
            if character.fire:
                win.blit(animation_png.left_jump_shoot[0],(character.x,character.y))
            elif not character.fire:
                win.blit(animation_png.left_jump[animcount // 3],(character.x,character.y))
        elif character.isright and not character.isjump and not character.right:
            if character.fire:
                win.blit(animation_png.right_shoot[0],(character.x,character.y))
            elif not character.fire:
                win.blit(animation_png.right_idle[animcount // 3],(character.x,character.y))
        elif character.isright and character.isjump:
            if character.fire:
                win.blit(animation_png.right_jump_shoot[0],(character.x,character.y))
            elif not character.fire:
                win.blit(animation_png.right_jump[animcount // 3],(character.x,character.y))
        for bullet in character.bullets:
            bullet.draw(win)
        for bullet in character.bullets2:
            bullet.draw(win)
    elif character.die:
        if character.isright:
            if not(animstop):
                win.blit(animation_png.right_die[diecount // 3],(character.x,character.y))
                diecount += 1
                if diecount == 29:
                    animstop = True
            elif animstop:
                win.blit(animation_png.right_died,(character.x,character.y))

        elif character.isleft:
            if not(animstop):
                win.blit(animation_png.left_die[diecount // 3],(character.x,character.y))
                diecount += 1
                if diecount == 29:
                    animstop = True
            elif animstop:
                win.blit(animation_png.left_died,(character.x,character.y))
    pygame.draw.rect(win,(255,0,0),character.hitbox,-1)


def sun_threaded():
    win.blit(animation_png.background1,(0,0))
    t = threading.Thread(target=sun.draw, name="Thread-1")
    t.start()




my_character = Character(x=10,width = 130, height = 130, vel = 12,color = (48,213,200))
my_second_character = Character(x = 660,width = 130, height = 130, vel = 12,color = (0,255,0),isleft = True,isright = False)

def drawWin():
    global animcount
    global diecount
    global animstop
    if animcount > 29:
        animcount = 0
    if diecount > 29:
        diecount = 0


    sun_threaded()

    win.blit(animation_png.background,(0,0))

    my_character.health(HP_1)
    my_second_character.health(HP_2)
    left_health.static_draw()
    right_health.static_draw()


    animation(my_character)
    animation(my_second_character)
    if replay == True:
        replay_black_screen.static_draw()
        replay_yes.static_draw()
        replay_no.static_draw()
        replay_choosing.choosing_draw()
        replay_game.static_draw()
        replay_press_yes_or_no(my_character,my_second_character)
        if replay == False:
            my_character.x = 10
            my_second_character.x = 660
            animstop = False
            if my_character.die == True:
                my_character.die = False
            if my_second_character.die == True:
                my_second_character.die = False

    pygame.display.update()
    animcount += 1


run = True
replay = False

### Game main loop
while run:

    clock.tick(30)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    my_character.move(pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_l)
    my_second_character.move(pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_g)

    shooting(my_character,my_second_character)
    shooting(my_second_character,my_character)

    drawWin()

pygame.quit()
