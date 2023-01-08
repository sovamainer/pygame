import os
import sys

import pygame


if __name__ == '__main__':
    pygame.init()

size = width, height = 1200, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
v = 20

all_sprites = pygame.sprite.Group()

backg = pygame.image.load("pageTD.png")
backg = pygame.transform.scale(backg, (1200, 700))
screen.blit(backg, (0, 0))

tower = pygame.image.load("pngwing.com.png")
tower = pygame.transform.scale(tower, (200, 200))
screen.blit(tower, (510, 180))

unit_sprites = pygame.sprite.Group()

life = 2

count_death_mob = 0
level = 1


font = pygame.font.Font(None, 50)
text = font.render(f"Уровень {level}", True, (0, 0, 0))
text_x = width // 3
text_y = 10
text_w = text.get_width()
text_h = text.get_height()
screen.blit(text, (text_x, text_y))


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    global start
    intro_text = ["Tower Defense", "",
                  "На вашу базу нападают монстры. Сможете ли вы отбиться?",
                  "Нажмите на любую кнопку мыши, чтобы начать"]

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
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


class Circle(pygame.sprite.Sprite):
    image_1 = pygame.transform.scale(pygame.image.load('i.png'), (50, 50))
    def __init__(self, x, y, r, v, clock):
        super().__init__(unit_sprites, all_sprites)
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.clock = clock
        self.image = Circle.image_1
        self.mask = pygame.mask.from_surface(self.image)
        self.true = True

    def move(self):
        global count_death_mob
        if self.true:
            if self.x < 200:
                self.x += self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x > 1200:
                count_death_mob += 1
                print(count_death_mob)
                self.true = False
            elif self.y <= 320 and self.x >= 747:
                self.x += self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x >= 747:
                self.y -= self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.y >= 447:
                self.x += self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x >= 433:
                self.y += self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.y <= 185:
                self.x += self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x >= 200:
                self.y -= self.v * self.clock.tick() / 250
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))


objects = []

level1, level2, level3 = True, False, False


def levels():
    if level1:
        for i in range(5):
            objects.append(Circle(-50, 380, 10, v, clock))
    if level2:
        for i in range(5):
            objects.append(Circle(-75, 380, 10, v + 10, clock))
    if level3:
        for i in range(5):
            objects.append(Circle(-100, 380, 10, v + 20, clock))


levels()


def do_function(objects):
   for object in objects:
      object.move()


a = True
start_screen()
running = True
while running:
    screen.blit(backg, (0, 0))
    screen.blit(tower, (510, 180))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or life <= 0:
            running = False
    if count_death_mob == 5:
        text = font.render(f"Уровень {level + 1}", True, (0, 0, 0))
        level1 = False
        level2 = True
        count_death_mob += 1
        levels()
    if count_death_mob == 11:
        text = font.render(f"Уровень {level + 2}", True, (0, 0, 0))
        level2 = False
        level3 = True
        count_death_mob += 1
        levels()
    if count_death_mob == 17:
        text = font.render(f"Поздравляю вы победили!", True, (0, 0, 0))
    screen.blit(text, (text_x, text_y))
    do_function(objects)
    pygame.display.flip()
pygame.quit()
