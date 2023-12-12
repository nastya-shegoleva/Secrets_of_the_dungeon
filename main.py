import pygame
import os
import sys

WIDHT = 1550
HEIGHT = 800


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

    def apply(self, obj):
        obj.rect.x = (obj.abs_pos + self.dx) % 1550

    def update(self):
        self.dx = 0


# class Sprite(pygame.sprite.Sprite):
#

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


def generate_level(level):
    x, y = None, None
    # hero = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Block_1(x * 50, y * 53)
            elif level[y][x] == '&':
                Block_2(x * 50.7, y * 51)
            elif level[y][x] == '@':
                Surface_water(x * 51, y * 51)
    return x, y


def level_1():
    global screen, level, hero_group, ghost_group, block_group, coins_group, particle_group, max_x, max_y

    location_1 = pygame.transform.scale(load_image('location_1.jpg'), screen.get_size())
    x = 0

    running = True
    while running:
        level = 1
        screen.fill((0, 0, 0))
        # группы спрайтов
        hero_group = pygame.sprite.Group()  # главный герой
        coins_group = pygame.sprite.Group()  # монеты
        particle_group = pygame.sprite.Group()  # частицы
        block_group = pygame.sprite.Group()  # блоки

        level_map = load_level(f"level_1.map")
        max_x, max_y = generate_level(level_map)

        screen.blit(location_1, (x, 0))
        screen.blit(location_1, (x + 1550, 0))

        camera = Camera()
        camera.update()
        # level_map = load_level(f"level_1.map")
        # hero, max_x, max_y = generate_level(level_map)
        # if x == -1550:
        #     x = 0
        # else:
        #     x -= 0.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
        block_group.update()
        block_group.draw(screen)
        pygame.display.flip()


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

    level = None
    hero = None
    max_x = 31
    max_y = 14

    splash_screen()
