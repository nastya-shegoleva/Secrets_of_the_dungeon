import math
from random import choice, sample

import pygame
import os
import sys

from data_db import db_session
from data_db.creating_tag import add_game
from data_db.game_func import Game

WIDHT = 1550
HEIGHT = 800
SIZE_SP = 50
FPS = 40


# загрузка изображений
def load_image(name, colorkey=None) -> pygame.Surface:
    pygame.init()
    fullname = os.path.join('image', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image.convert_alpha()
    return image


class Block_1(pygame.sprite.Sprite):
    block = pygame.Surface((65, 120), pygame.SRCALPHA)

    def __init__(self, x, y):
        super().__init__(block_group, all_sprites)
        self.image = self.block
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = self.rect.x


class Block_2(pygame.sprite.Sprite):
    block = pygame.Surface((50, 120), pygame.SRCALPHA)

    def __init__(self, x, y):
        super().__init__(block_group, all_sprites)
        self.image = Block_2.block
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = self.rect.x


class Surface_water(pygame.sprite.Sprite):
    water = pygame.Surface((50, 10), pygame.SRCALPHA)

    def __init__(self, x, y):
        super().__init__(water_group, all_sprites)
        self.image = Surface_water.water
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = self.rect.x


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x = (obj.abs_pos + self.dx) % WIDHT

    def update(self):
        self.dx = 0


# начало игры
def start_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
        pygame.display.flip()


# экран проигрыша
def game_over_screen():
    global screen

    # фото, текст и кнопки на экране проигрыша
    image_game_over = pygame.transform.scale(load_image('game_over.jpg'), (screen.get_size()))
    text = font.render("You've lost", True, 'lightskyblue')
    button_game_over = pygame.transform.scale(load_image('button_game_over.png', -1), (80, 80))
    button_menu = pygame.transform.scale(load_image('button_menu_in_game_over_screen.png', -1), (80, 80))

    running = True
    flag_game_over = False
    flag_menu_screen = False
    while running:
        screen.blit(image_game_over, (0, 0))
        screen.blit(text, (570, 300))
        screen.blit(button_game_over, (830, 400))
        screen.blit(button_menu, (650, 400))
        pygame.draw.rect(screen, 'black', (820, 390, 100, 100), 4)
        pygame.draw.rect(screen, 'black', (640, 390, 100, 100), 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # начинаем игру заново
                if 820 <= event.pos[0] <= 920 and 390 <= event.pos[1] <= 490:
                    flag_game_over = True
                    running = False

                # переход в меню
                if 640 <= event.pos[0] <= 740 and 390 <= event.pos[1] <= 490:
                    flag_menu_screen = True
                    running = False
        pygame.display.flip()
    if flag_game_over:
        level_1()
    if flag_menu_screen:
        splash_screen()


# экран настроек
def setting_screen():
    global screen, sound_flag, sound_status

    # кнопки
    text = font.render('Sound', True, 'aquamarine2')

    x, y = 620, 200
    button_group = pygame.sprite.Group()
    for word in ['Off', 'On']:
        Button(button_group, word, x, y)
        y += 120

    # фото
    image_setting = pygame.transform.scale(load_image('setting.jpg'), screen.get_size())
    pygame.display.set_caption('Setting')

    running = True
    esc_key = False

    while running:
        if not esc_key:
            screen.blit(image_setting, (0, 0))
            screen.blit(text, (650, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        esc_key = True
                button_group.draw(screen)
                button_group.update(event)
                if sound_status == 'off':
                    sound_flag = False
                if sound_status == 'on':
                    sound_flag = True
                if sound_flag:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.pause()
        else:
            esc_key = splash_screen()
        button_group.draw(screen)
        button_group.update()
        pygame.display.flip()


# экран рейтинга
def rating_screen():
    global screen, level, SCORE

    text = font.render("Rating", True, 'palegreen2')
    image = pygame.transform.scale(load_image('rating.jpg'), screen.get_size())
    pygame.display.set_caption('Rating')

    running = True
    esc_key = False

    while running:
        if not esc_key:
            screen.blit(image, (0, 0))
            screen.blit(text, (600, 50))

            lst = []
            db_sess = db_session.create_session()
            game = db_sess.query(Game).all()
            lst.extend(game)
            list_db = sorted(lst, key=lambda x: x.create_date, reverse=True)
            db_sess.close()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    esc_key = True
            count = 1
            y = 3
            for el in list_db[:6]:
                if SCORE != 'GAME OVER':
                    meaning_rating = font_button.render(
                        f'{count} | {el.level} | {el.score}',
                        True, pygame.Color("white"))
                    count += 1
                    screen.blit(meaning_rating, (620, y * SIZE_SP))
                    y += 1
        else:
            esc_key = splash_screen()
        pygame.display.flip()


# выигрыш
def win_screen():
    global screen

    # фото, текст и кнопки на экране выигрыша
    image_win_screen = pygame.transform.scale(load_image('win_screen.jpg'), (screen.get_size()))
    text = font.render('You win!', True, 'dodgerblue1')
    menu_button = pygame.transform.scale(load_image('button_menu.png', -1), (70, 70))

    running = True
    while running:
        screen.blit(image_win_screen, (0, 0))
        screen.blit(text, (600, 300))
        screen.blit(menu_button, (720, 390))
        pygame.draw.rect(screen, 'dodgerblue1', (710, 380, 90, 90), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # открываем окно меню при нажатии на кнопку
                if 710 <= event.pos[0] <= 800 and 380 <= event.pos[1] <= 470:
                    running = False
        pygame.display.flip()
    game_over_screen()


# переход на 2 уровень
def next_level_2_screen():
    global screen

    # фото, текст и кнопки на экране перехода на 2 уровень
    image_level_2 = pygame.transform.scale(load_image('next_level_2_screen.png'), screen.get_size())
    text = font.render('Level 2', True, 'palegreen1')
    button_go_over_2 = pygame.transform.scale(load_image('button_go_over_2.png', -1), (100, 70))

    running = True
    while running:
        screen.blit(image_level_2, (0, 0))
        screen.blit(text, (600, 300))
        screen.blit(button_go_over_2, (870, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # открываем окно 2 уровня при нажатии на стрелку
                if 870 <= event.pos[0] <= 970 and 300 <= event.pos[1] <= 370:
                    running = False
        pygame.display.flip()
    level_2()


# переход на 3 уровень
def next_level_3_screen():
    global screen

    # фото, текст и кнопки на экране перехода на 3 уровень
    image_next_level_3_screen = pygame.transform.scale(load_image('next_level_3_screen.png'), (screen.get_size()))
    text = font.render('Level 3', True, 'skyblue2')
    button_go_over_3 = pygame.transform.scale(load_image('button_go_over_3.png', -1), (100, 70))

    running = True
    while running:
        screen.blit(image_next_level_3_screen, (0, 0))
        screen.blit(text, (600, 300))
        screen.blit(button_go_over_3, (870, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # открываем окно 3 уровня при нажатии на стрелку
                if 870 <= event.pos[0] <= 970 and 300 <= event.pos[1] <= 370:
                    running = False
        pygame.display.flip()
    level_2()


# завершение игры
def close():
    global SCORE, level
    if level:
        add_game(SCORE, level)
    pygame.quit()
    sys.exit()


# пауза
def pause_screen():
    global sound_flag
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if sound_flag:
                pygame.mixer.music.unpause()
                return False
            else:
                return False
    return True


def load_level(filename):
    filename = 'level/' + filename
    with open(filename, 'r') as mapfile:
        level_map = [line.strip() for line in mapfile]
    maxW = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(maxW, '.')), level_map))


# класс кнопок главного меню
class Button(pygame.sprite.Sprite):
    button_green = pygame.transform.scale(load_image('green_button.png'), (300, 100))

    def __init__(self, button_group, text, x, y):
        super().__init__(button_group)
        self.image = Button.button_green
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.text = text
        self.all_text = font_button.render(self.text, True, 'seagreen4')

    def update(self, *args) -> None:
        global level, sound_status
        screen.blit(self.all_text, (self.rect.x + 80, self.rect.y + 28))
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.text == 'Play':
                level = 1
            if self.text == 'Setting':
                level = 'setting'
            if self.text == 'Rating':
                level = 'rating'
            if self.text == 'Off':
                sound_status = 'off'
            if self.text == 'On':
                sound_status = 'on'


def generate_level(level):
    x, y = None, None
    hero = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Block_1(x * 50, y * 53)
            elif level[y][x] == '&':
                Block_2(x * 50.7, y * 51)
            elif level[y][x] == '@':
                Surface_water(x * 51, y * 55)
            elif level[y][x] == '%':
                hero = Main_Hero(x * SIZE_SP, y * SIZE_SP)
                level[y][x] = "."
            elif level[y][x] == '*':
                Coins(x * SIZE_SP, y * SIZE_SP)
                level[y][x] = "."
            elif level[y][x] == '!':
                Dot(x * SIZE_SP, y * SIZE_SP)
                level[y][x] = "."
    return x, y, hero


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None
        self.pos = None
        self.sheet = None
        self.frames = []

    def get_event(self, event):
        pass

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))


# привидения
class Ghost(Sprite):
    colums = 4
    row = 1
    img = pygame.transform.scale(load_image('ghost_2.png', -1), (360, 110))
    ghost_img = pygame.transform.flip(img, True, False)

    def __init__(self):
        super().__init__(ghost_group)
        self.sheet = Ghost.ghost_img
        self.frames = []
        self.cut_sheet(self.sheet, Ghost.colums, Ghost.row)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = self.image.get_rect()
        self.rect.x = WIDHT + 150
        self.rect.y = 620

        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        if self.rect.x == -150:
            self.kill()
        else:
            self.rect.x -= 1.8


class Main_Hero(Sprite):
    columns = 10
    rows = 1
    img = pygame.transform.scale(load_image("main_hero.png", -1), (730, 100))

    def __init__(self, x, y):
        super().__init__(hero_group)
        self.vec = pygame.math.Vector2
        self.ACC = 0.2
        self.FRIC = -0.2

        self.sheet = Main_Hero.img
        self.frames = []
        self.cut_sheet(self.sheet, Main_Hero.columns, Main_Hero.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)
        self.pos = self.vec(x // SIZE_SP, y // SIZE_SP)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args) -> None:
        global block_group, water_group

        contact = pygame.sprite.spritecollide(self, block_group, False)
        if contact:
            self.pos.y = contact[0].rect.top + 1
            self.vel.y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if keys[pygame.K_UP]:
            self.cur_frame = 1
            self.image = self.frames[self.cur_frame]

        global SCORE, level, camera, ghost
        if pygame.sprite.spritecollideany(self, water_group) or pygame.sprite.spritecollideany(self,
                                                                                               ghost_group) and SCORE != 'GAME OVER':
            if level == 1 or level == 2 or level == 3:
                add_game(SCORE, level)
            self.kill()
            create_particles((self.rect[0], self.rect[1]))
            SCORE = 'GAME OVER'
            level = None

    def jump(self):
        global block_group
        contact = pygame.sprite.spritecollide(self, block_group, False)
        if contact:
            self.vel.y = -15

    def move(self):
        self.acc = self.vec(0, 0.5)

        # меняем направление движения и фото спрайта
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.rect.x > 20:
            self.rotate('left')
            self.acc.x = -self.ACC
        if pressed_keys[pygame.K_RIGHT] and self.rect.x < 1460:
            self.rotate('right')
            self.acc.x = self.ACC

        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        # передвигаем всю локацию
        global camera
        camera.dx -= self.vel.x * 2

        for sprite in all_sprites:
            camera.apply(sprite)

    # поворот спрайта
    def rotate(self, movement):
        self.frames = []
        if movement == "left":
            image = pygame.transform.flip(Main_Hero.img, True, False)
            self.cut_sheet(image, Main_Hero.columns, Main_Hero.rows)
            self.image = self.frames[self.cur_frame]
        elif movement == "right":
            image = Main_Hero.img
            self.cut_sheet(image, Main_Hero.columns, Main_Hero.rows)
            self.image = self.frames[self.cur_frame]


def level_1():
    global screen, level, hero_group, ghost_group, block_group, coins_group, particle_group, max_x, max_y, \
        camera, water_group, level_map, SCORE

    hero_group = pygame.sprite.Group()  # главный герой
    coins_group = pygame.sprite.Group()  # монеты
    ghost_group = pygame.sprite.Group()  # привидения
    particle_group = pygame.sprite.Group()  # частицы
    block_group = pygame.sprite.Group()  # блоки
    water_group = pygame.sprite.Group()  # вода

    pause = False
    time = False
    esc_key = False
    level = 1
    clock = pygame.time.Clock()
    count = 1
    SCORE = 0
    x_pos_location = 0
    running = True

    pygame.display.set_caption('1 уровень')
    location_1 = pygame.transform.scale(load_image('location_1.jpg'), screen.get_size())

    # загружаем карту игры
    level_map = load_level(f"level_1.map")
    max_x, max_y, hero = generate_level(level_map)

    # создаем новую группу спрайтов и экземпляр класса Camera
    all_sprites = pygame.sprite.Group()
    all_sprites.add(hero)
    camera = Camera()
    camera.update()

    while running:
        text = font_button.render(f'SCORE: {SCORE}', True, 'white')

        if not esc_key:
            if not pause:
                screen.fill(0)
                screen.blit(location_1, (x_pos_location, 0))
                screen.blit(location_1, (x_pos_location + WIDHT, 0))
                screen.blit(location_1, (x_pos_location - WIDHT, 0))
                screen.blit(location_1, (x_pos_location + WIDHT + WIDHT, 0))
                screen.blit(location_1, (x_pos_location + WIDHT + WIDHT + WIDHT, 0))

                x_pos_location -= hero.vel.x * 2

                if count == SCORE:
                    level += 1
                    running = False
                    next_level_2_screen()
                if SCORE == 'GAME OVER':
                    if not time:
                        time_now = pygame.time.get_ticks() + 3000
                        time = True
                elif SCORE % 2 == 0:
                    generate_coins(level_map, hero.rect.x)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close()

                    elif event.type == pygame.KEYDOWN:
                        hero.update(event)
                        if event.key == pygame.K_UP:
                            hero.jump()
                        elif event.key == pygame.K_p:
                            pygame.mixer.music.pause()
                            pause = True
                        elif event.key == pygame.K_ESCAPE:
                            pygame.mixer.music.pause()
                            esc_key = True
                hero.move()
                hero.update()

                for entity in all_sprites:
                    screen.blit(entity.image, entity.rect)
                update_screen(screen, text)

                # окно game over
                if time and time_now <= pygame.time.get_ticks():
                    game_over_screen()
                    running = False
            else:
                pause = pause_screen()
        else:
            if level:
                if level == 1:
                    add_game(SCORE, level)
                    esc_key = splash_screen()

        pygame.display.update()
        clock.tick(FPS)


def update_screen(screen, text, ghost=False, coins=True, block=True, water=True, particle=True, dot=True):
    if hero:
        hero_group.update()
        hero_group.draw(screen)
    if block:
        block_group.update()
        block_group.draw(screen)
    if ghost:
        ghost_group.update()
        ghost_group.draw(screen)
    if water:
        water_group.update()
        water_group.draw(screen)
    if coins:
        coins_group.draw(screen)
        coins_group.update()
    if particle:
        particle_group.draw(screen)
        particle_group.update()
    if dot:
        dot_group.draw(screen)
        dot_group.update()
    screen.blit(text, (WIDHT - text.get_width() - 50, 10))


def level_2():
    global screen, level, hero_group, ghost_group, block_group, coins_group, particle_group, max_x, max_y, \
        camera, water_group, level_map, SCORE, ghost, HP_ghost, HP_hero

    hero_group = pygame.sprite.Group()  # главный герой
    coins_group = pygame.sprite.Group()  # монеты
    ghost_group = pygame.sprite.Group()  # привидения
    particle_group = pygame.sprite.Group()  # частицы
    block_group = pygame.sprite.Group()  # блоки
    water_group = pygame.sprite.Group()  # вода

    bullet = pygame.transform.scale(load_image("arrow.png", -1), (20, 10))  # пули
    lst_bullet = []
    HP_ghost, HP_hero = 2, 3

    pause = False
    time = False
    esc_key = False
    time_ghost = False
    count = 17
    block_group = pygame.sprite.Group()
    # загружаем карту игры
    level_map = load_level(f"level_2.map")
    max_x, max_y, hero = generate_level(level_map)

    # создаем новую группу спрайтов и экземпляр класса Camera
    all_sprites = pygame.sprite.Group()
    all_sprites.add(hero)
    camera = Camera()
    camera.update()

    pygame.display.set_caption('Уровень 2')
    location_2 = pygame.transform.scale(load_image('location_2.png').convert(), screen.get_size())
    location_2_width = location_2.get_width()
    titles = math.ceil(WIDHT / location_2_width) + 1

    level = 2
    clock = pygame.time.Clock()
    SCORE = 0
    x_pos_location = 0
    run = True

    # привидение
    ghost = Ghost()
    ghost_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(ghost_timer, 7000)

    while run:

        if not esc_key:
            if not pause:

                for i in range(0, titles):
                    screen.blit(location_2, (i * location_2_width - x_pos_location, 0))

                if lst_bullet:
                    for pos, bul in enumerate(lst_bullet):
                        screen.blit(bullet, (bul.x, bul.y))
                        bul.x += 8
                        if bul.x > 1550 and hero.rect.x < 1550:
                            lst_bullet.pop(pos)
                        if ghost:
                            if bul.colliderect(ghost):
                                if HP_ghost > 0:
                                    HP_ghost -= 1
                                    if HP_ghost == 0:
                                        HP_ghost = 2
                                        ghost.kill()
                                lst_bullet.pop(pos)

                key = pygame.key.get_pressed()
                if key[pygame.K_LEFT] and x_pos_location > 0:
                    x_pos_location += hero.vel.x * 2
                    print(hero.vel.x * 2, x_pos_location)
                if key[pygame.K_RIGHT] and x_pos_location < 3000:
                    x_pos_location += hero.vel.x * 2

                if abs(x_pos_location) > location_2_width:
                    x_pos_location = 0

                text = font_button.render(f'HP: {HP_hero}  SCORE: {SCORE}', True, 'white')

                # смена картинки у привидения
                if not time_ghost:
                    time_now_ghost = pygame.time.get_ticks() + 400
                    time_ghost = True
                else:
                    if time_ghost and time_now_ghost <= pygame.time.get_ticks():
                        time_now_ghost = pygame.time.get_ticks() + 400
                        time_ghost = False
                        ghost.cur_frame = (ghost.cur_frame + 1) % len(ghost.frames)
                        ghost.image = ghost.frames[ghost.cur_frame]

                if count == SCORE:
                    level += 1
                    next_level_3_screen()
                if SCORE == 'GAME OVER':
                    if not time:
                        time_now = pygame.time.get_ticks() + 3000
                        time = True
                if not coins_group:
                    generate_coins(level_map, hero.rect.x)
                if HP_hero < 3:
                    generate_dot()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close()
                    if event.type == ghost_timer and ghost.rect.x == -150 and SCORE != 'GAME OVER':
                        ghost = Ghost()
                    elif event.type == pygame.KEYDOWN:
                        hero.update(event)
                        if event.key == pygame.K_UP:
                            hero.jump()
                        elif event.key == pygame.K_SPACE:
                            lst_bullet.append(bullet.get_rect(topleft=(hero.rect.x + 40, hero.rect.y + 17)))
                        elif event.key == pygame.K_p:
                            pygame.mixer.music.pause()
                            pause = True
                        elif event.key == pygame.K_ESCAPE:
                            esc_key = True
                hero.move()
                hero.update()
                ghost.update()
                ghost_group.draw(screen)
                ghost_group.update()
                for entity in all_sprites:
                    screen.blit(entity.image, entity.rect)
                update_screen(screen, text)
                if time and time_now <= pygame.time.get_ticks():
                    game_over_screen()
                    run = False
            else:
                pause = pause_screen()
        else:
            if level:
                esc_key = splash_screen()
        pygame.display.update()
        clock.tick(50)


# экран меню
def splash_screen():
    global screen, level, hero_group, ghost_group, block_group, coins_group, particle_group, max_x, max_y, SCORE, sound_flag

    # фото и текст на экране меню
    main_menu = pygame.transform.scale(load_image('main_menu.jpg'), screen.get_size())
    text = font.render('Secrets of the dungeon', True, 'seagreen1')
    button_group = pygame.sprite.Group()

    x, y = 590, 215
    for word in ['Play', 'Rating', 'Setting']:
        Button(button_group, word, x, y)
        y += 130

    level = None
    SCORE = 0

    while True:
        screen.blit(main_menu, (0, 0))
        screen.blit(text, (WIDHT // 2 - text.get_width() // 2, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            button_group.draw(screen)
            button_group.update(event)
        if level == 1:
            level = 1
            level_1()
        if level == 'setting':
            setting_screen()
        if level == 'rating':
            rating_screen()
        if sound_flag:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.pause()
        button_group.draw(screen)
        button_group.update()
        pygame.display.flip()


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_group, all_sprites)
        self.image = pygame.transform.scale(load_image("icon-dollar.png", -1), (SIZE_SP // 2, SIZE_SP // 2))
        self.rect = self.image.get_rect(center=(SIZE_SP // 2, SIZE_SP // 2))
        self.rect = self.rect.move(x, y)
        self.pos = (x // SIZE_SP, y // SIZE_SP)
        self.abs_pos = self.rect.x

    def update(self) -> None:
        global SCORE, level_map
        x, y = self.pos
        if pygame.sprite.spritecollideany(self, hero_group):
            if SCORE != 'GAME OVER':
                SCORE += 1
            self.kill()
            if level:
                level_map[y][x] = '*'


def generate_coins(level_map, hero_x):
    for y in range(sample([0, 1, 2], 1)[0], len(level_map), 2):
        for x in range(sample([0, 1, 2], 1)[0], len(level_map[y]), 2):
            if level_map[y][x] == '*' and x * SIZE_SP > hero_x:
                Coins(x * SIZE_SP, y * SIZE_SP)
                level_map[y][x] = '.'


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png", -1)]

    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(choice(fire), (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.4

    def update(self, *args):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, 1550, 800)):
            self.kill()


class Dot(pygame.sprite.Sprite):
    dot = pygame.transform.scale(load_image("dot.png", -1), (SIZE_SP, SIZE_SP))

    def __init__(self, x, y):
        super().__init__(dot_group, all_sprites)
        self.image = Dot.dot
        self.rect = self.image.get_rect(center=(SIZE_SP // 2, SIZE_SP // 2))
        self.rect = self.rect.move(x, y)
        self.pos = (x // SIZE_SP, y // SIZE_SP)
        self.abs_pos = self.rect.x

    def update(self) -> None:
        global HP_hero, level_map
        x, y = self.pos
        # print(x, y)
        if pygame.sprite.spritecollideany(self, hero_group):
            if HP_hero < 3:
                HP_hero += 1
            self.kill()
            if level == 2:
                level_map[y][x] = '*'


def generate_dot():
    global level_map
    for y in range(sample([0, 1, 2], 1)[0], len(level_map), 2):
        for x in range(sample([0, 1, 2], 1)[0], len(level_map[y]), 2):
            if level_map[y][x] == '!':
                Dot(x * SIZE_SP, y * SIZE_SP)
                level_map[y][x] = '.'


if __name__ == "__main__":
    pygame.init()

    # экран
    screen = pygame.display.set_mode((WIDHT, HEIGHT))
    pygame.display.set_caption('Secrets of the dungeon')

    # шрифт
    font = pygame.font.Font('font/TanaUncialSP.otf', 70)
    font_button = pygame.font.Font('font/TanaUncialSP.otf', 40)

    # группы спрайтов
    hero_group = pygame.sprite.Group()  # главный герой
    coins_group = pygame.sprite.Group()  # монеты
    ghost_group = pygame.sprite.Group()  # привидения
    particle_group = pygame.sprite.Group()  # частицы
    block_group = pygame.sprite.Group()  # блоки
    water_group = pygame.sprite.Group()  # вода
    all_sprites = pygame.sprite.Group()  # все спрайты
    dot_group = pygame.sprite.Group()  # зелья

    # подключение звука
    pygame.mixer.music.load('sound/звук_пещеры.mp3')

    # подключение базы данных
    db_session.global_init("db/game_secret.db")

    SCORE = 0
    camera = None
    level = None
    hero = None
    ghost = None
    level_map = None
    max_x = 31
    max_y = 14
    HP_ghost, HP_hero = 2, 3
    sound_flag = True
    sound_status = None
    splash_screen()
