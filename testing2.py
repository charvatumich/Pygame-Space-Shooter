import pygame
import pygame.sprite
from pygame import locals

X_MAX = 800
Y_MAX = 600

GAME_EXIT = True

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 400
        self.dx = self.dy = 0

    def move(self):
        if (float(self.x) + self.dx) > float(0) and (float(self.x) + self.dx) < float(X_MAX):
            self.x += self.dx

        if (self.y + self.dy) > float(0) and (self.y + self.dy) < float(Y_MAX):
            self.y += self.dy

        self.rect.center = (self.x, self.y)


def main():
    pygame.init()

    pygame.joystick.init()  #intiate gamepad functionality

    try:
        j = pygame.joystick.Joystick(0)  # create a joystick instance
        j.init()  # init instance of joystick
    except pygame.error:
        print('Please connect a gamepad and try again.')
        quit()

    screen = pygame.display.set_mode((X_MAX,Y_MAX))
    pygame.display.set_caption('Why so many bullets?')

    screen.fill(BLACK)

    p = Player()
    sprites = pygame.sprite.Group(p)

    GAME_EXIT = True

    while GAME_EXIT:
        for e in pygame.event.get():
            if e.type == pygame.locals.QUIT:
                GAME_EXIT = False
            elif e.type == pygame.locals.JOYAXISMOTION:
                x, y = j.get_axis(0), j.get_axis(1)
                print(x, y)
                if x > .2:  # move right
                    p.dx = x
                if x < -.2:  # move left
                    p.dx = x
                if y > .2:  # move down
                    p.dy = y
                if y < -.2:  # move up
                    p.dy = y
                p.move()
            elif j.get_axis(4) > .2:
                p.dx = j.get_axis(0)
            elif j.get_axis(4) < -.2:
                p.dx = j.get_axis(0)
            elif j.get_axis(3) > .2:
                p.dx = j.get_axis(0)
            elif j.get_axis(3) > .2:
                p.dx = j.get_axis(0)

            elif e.type == pygame.locals.JOYHATMOTION:
                print('hat motion')
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                print('button down')
            elif e.type == pygame.locals.JOYBUTTONUP:
                print('button up')

        screen.fill(BLACK)
        #pygame.draw.rect(screen, WHITE, [400, 300, 10, 10])
        sprites.update()
        sprites.draw(screen)
        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == '__main__':
  main()