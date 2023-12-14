import math

import pygame
import os
import sys

WIDHT = 1550
HEIGHT = 800
SIZE_SP = 50


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
    img_block = pygame.transform.scale(load_image('tile.jpg'), (65, 120))

    def __init__(self, x, y):
        super().__init__(block_group)
        self.image = Block_1.img_block
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = self.rect.x
        self.y, self.x = self.rect.y, self.rect.x


class Block_2(pygame.sprite.Sprite):
    img_block = pygame.transform.scale(load_image('img.png'), (50, 120))

    def __init__(self, x, y):
        super().__init__(block_group)
        self.image = Block_2.img_block
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = self.rect.x


class Surface_water(pygame.sprite.Sprite):
    img_block = pygame.transform.scale(load_image('img_1.png'), (50, 120))

    def __init__(self, x, y):
        super().__init__(block_group)
        self.image = Surface_water.img_block
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = self.rect.x


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = (obj.abs_pos + self.dx) % 1550

    def update(self):
        self.dx = 0
        self.dy = 0


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
        pass
        # LEVEL 1
    if flag_menu_screen:
        splash_screen()


# экран настроек
def setting_screen():
    pass


# экран рейтинга
def rating_screen():
    pass


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
    Level_2()
    # ОТКРЫТЬ 2 УРОВЕНЬ
    next_level_3_screen()


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
    # ОТКРЫТЬ 3 УРОВЕНЬ
    win_screen()


# завершение игры
def close():
    pygame.quit()
    sys.exit()


# пауза
def pause_screen():
    pass


def update_group(screen, text, hero=True, coins=True, block=True, ghost=True):
    if hero:
        hero_group.update()
        hero_group.draw(screen)
    if coins:
        coins_group.update()
        coins_group.draw(screen)
    if block:
        block_group.update()
        block_group.draw(screen)
    if ghost:
        ghost_group.update()
        ghost_group.draw(screen)


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
        global level
        screen.blit(self.all_text, (self.rect.x + 80, self.rect.y + 28))
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            print(self.text)
            if self.text == 'Play':
                level = 1


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
                Surface_water(x * 51, y * 51)
            elif level[y][x] == '%':
                hero = Main_Hero(x * SIZE_SP, y * SIZE_SP)
                level[y][x] = '.'

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


class Main_Hero(Sprite):
    columns = 10
    rows = 1
    img = pygame.transform.scale(load_image("main_hero.png", -1), (1425, 189))

    def __init__(self, x, y):
        super().__init__(hero_group)
        self.vec = pygame.math.Vector2
        self.ACC = 0.5
        self.FRIC = -0.12
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

    def update(self, *args) -> None:
        global block_group
        hits = pygame.sprite.spritecollide(self, block_group, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        global SCORE, level, camera
        if pygame.sprite.spritecollideany(self, ghost_group):
            if level == 1:
                '''add_inf_game(SCORE)
                create_particles((self.rect[0], self.rect[1]))'''
                pass
            else:
                '''add_stand_game(SCORE, level)
                create_particles((SIZE_SP * self.pos[0], SIZE_SP * self.pos[1]))'''
                pass
            self.kill()
            SCORE = 'GAME OVER'
            level = None

    def jump(self):
        global block_group
        hits = pygame.sprite.spritecollide(self, block_group, False)
        if hits:
            self.vel.y = -15

    def move(self):
        self.acc = self.vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -self.ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = self.ACC
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def rotate(self, movement):
        x, y = self.pos
        if movement == "up":
            image = Main_Hero.img
            self.cut_sheet(image, Main_Hero.rows, Main_Hero.columns)
            self.image = self.frames[self.cur_frame]
        elif movement == "down":
            image = Main_Hero.img
            self.cut_sheet(image, Main_Hero.rows, Main_Hero.columns)
            self.image = self.frames[self.cur_frame]
        elif movement == "left":
            image = pygame.transform.flip(Main_Hero.img, True, False)
            self.cut_sheet(image, Main_Hero.columns, Main_Hero.rows)
            self.image = self.frames[self.cur_frame]
        elif movement == "right":
            image = Main_Hero.img
            self.cut_sheet(image, Main_Hero.columns, Main_Hero.rows)
            self.image = self.frames[self.cur_frame]

        self.rect = self.rect.move(x * SIZE_SP, y * SIZE_SP)


def level_1():
    global screen, level, hero_group, ghost_group, block_group, coins_group, particle_group, max_x, max_y, camera

    pause = False
    time = False
    esc_key = False
    pygame.display.set_caption('Уровень 1')
    location_1 = pygame.transform.scale(load_image('location_1.jpg'), screen.get_size())
    level = 1
    clock = pygame.time.Clock()
    level_map = load_level(f"level_1.map")
    max_x, max_y, hero = generate_level(level_map)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(block_group)
    all_sprites.add(hero)
    count, SCORE = 0, 10
    camera = Camera()
    camera.update()
    running = True
    while running:

        screen.fill(0)
        screen.blit(location_1, (0, 0))
        if not esc_key:
            if not pause:
                if count == SCORE:
                    return level + 1
                if SCORE == 'GAME OVER':
                    if not time:
                        time_now = pygame.time.get_ticks() + 3000
                        time = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pass
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            hero.jump()
                        elif event.key == pygame.K_p:
                            pygame.mixer.music.pause()
                            pause = True
                        elif event.key == pygame.K_ESCAPE:
                            esc_key = True
                hero.move()
                hero.update()
                for entity in all_sprites:
                    screen.blit(entity.image, entity.rect)
                update_screen(screen)
                if time and time_now <= pygame.time.get_ticks():
                    game_over_screen()
                    running = False
            else:
                pause = pause_screen()
        else:
            if level:
                if level >= 1:
                    pass
        pygame.display.update()
        clock.tick(50)


def update_screen(screen, ghost=False, block=True, particle=False):
    if ghost:
        ghost_group.draw(screen)
        ghost_group.update()
    if block:
        block_group.draw(screen)
    if particle:
        particle_group.draw(screen)
        particle_group.update()


def level_2():
    pygame.display.set_caption('Уровень 2')
    bg = pygame.transform.scale(load_image('location_2.png').convert(), (2448, HEIGHT))
    bg_width = bg.get_width()
    scroll = 0
    titles = math.ceil(WIDHT / bg_width) + 1
    clock = pygame.time.Clock()

    run = True
    while run:

        clock.tick(10)

        for i in range(0, titles):
            screen.blit(bg, (i * bg_width - scroll, 0))

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and scroll > 0:
            scroll -= 5
        if key[pygame.K_RIGHT] and scroll < 3000:
            scroll += 5

        if abs(scroll) > bg_width:
            scroll = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


# экран меню
def splash_screen():
    global screen, level, hero_group, ghost_group, block_group, coins_group, particle_group, max_x, max_y

    # фото и текст на экране меню
    main_menu = pygame.transform.scale(load_image('main_menu.jpg'), screen.get_size())
    text = font.render('Secrets of the dungeon', True, 'seagreen1')
    button_group = pygame.sprite.Group()

    x, y = 590, 215
    for word in ['Play', 'Rating', 'Setting']:
        Button(button_group, word, x, y)
        y += 130

    level = None

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
        button_group.draw(screen)
        button_group.update()
        pygame.display.flip()


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

    camera = None
    level = None
    hero = None
    max_x = 31
    max_y = 14
    splash_screen()
