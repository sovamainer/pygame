import os
import sys
import random
import sqlite3
import timeit

import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()


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


def load_image1(name, colorkey=None):
    fullname = os.path.join('images', name)
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


size = width, height = 1200, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


con = sqlite3.connect("pygame_TD.db")
cur = con.cursor()

swords = load_image1("swords.png")
swords = pygame.transform.scale(swords, (40, 40))


endscreen = pygame.image.load("endscreen.jpg")
endscreen = pygame.transform.scale(endscreen, (1200, 700))

backg = pygame.image.load("pageTD.png")
backg = pygame.transform.scale(backg, (1200, 700))
screen.blit(backg, (0, 0))

tower = load_image1("pngwing.com.png")
tower = pygame.transform.scale(tower, (200, 200))
screen.blit(tower, (510, 180))

tower1 = load_image1("pngwing.com.png")
tower1 = pygame.transform.scale(tower1, (200, 200))
screen.blit(tower1, (50, 450))

tower2 = load_image1("pngwing.com.png")
tower2 = pygame.transform.scale(tower2, (200, 200))
screen.blit(tower2, (1100, 194))

ar1 = load_image1("ar1.png")
ar1 = pygame.transform.scale(ar1, (50, 50))

ar2 = load_image1("ar2.png")
ar2 = pygame.transform.scale(ar2, (50, 50))

ar3 = load_image1("ar3.png")
ar3 = pygame.transform.scale(ar3, (50, 50))

ar4 = load_image1("ar4.png")
ar4 = pygame.transform.scale(ar4, (50, 50))

ar5 = load_image1("ar5.png")
ar5 = pygame.transform.scale(ar5, (50, 50))

ar6 = load_image1("ar6.png")
ar6 = pygame.transform.scale(ar6, (50, 50))

upgrade_button = load_image1("upgrade.png")
upgrade_button = pygame.transform.scale(upgrade_button, (26, 26))
screen.blit(upgrade_button, (width // 3, height - 25))

hearts = load_image1("hearts.png")
hearts = pygame.transform.scale(hearts, (50, 50))

little_heart = load_image1("heart1.png")
little_heart = pygame.transform.scale(little_heart, (26, 26))

heart1 = load_image1("heart1.png")
heart1 = pygame.transform.scale(heart1, (50, 50))

heart2 = load_image1("heart2.png")
heart2 = pygame.transform.scale(heart2, (50, 50))

heart3 = load_image1("heart3.png")
heart3 = pygame.transform.scale(heart3, (50, 50))

upgrade_button_bar = load_image1("upgrade_bar_with_green.png")
upgrade_button_bar = pygame.transform.scale(upgrade_button_bar, (175, 66))

coins = load_image1("coins.png")
coins = pygame.transform.scale(coins, (200, 100))

coin1 = load_image1("coin1.png")
coin1 = pygame.transform.scale(coin1, (50, 50))

coin2 = load_image1("coin2.png")
coin2 = pygame.transform.scale(coin2, (50, 50))

coin3 = load_image1("coin3.png")
coin3 = pygame.transform.scale(coin3, (50, 50))

coin4 = load_image1("coin4.png")
coin4 = pygame.transform.scale(coin4, (50, 50))

coin5 = load_image1("coin5.png")
coin5 = pygame.transform.scale(coin5, (50, 50))

coin6 = load_image1("coin6.png")
coin6 = pygame.transform.scale(coin6, (50, 50))

coins_animation = [coin1, coin2, coin3, coin4, coin5, coin6]

archer_animation1 = [ar1, ar2, ar3, ar4, ar5, ar6]
archer_animation2 = [ar1, ar2, ar3, ar4, ar5, ar6]
archer_animation3 = [ar1, ar2, ar3, ar4, ar5, ar6]

archer_counter1 = 0
archer_counter2 = 0
archer_counter3 = 0
coins_animation_counter = 0

all_sprites = pygame.sprite.Group()
towers = pygame.sprite.Group()
unit_sprites = pygame.sprite.Group()
hearts_s = pygame.sprite.Group()
coins_s = pygame.sprite.Group()


count_death_mob = -1
level = 1


font = pygame.font.Font(None, 50)
text = font.render(f"Уровень {level}", True, (0, 0, 0))
text_x = width // 1.3
text_y = 500
text_w = text.get_width()
text_h = text.get_height()
screen.blit(text, (text_x, text_y))
zapus = False
start_timer = None
text_time = None
max_damage = -1
need_input = True
input_text = ''
nickname = ''


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global running, start_timer, input_text, nickname
    start_timer = timeit.default_timer()
    intro_text = ["Tower Defense",
                  "На вашу базу нападают монстры. Сможете ли вы отбиться?",
                  "Обучение: На старте игры вам доступно три башни 1 уровня,",
                  f"У вас есть 10 сердец на всю игру.",
                  "При прохождении моба своего пути становится на 1 жизнь меньше",
                  "Башни атакуют только первую цель из оставшейся банды магов",
                  "Внизу расположен бар с улучшениями для башен:",
                  "Первое улучшение стоит 1 монету и увеличивает урон башни",
                  "Второе улучшение стоит 5 монет и значительно увеличивает урон башни",
                  "Третье улучшение стоит 2 монет и дает дополнительную жизнь башне",
                  "Монеты падают с монстров с неким шансом",
                  "Нажмите на любую кнопку мыши, чтобы начать",
                  "Введите никнейм перед тем как начать игру(без него она не начнется)"]

    fon = pygame.transform.scale(load_image('staaartscreen.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, True, (0, 0, 0))
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
            elif event.type == pygame.KEYDOWN and need_input:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 10:
                        input_text += event.unicode
                        text_surface = font.render(input_text, False, (255, 255, 0))
                        screen.blit(text_surface, (100, height - 100))

            elif event.type == pygame.MOUSEBUTTONDOWN and len(input_text) > 0:
                running = True
                nickname = input_text
                return
        pygame.display.flip()


class Circle():
    image_1 = pygame.transform.scale(load_image1('i.png'), (50, 50))

    def __init__(self, x, y, health, v, clock):
        self.x = x
        self.y = y
        self.health = health
        self.health1 = health
        self.v = v
        self.clock = clock
        self.image = Circle.image_1
        self.mask = pygame.mask.from_surface(self.image)
        self.true = True
        self.attack1 = False
        self.attack2 = False
        self.attack3 = False

    def move(self):
        global count_death_mob, damage, life, archer_counter1, archer_counter2, archer_counter3
        if self.true:
            if self.x < 200:
                self.x += self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x > 1220:
                count_death_mob += 1
                damage -= 0.1
                life -= 1
                self.true = False
            elif self.y <= 320 and self.x >= 747:
                self.x += self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x >= 747:
                self.y -= self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.y >= 447:
                self.x += self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x >= 433:
                self.y += self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.y <= 185:
                self.x += self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))
            elif self.x >= 200:
                self.y -= self.v * 0.05
                screen.blit(self.image, (int(self.x - 20), int(self.y - 20)))

            if self.x >= 370 and self.x <= 850 and self.y >= 130 and self.y <= 610:
                if objects.index(self) == 0:
                    self.health -= damage
                    if archer_counter2 == 36:
                        archer_counter2 = 0
                    screen.blit(archer_animation2[archer_counter2 // 6], (590, 188))
                    archer_counter2 += 1
            else:
                screen.blit(archer_animation2[-1], (590, 188))

            if self.x >= 0 and self.x <= 370 and self.y >= 130:
                if objects.index(self) == 0:
                    self.health -= damage
                    if archer_counter1 == 36:
                        archer_counter1 = 0
                    screen.blit(archer_animation1[archer_counter1 // 6], (130, 460))
                    archer_counter1 += 1
            else:
                screen.blit(archer_animation1[-1], (130, 460))

            if self.x >= 850:
                if objects.index(self) == 0:
                    self.health -= damage
                    if archer_counter3 == 36:
                        archer_counter3 = 0
                    screen.blit(archer_animation3[archer_counter3 // 6], (970, 86))
                    archer_counter3 += 1
            else:
                screen.blit(archer_animation1[-1], (970, 86))

    def get_damage(self):
        global count_death_mob, coins
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 15, self.y - 40, 50 * self.health / self.health1, 10))
        if self.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (self.x - 15 + 50 - 50 * (self.health1 - self.health) / self.health1, self.y - 40, 50 - 50 * (self.health / self.health1), 10))
        else:
            self.true = False
            count_death_mob += 1
            objects.remove(self)
            a = random.randint(1, 3)
            if a == 1 or a == 3:
                coins += 1


upgrade = 2
objects = []
coins = 0
damage = 1 * upgrade
life = 10
v = 20
level1, level2, level3, level4, level5, level6 = False, False, False, False, False, False
lock = True


def levels():
    if level1:
        objects.clear()
        y = -50
        for i in range(5):
            a = Circle(y - 20, 380, 100, v + 20, clock)
            objects.append(a)
            y -= 60
    if level2:
        objects.clear()
        y = -75
        for i in range(7):
            a = Circle(y - 20, 380, 200, v + 40, clock)
            objects.append(a)
            y -= 60
    if level3:
        objects.clear()
        y = -100
        for i in range(9):
            a = Circle(y - 20, 380, 300, v + 60, clock)
            objects.append(a)
            y -= 60
    if level4:
        objects.clear()
        y = -50
        for i in range(11):
            a = Circle(y - 20, 380, 400, v + 80, clock)
            objects.append(a)
            y -= 60
    if level5:
        objects.clear()
        y = -75
        for i in range(13):
            a = Circle(y - 20, 380, 500, v + 90, clock)
            objects.append(a)
            y -= 60
    if level6:
        objects.clear()
        y = -100
        for i in range(15):
            a = Circle(y - 20, 380, 600, v + 100, clock)
            objects.append(a)
            y -= 60


def do_function(objects1):
    for object in objects1:
        object.move()
        object.get_damage()


running = True
start_screen()
timer_end = 0
nickname_game = font.render(f'Ваш никнейм: {nickname}', True, (0, 0, 0))
print(nickname)
while running:
    screen.blit(backg, (0, 0))
    screen.blit(tower, (510, 180))
    screen.blit(tower1, (50, 450))
    screen.blit(tower2, (900, 70))
    max_damage = max(max_damage, damage)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and life == 0:
            life = 10
            count_death_mob = -1
            upgrade = 2
            damage = 1 * upgrade
            level1 = True
            level2 = False
            level3 = False
            level4 = False
            level5 = False
            level6 = False
            text = font.render(f"Уровень {level}", True, (0, 0, 0))
            text_x = width // 1.3
            coins = 0
        elif count_death_mob == 65:
            timer_end = timeit.default_timer() - start_timer
            count_death_mob += 1
        elif event.type == pygame.KEYDOWN and life == 0:
            if event.key == 27:
                life = -1
                timer_end = timeit.default_timer() - start_timer
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= 367 and event.pos[0] <= 398 and event.pos[1] >= 653 and event.pos[1] <= 681 \
                    and count_death_mob != 66:
                if coins >= 1:
                    upgrade += 1
                    damage = upgrade * 1
                    coins -= 1
                    max_damage = max(max_damage, damage)
                else:
                    max_damage = max(max_damage, damage)
            elif event.pos[0] >= 415 and event.pos[0] <= 444 and event.pos[1] >= 652 and event.pos[1] <= 683 \
                    and count_death_mob != 66:
                if coins >= 5:
                    upgrade += 6
                    damage = upgrade * 1
                    coins -= 5
                    max_damage = max(max_damage, damage)
                else:
                    max_damage = max(max_damage, damage)
            elif event.pos[0] >= 461 and event.pos[0] <= 491 and event.pos[1] >= 651 and event.pos[1] <= 682 \
                    and count_death_mob != 66:
                if coins >= 2:
                    life += 1
                    coins -= 2
                    max_damage = max(max_damage, damage)
                else:
                    max_damage = max(max_damage, damage)

    if life > 0:
        if life >= 3:
            screen.blit(heart1, (text_x, text_y + 30))
        elif life == 2:
            screen.blit(heart2, (text_x, text_y + 30))
        elif life == 1:
            screen.blit(heart3, (text_x, text_y + 30))

        screen.blit(upgrade_button_bar, (width // 3.5, height - 60))
        screen.blit(upgrade_button, (width // 3.23, height - 47))
        screen.blit(upgrade_button, (width // 2.84, height - 50))
        screen.blit(upgrade_button, (width // 2.9, height - 45))
        screen.blit(little_heart, (width // 2.59, height - 47))
        text_life = font.render(f"{life}", True, (155, 45, 48))
        screen.blit(text_life, (text_x + 60, text_y + 40))
        text_coins = font.render(f"{coins}", True, (255, 255, 0))
        screen.blit(text_coins, (text_x + 150, text_y + 40))
        screen.blit(swords, (text_x + 180, text_y + 39))
        text_damage = font.render(f"{damage}", True, (150, 75, 0))
        screen.blit(text_damage, (text_x + 230, text_y + 39))
        screen.blit(nickname_game, (10, 70))

        if coins_animation_counter == 36:
            coins_animation_counter = 0
        screen.blit(coins_animation[coins_animation_counter // 6], (text_x + 90, text_y + 30))
        coins_animation_counter += 1

        if count_death_mob == -1:
            count_death_mob += 1
            level1 = True
            levels()
        if count_death_mob == 5:
            text = font.render(f"Уровень {level + 1}", True, (0, 0, 0))
            level1 = False
            level2 = True
            count_death_mob += 1
            levels()
        if count_death_mob == 13:
            text = font.render(f"Уровень {level + 2}", True, (0, 0, 0))
            level2 = False
            level3 = True
            count_death_mob += 1
            levels()
        if count_death_mob == 23:
            text = font.render(f"Уровень {level + 3}", True, (0, 0, 0))
            level3 = False
            level4 = True
            count_death_mob += 1
            levels()
        if count_death_mob == 35:
            text = font.render(f"Уровень {level + 4}", True, (0, 0, 0))
            level4 = False
            level5 = True
            count_death_mob += 1
            levels()
        if count_death_mob == 49:
            text = font.render(f"Уровень {level + 5}", True, (0, 0, 0))
            level5 = False
            level6 = True
            count_death_mob += 1
            levels()
        if count_death_mob == 66:
            text = font.render(f"""Вы победили!""", True, (0, 0, 0))
            text3 = font.render(f"""Текущее время прохождения {round(timer_end, 3)} секунд""", True, (0, 0, 0))
            text_x = width // 3
            screen.blit(text3, (width // 4.5, 100))
        screen.blit(text, (text_x, text_y))
        do_function(objects)
    elif life == -1:
        lock = False
        cuery = 'SELECT nickname, passage_time FROM Data_player'
        a = cur.execute(cuery).fetchall()
        a = sorted(a, key=lambda tup: tup[1])
        best_text = font.render("ЛУЧШИЕ РЕЗУЛЬТАТЫ", True, (255, 255, 255))
        text_1 = font.render(f"1. {a[0][0]} {a[0][1]}", True, (255, 255, 255))
        text_2 = font.render(f"2. {a[1][0]} {a[1][1]}", True, (255, 255, 255))
        text_2_3 = font.render(f"3. {a[2][0]} {a[2][1]}", True, (255, 255, 255))
        text3 = font.render(f"""Текущее время прохождения(неудача) {round(timer_end, 3)} секунд""", True, (255, 255, 255))
        text4 = font.render(f"""Максимальный урон {max_damage}""", True, (255, 255, 255))
        pygame.draw.rect(screen, (255, 255, 255), (200, 150, 100, 50))
        screen.blit(endscreen, (0, 0))
        screen.blit(text3, (width // 12, 500))
        screen.blit(text4, (width // 12, 550))
        screen.blit(best_text, (width // 12, 20))
        screen.blit(text_1, (width // 12, 50))
        screen.blit(text_2, (width // 12, 80))
        screen.blit(text_2_3, (width // 12, 110))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        text = font.render(f"""Вы проиграли!""", True, (0, 0, 0))
        text1 = font.render(f"""Кликните, чтобы начать заново""", True, (0, 0, 0))
        text2 = font.render(f"""Нажмите ESC, чтобы закончить игру""", True, (0, 0, 0))
        text_x = width // 3
        screen.blit(text2, (text_x, text_y + 80))
        screen.blit(text1, (text_x, text_y + 40))
        screen.blit(text, (text_x, text_y))
    pygame.display.flip()
if int(timer_end) > 0 and lock:
    cur.execute(f'INSERT INTO Data_player(passage_time, nickname) VALUES("{round(timer_end, 3)}", "{nickname}")')
    con.commit()
pygame.quit()
