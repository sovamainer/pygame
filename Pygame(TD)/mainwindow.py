import os
import sys

import pygame

if __name__ == '__main__':
    pygame.init()
size = width, height = 1200, 700
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = ["Tower Defense", "",
                  "На вашу базу нападают монстры. Сможете ли вы отбиться?",
                  "Нажмите любую кнопку чтобы начать"]

    fon = pygame.transform.scale(load_image('startscreen.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


backg = pygame.image.load("pageTD.png")
backg = pygame.transform.scale(backg, (1200, 700))
screen.blit(backg, (0, 0))


tower = pygame.image.load("pngwing.com.png")
tower = pygame.transform.scale(tower, (200, 200))
screen.blit(tower, (510, 180))

unit_sprites = pygame.sprite.Group()



class Circle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__(unit_sprites)
        self.x = x
        self.y = y
        self.r = radius

    def move(self):
        global pos_x, pos_y #, running
        #if pos_x >= 1200:
        #    start_screen()
            #running = False
        if right:
            pos_x += v * clock.tick() / 250
            pygame.draw.circle(screen, (255, 0, 0), (int(pos_x), int(pos_y)), 10)
        elif left:
            pass
        elif up:
            pos_y -= v * clock.tick() / 250
            pygame.draw.circle(screen, (255, 0, 0), (int(pos_x), int(pos_y)), 10)
        elif down:
            pos_y += v * clock.tick() / 250
            pygame.draw.circle(screen, (255, 0, 0), (int(pos_x), int(pos_y)), 10)


v = 20
clock = pygame.time.Clock()
pos_x = -150
pos_y = 380
k = -150
hero = Circle(-150, 380, 10)
b = pygame.draw.circle(screen, (255, 0, 0), (int(pos_x), int(pos_y)), 10)
g = False

start_screen()
running = True
while running:
    screen.blit(backg, (0, 0))
    screen.blit(tower, (510, 180))
    right, left, up, down = False, False, False, False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    print(int(pos_x), int(pos_y))
    if pos_x < 200:
        right = True
        hero.move()
    elif pos_y <= 330 and pos_x >= 747:
        up = False
        right = True
        hero.move()
    elif pos_x >= 747:
        right = False
        up = True
        hero.move()
    elif pos_y >= 447:
        down = False
        right = True
        hero.move()
    elif pos_x >= 433:
        right = False
        down = True
        hero.move()
    elif pos_y <= 185:
        up = False
        right = True
        hero.move()
    elif pos_x >= 200:
        right = False
        up = True
        hero.move()
    pygame.display.flip()
pygame.quit()
