# Hunter Charvat
# SI 206 Project 4


from pygame import *
from pygame.sprite import *
from random import *
from pygame import locals


X_MAX = 1280
Y_MAX = 720
START, STOP = 0, 1
LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
BGC = (0,42,196)

everything = pygame.sprite.Group()

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.dx = self.dy = 0


    def steer(self, dx, dy):
        print("Maybe not using this")


    def update(self):
        x, y = self.rect.center

        if x + self.dx < X_MAX and x + self.dx > 0:
            x -= self.dx
        if y + self.dy < Y_MAX and y + self.dy > 0:
            y -= self.dy
        self.dx = self.dy = 0
        self.rect.center = x, y

        # if x != X_MAX:
        #     x += (abs(X_MAX / 2 - x) / (X_MAX / 2 - x)) * 2
        # if y != Y_MAX:
        #     y += (abs(Y_MAX - 100 - y) / (Y_MAX - 100 - y)) * 2

        #self.rect.center = x, y

def main():
    init()
    joystick.init()
    joysticks = [joystick.Joystick(x) for x in range(joystick.get_count())]

    screen = display.set_mode((X_MAX, Y_MAX))

    mouse.set_visible(False)

    p = Player()

    sprites =RenderPlain(p)

    while True:
        p.dx = p.dy = 0
        for e in event.get():
            print(e.type)
            if e.type == QUIT:
                quit()
                break
            if e.type == JOYAXISMOTION:
                print("Joystick")
                if e.axis == 0:
                    p.dx = e.pos
                if e.axis == 1:
                    p.dx = e.pos

            screen.fill(BGC)
            sprites.update()
            sprites.draw(screen)
            display.update()


if __name__ == '__main__':
  main()