import pygame
import pygame.sprite
from pygame import locals
import random

X_MAX = 800
Y_MAX = 600

MILLI_DIFFICULTY_UP = 30000

GAME_EXIT = True

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

VEL_MUL = 5

FIREEVENT = pygame.USEREVENT+1
pygame.time.set_timer(FIREEVENT, 125)

EN_FIRE = pygame.USEREVENT+2
pygame.time.set_timer(EN_FIRE, 500)

GO_TXT = "You ran out of lives. Press A to play again, B to quit."
GE_TXT = "Thanks for playing!"

screen = pygame.display.set_mode((X_MAX, Y_MAX))
pygame.display.set_caption('2016: I Underestimated Everything')

clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

E_LIST = [] #hold enemies
FB_LIST = [] #hold friendly bullets
EB_LIST = [] #hold enemy bullets

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = X_MAX/2
        self.y = Y_MAX/2
        self.dx = self.dy = 0
        self.hp = 5
        self.lives = 3
        self.type = 'F'

    def move(self):
        if (float(self.x) + self.dx) >= float(0) and (float(self.x) + self.dx) <= float(X_MAX):
            self.x += self.dx

        if (self.y + self.dy) >= float(0) and (self.y + self.dy) <= float(Y_MAX):
            self.y += self.dy

        self.rect.center = (self.x, self.y)


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
        self.type = 'E'

    def move(self):
        if self.vel == 0:
            self.vel = random.randint(1, 3)
        self.y += self.vel
        self.rect.center = (self.x, self.y)
        if self.y >= Y_MAX:
            self.kill()


class SpiralBullets(pygame.sprite.Sprite):
    def __init__(self, en):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = en.x
        self.y = en.y
        self.dx = random.uniform(-1.0, 1.0)
        self.dy = random.uniform(-1.0, 1.0)
        self.type = 'E'
        self.hp = 1

    def move(self):
        self.x += self.dx * 2
        self.y += self.dy * 2
        self.rect.center = (self.x, self.y)
        if self.y <= 0 or self.y >= Y_MAX or self.x <= 0 or self.x >= X_MAX:
            self.kill()

def message(txt, color):
    screen_text = font.render(txt, True, color)
    screen.blit(screen_text, [X_MAX/8, Y_MAX/2])

def displayHP(p):
    screen_text = font.render(str(p.hp), True, (0, 255, 255))
    screen.blit(screen_text, [X_MAX - 20, Y_MAX - 25])


def displayLives(p):
    screen_text = font.render(str(p.lives), True, (0, 255, 255))
    screen.blit(screen_text, [5, Y_MAX-25])


def gameLoop(game_over, game_exit):
    pygame.init()

    pygame.joystick.init()  #intiate gamepad functionality

    try:
        j = pygame.joystick.Joystick(0)  # create a joystick instance
        j.init()  # init instance of joystick
    except pygame.error:
        print('Please connect a gamepad and try again.')
        quit()


    p = Player()
    sprites = pygame.sprite.Group(p)
    bx = 0
    by = -1


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
                if e.button == 0:
                    gameLoop(False, True)
                elif e.button == 1:
                    screen.fill(BLACK)
                    message(GE_TXT, RED)
                    pygame.display.update()
                    pygame.quit()

    while game_exit:
        passed_time = pygame.time.get_ticks()
        diff_modifier = passed_time / MILLI_DIFFICULTY_UP
        spiral_p = 100 - diff_modifier
        spiral_v = random.randint(0, 100)
        if spiral_v > spiral_p:
            E_LIST.append(Spiral())

        for e in pygame.event.get():
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
                FB_LIST.append(FriendBullets(p, bx, by))
            if e.type == EN_FIRE:
                for en in E_LIST:
                    EB_LIST.append(SpiralBullets(en))
            # elif e.type == pygame.locals.JOYHATMOTION:
            #     print('hat motion')
            # elif e.type == pygame.locals.JOYBUTTONDOWN:
            #     print('button down')
            # elif e.type == pygame.locals.JOYBUTTONUP:
            #     print('button up')

        p.move()
        for en in E_LIST:
            sprites.add(en)
            en.move()
        for fbul in FB_LIST:
            sprites.add(fbul)
            fbul.move()
        for ebul in EB_LIST:
            sprites.add(ebul)
            ebul.move()


        screen.fill(BLACK)
        displayHP(p)
        displayLives(p)
        sprites.update()
        sprites.draw(screen)
        pygame.display.update()

        clock.tick(60)



def main():
    game_exit = True
    game_over = False
    gameLoop(game_over, game_exit)
    quit()

if __name__ == '__main__':
  main()