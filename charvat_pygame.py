# "pyGame Bullet Hell" - by Hunter Charvat
# Created for SI 206 Fall 2016, project 4, taught by Colleen van Lent
# Version 1 - 12/2/2016
#
# ***************************************************
#*** You need to have a gampad connected to play ***
# ***************************************************
# Sources:
#     The pyGame Documentation:
#         http://www.pygame.org/docs/index.html
#         Everything in this program canbe found here, very helpful.
#
#     The Official Python Documentation:
#         https://docs.python.org/3/library/random.html
#         Was especially useful for the random module in this game.async
#
#     thenewboston Pygame Tutorial Video Series by Bucky Roberts
#         https://www.youtube.com/watch?v=K5F-aGDIYaM&list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq&index=1
#         I used this to learn some best pracices of pygame, and build the basic frameworks such as display.set, update, etc.

#     Gamepad monitor program by Paul Vincent Craven
#         http://programarcadegames.com/python_examples/show_file.php?file=joystick_calls.py
#         Used this to learn how python interprets input from the gamepad

#     'game.py' by TheLycaeum of Github.
#         https://github.com/TheLycaeum/pygame
#         Took some inspiration regarding group functionality and projectile creation.


import pygame
import pygame.sprite
from pygame import locals
import random

X_MAX = 800
Y_MAX = 600

MILLI_DIFFICULTY_UP = 15000 #the time between difficulty increases

GAME_EXIT = True

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255,165,0)

VEL_MUL = 3 #player speed

LIFE_COUNT = 2
SCORE = 0

FIREEVENT = pygame.USEREVENT+1 #event that checks if the player should shoot
pygame.time.set_timer(FIREEVENT, 125)

EN_FIRE = pygame.USEREVENT+2 #event that checks if the enemies should shoot
pygame.time.set_timer(EN_FIRE, 250)

GO_TXT = "You ran out of lives. Press A to play again, B to quit." #game over text
GE_TXT = "Thanks for playing!" #game exit text

screen = pygame.display.set_mode((X_MAX, Y_MAX))
pygame.display.set_caption('pygame Bullet Hell')

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

song = 'Battalium_Retribution.wav'
pygame.mixer.init()
pygame.mixer.music.load(song)
pygame.mixer.music.play()

#groups used to handle various collision and other functionality
ENEMIES = pygame.sprite.Group()
EN_SHIPS = pygame.sprite.Group()
EN_BUL = pygame.sprite.Group()
FRIENDS = pygame.sprite.Group()
NEUTRAL = pygame.sprite.Group()
SPRITES = pygame.sprite.Group()

#the player controller class
class Player(pygame.sprite.Sprite):
    def __init__(self, lives):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = X_MAX/2
        self.y = Y_MAX/2
        self.dx = self.dy = 0
        self.hp = 5
        self.lives = lives
        self.type = 'F' #type is occasionally used in projectile creation

    def move(self):
        if (float(self.x) + self.dx) >= float(0) and (float(self.x) + self.dx) <= float(X_MAX): #check that player is staying on screen
            self.x += self.dx

        if (self.y + self.dy) >= float(0) and (self.y + self.dy) <= float(Y_MAX): #check that player is staying on screen
            self.y += self.dy

        self.rect.center = (self.x, self.y)

    def damage(self):
        self.hp -= 1

class FriendBullets(pygame.sprite.Sprite):
    def __init__(self, p, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = p.x
        self.y = p.y
        self.dx = dx
        self.dy = dy
        self.type = 'F'
        self.hp = 10

    def move(self):
        self.x += self.dx * 10
        self.y += self.dy * 10
        self.rect.center = (self.x, self.y)
        if self.y <= 0 or self.y >= Y_MAX or self.x <= 0 or self.x >= X_MAX:
            self.kill()

    def hit(self, target): #currently unused
        return self.rect.colliderect(target)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()

class Spiral(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = random.randint(0, X_MAX)
        self.y = 0
        self.rect.center = (self.x, self.y)
        self.vel = 0
        self.hp = 2
        self.type = 'spi'

    def move(self):
        if self.vel == 0:
            self.vel = random.randint(1, 2)
        self.y += self.vel
        self.rect.center = (self.x, self.y)
        if self.y >= Y_MAX:
            self.kill() #get rid of the sprite if it goes off screen

    def hit(self, target):
        return self.rect.colliderect(target)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()


class SpiralBullets(pygame.sprite.Sprite):
    def __init__(self, en):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.x = en.x
        self.y = en.y
        self.dx = random.uniform(-1.0, 1.0)
        self.dy = random.uniform(-1.0, 1.0)
        self.hp = 1
        self.type = en.type

    def move(self):
        if self.type == 'spi': #check if the enemy shooting is a spiral or zag
            self.x += self.dx * 2
            self.y += self.dy * 2
            self.rect.center = (self.x, self.y)
            if self.y <= 0 or self.y >= Y_MAX or self.x <= 0 or self.x >= X_MAX:
                self.kill()
                del self
        elif self.type == 'zag':
            self.y += 3
            self.rect.center = (self.x, self.y)
            if self.y <= 0 or self.y >= Y_MAX or self.x <= 0 or self.x >= X_MAX:
                self.kill()
                del self
    def hit(self, target):
        return self.rect.colliderect(target)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()

class Zag(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = random.randint(0, X_MAX)
        self.y = 0
        self.rect.center = (self.x, self.y)
        self.vel = random.randint(1, 2)
        self.hp = 2
        self.dx = random.randint(-3, 3)
        self.type = 'zag'

    def move(self):
        self.y += self.vel
        self.x += self.dx
        if self.x >= X_MAX or self.x <= 0:
            self.dx = -self.dx
        self.rect.center = (self.x, self.y)
        if self.y >= Y_MAX:
            self.kill()

    def hit(self, target):
        return self.rect.colliderect(target)

    def damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()


def message(txt, color):
    screen_text = font.render(txt, True, color)
    screen.blit(screen_text, [X_MAX/8, Y_MAX/2])

def displayHP(p):
    screen_text = font.render("HP:" + str(p.hp), True, (0, 255, 255))
    screen.blit(screen_text, [X_MAX - 55, Y_MAX - 25])


def displayLives(p):
    screen_text = font.render("Lives:" + str(p.lives), True, (0, 255, 255))
    screen.blit(screen_text, [5, Y_MAX-25])

def displayScore():
    global SCORE
    screen_text = font.render("Score:" + str(SCORE), True, (0, 255, 255))
    screen.blit(screen_text, [X_MAX -500, Y_MAX-25])

def displayTime(time):
    screen_text = font.render(str(time), True, (0, 255, 255))
    screen.blit(screen_text, [X_MAX - 300, Y_MAX - 25])

def gameLoop(game_over, game_exit, p):
    global SCORE
    pygame.init()

    pygame.joystick.init()  #intiate gamepad functionality

    try:
        j = pygame.joystick.Joystick(0)  # create a joystick instance
        j.init()  # init instance of joystick
    except pygame.error:
        print('Please connect a gamepad and try again.')
        quit()



    bx = 0
    by = -1

    SPRITES.add(p)
    NEUTRAL.add(p)


    while game_exit:
        if p.lives <= 0:
            game_over = True

        while game_over:
            screen.fill(BLACK)
            message(GO_TXT, RED)
            pygame.display.update()

            for e in pygame.event.get():
                if e.type == pygame.locals.QUIT:
                    pygame.quit()

                elif e.type == pygame.locals.JOYBUTTONDOWN:
                    if e.button == 0: #if button A pressed
                        z = Player(2)
                        FRIENDS.empty()
                        ENEMIES.empty()
                        SPRITES.empty()
                        NEUTRAL.empty()
                        EN_SHIPS.empty()
                        pygame.mixer.music.rewind()
                        gameLoop(False, True, z)

                    elif e.button == 1: #if button B pressed
                        screen.fill(BLACK)
                        message(GE_TXT, RED)
                        pygame.display.update()
                        pygame.quit()

        #logic for randomly generating enemies
        passed_time = pygame.time.get_ticks()
        diff_modifier = passed_time / MILLI_DIFFICULTY_UP
        en_p = 100 - diff_modifier
        en_v = random.randint(0, 100)

        if en_v > en_p and en_v % 2 == 0:
            temp = Zag()
            ENEMIES.add(temp)
            EN_SHIPS.add(temp)

        elif en_v > en_p:
            temp = Spiral()
            ENEMIES.add(temp)
            EN_SHIPS.add(temp)

        for e in pygame.event.get(): #handle inputs
            if e.type == pygame.locals.QUIT:
                pygame.quit()

            elif e.type == pygame.locals.JOYAXISMOTION:
                x, y = j.get_axis(0), j.get_axis(1)
                if x > .2:  # move right
                    p.dx = x * VEL_MUL #scale the speed
                elif x < -.2:  # move left,
                    p.dx = x * VEL_MUL
                else: #don't move on the x
                    p.dx = 0
                if y > .2:  # move down
                    p.dy = y * VEL_MUL
                elif y < -.2:  # move up
                    p.dy = y * VEL_MUL
                else: #Don't move on the y
                    p.dy = 0

                if j.get_axis(4) > .1: #shoot right
                    bx = j.get_axis(4)
                elif j.get_axis(4) < -.1: #shoot left
                    bx = j.get_axis(4)
                if j.get_axis(3) > .025: #shoot down
                    by = j.get_axis(3)
                elif j.get_axis(3) < -.025: #shoot up
                    by = j.get_axis(3)
                if j.get_axis(3) < .1 and j.get_axis(3) > -.1 and j.get_axis(4) < .1 and j.get_axis(4) > -.1:
                    by = -1
                    bx = 0


            if e.type == FIREEVENT:
                FRIENDS.add(FriendBullets(p, bx, by))
            if e.type == EN_FIRE:
                for en in EN_SHIPS.sprites():
                    ENEMIES.add(SpiralBullets(en))
                    EN_BUL.add(SpiralBullets(en))


        for en in ENEMIES.sprites():
            SPRITES.add(en)
            en.move() #move the enemies

        for fbul in FRIENDS.sprites():
            SPRITES.add(fbul)
            fbul.move() #move the friendly bullets

        p.move()

        hit_en_lis = pygame.sprite.groupcollide(FRIENDS, ENEMIES, False, True)
        hit_p_lis = pygame.sprite.groupcollide(NEUTRAL, ENEMIES, False, True)

        for point in hit_en_lis.values():
            SCORE += 1 #for every enemy sprite killed, score increase

        for hit in hit_p_lis.values():
            for ship in hit:
                p.damage() #for every enemy that hits player, take damage

        screen.fill(BLACK)

        if p.hp <= 0:
            p.lives -=1
            p.hp = 5
            p.x = X_MAX / 2
            p.y = Y_MAX / 2

        #Display HUD
        displayHP(p)
        displayLives(p)
        displayScore()
        displayTime(passed_time / 1000)
        #update the screen
        SPRITES.update()
        SPRITES.draw(screen)
        pygame.display.update()

        clock.tick(60)



def main():
    game_exit = True
    game_over = False
    p = Player(LIFE_COUNT)
    gameLoop(game_over, game_exit, p)
    quit()

if __name__ == '__main__':
  main()