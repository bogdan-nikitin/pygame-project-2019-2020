"""Модуль самой игры."""

import sys

from Modules.Camera import *
from Modules.Enemies import *
from Modules.MenuUI import *
from Modules.Player import *

GAME_TITLE = 'PyDungeon'

LEVELS_FILE = 'levels.json'
LOADING = 'Loading'
LOADING_FONT_SIZE = 30
THE_END = '''The end
Game was made by 
Bogdan Nikitin and 
Vasiliev Alexander 
for the educational platform 
Yandex Lyceum'''.split('\n')
THE_END_FIRST_LINE_FONT_SIZE = 60
THE_END_FONT_SIZE = 20

LINE_SPACING = 10

# Название полей в level.json. Их использование утверждено в README.me.
FIRST_LEVEL = 'firstLevel'
NEXT_STAGE = 'nextStage'
MAP_FILE = 'mapFile'
HERO_POS = 'heroPos'
MUSIC = 'music'
ENEMIES = 'enemies'

ENEMY_TABLE = {'Insect': Insect,
               'Knight': Knight,
               'Snake': Snake,
               # 'Bat': Bat,
               'Rat': Rat}

FPS = 30
USER_EVENT = 1000

# Кнопки управления. Их использование утверждено в README.me.
DEFAULT_ATTACK_KEY = pygame.K_z
RANGE_ATTACK_KEY = pygame.K_x
MOVE_LEFT_KEY = pygame.K_LEFT
MOVE_RIGHT_KEY = pygame.K_RIGHT
JUMP_KEY = pygame.K_UP
MOVE_DOWN_KEY = pygame.K_DOWN
OPEN_MENU_KEY = pygame.K_ESCAPE


class Main:
    """Основной класс игры, включающий в себя игровой цикл."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.hero = None
        self.hero_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.RESIZABLE)

        self.hp_bar = None
        self.stamina_bar = None

        self.levels = None
        self.load_levels_config()
        self.tiles = None
        self.cur_level_name = None

        self.loading_label = Label(LOADING)
        self.loading_label.font_size = LOADING_FONT_SIZE
        self.loading_label.hide()
        self.is_loading = False

        self.menu: typing.Optional[Menu] = None
        self.settings_data = {}

        self.the_end_labels = []
        self.is_end = False

        self.music = None
        self.tick = 0
        self.is_paused = False
        self.full_screen = False
        self.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.camera = Camera(self.screen)

        self.load_next_level()

        self.running = True

    def create_menu(self):
        self.menu = Menu(self, settings_data=self.settings_data)
        self.menu.hide()

    def events(self):
        """Обработка событий."""
        for event in pygame.event.get():
            SpriteGroups.ui_group.event(event)
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.USEREVENT:
                if not self.hero.dead:
                    self.hero.tick()

            elif event.type == pygame.KEYDOWN:
                if not self.hero.dead:
                    if event.key == JUMP_KEY:
                        self.hero.up = True
                    if event.key == MOVE_RIGHT_KEY:
                        self.hero.right = True
                        self.hero.direction = RIGHT
                    if event.key == MOVE_LEFT_KEY:
                        self.hero.left = True
                        self.hero.direction = LEFT

            elif event.type == pygame.KEYUP:

                if not self.hero.stunned:
                    if (event.key == DEFAULT_ATTACK_KEY and
                            not self.hero.is_default_attack and
                            not self.hero.is_range_attack and
                            self.hero.stamina >= HERO_DA_COST):
                        self.hero.stamina -= HERO_DA_COST
                        self.hero.is_default_attack = True
                    elif (event.key == RANGE_ATTACK_KEY and
                          not self.hero.is_range_attack and
                          not self.hero.is_default_attack and
                          self.hero.stamina >= HERO_RA_COST):
                        self.hero.stamina -= HERO_RA_COST
                        self.hero.is_range_attack = True

                if event.key == JUMP_KEY:
                    self.hero.up = False
                if event.key == MOVE_RIGHT_KEY:
                    self.hero.right = False
                if event.key == MOVE_LEFT_KEY:
                    self.hero.left = False
                if event.key == OPEN_MENU_KEY:
                    if self.is_end:
                        self.running = False
                    else:
                        self.is_paused = not self.is_paused
                        if self.is_paused:
                            self.menu.show()
                            if self.music:
                                pygame.mixer.pause()
                        else:
                            self.menu.hide()
                            self.menu.settings_panel.hide()
                            if self.music:
                                pygame.mixer.unpause()

            elif event.type == FULL_SCREEN_EVENT_TYPE:
                full_screen = event.fullscreen
                self.full_screen = full_screen
                self.size = self.screen.get_rect().size
                if full_screen:
                    self.screen = pygame.display.set_mode([0, 0],
                                                          pygame.FULLSCREEN)
                else:
                    self.screen = pygame.display.set_mode(self.size,
                                                          pygame.RESIZABLE)
            elif event.type == RESUME_EVENT.type:
                self.is_paused = False
                self.menu.hide()
                self.menu.settings_panel.hide()
                pygame.mixer.unpause()

            elif event.type == EXIT_EVENT.type:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.VIDEORESIZE:
                if not self.full_screen:
                    self.screen = pygame.display.set_mode(event.size,
                                                          pygame.RESIZABLE)

    def update(self, *args):
        """Обновляет спрайты."""
        SpriteGroups.ui_group.update(*args)
        if not self.is_paused:
            self.camera.update(self.hero)
            for sprite in SpriteGroups.all_sprites:
                if not isinstance(sprite, UIElement):
                    self.camera.apply(sprite)
            SpriteGroups.characters_group.update(*args)
            SpriteGroups.tiles_group.update(*args)
            self.hero.hero_melee_attacks.update(*args)
            self.hero.hero_range_attacks.update(*args)

    def render(self):
        """Отрисовка всех спрайтов."""
        clear(self.screen)
        SpriteGroups.tiles_group.draw(self.screen)
        SpriteGroups.characters_group.draw(self.screen)
        self.hero.hero_melee_attacks.draw(self.screen)
        self.hero.hero_range_attacks.draw(self.screen)
        SpriteGroups.ui_group.draw(self.screen)
        pygame.display.flip()

    def game_cycle(self):
        """Игровой цикл."""
        # изменение состояния персонажа(здоровье и прочее)
        pygame.time.set_timer(pygame.USEREVENT, USER_EVENT)
        while self.running:
            self.events()
            self.update(self.tick)
            self.render()
            # print(self.clock.get_fps())
            self.tick = self.clock.tick(FPS)
        pygame.quit()

    def load_levels_config(self):
        """Загрузка конфигурации уровней."""
        with open(data_path(LEVELS_FILE)) as file:
            self.levels = json.load(file)

    def load_next_level(self):
        """Загрузка следующего (или первого) уровня."""

        self.settings_data = self.menu.settings_data if self.menu else {}

        # Очищаем всё, что осталось от предыдущего уровня

        SpriteGroups.empty_all()
        Tile.clear_map()
        self.camera.reset()

        # Загружаем уровень

        if self.cur_level_name is None:
            self.cur_level_name = self.levels[FIRST_LEVEL]
        else:
            next_level = self.levels[self.cur_level_name].get(NEXT_STAGE)
            if not (next_level and next_level in self.levels):
                self.end_game()
                return
            self.cur_level_name = next_level

        if self.music:
            self.music.stop()

        level_data = self.levels[self.cur_level_name]
        file_name = level_data[MAP_FILE]

        self.spawn_enemies(level_data.get(ENEMIES, []))

        self.set_loading_screen()

        _, _, self.tiles = generate_level(load_level(file_name))

        # Инициализируем всё остальное

        self.hero = Player(self, RIGHT, *level_data[HERO_POS])
        self.hero_group.add(self.hero)

        self.hp_bar = HPBar(self.hero, MAX_HP)
        self.stamina_bar = StaminaBar(self.hero, MAX_STAMINA)

        self.end_loading()

        if MUSIC in level_data:
            self.music = pygame.mixer.Sound(data_path(level_data[MUSIC]))
            self.music.play(-1)

        self.create_menu()

    def end_game(self, message=None, clear_screen=True):
        """Оканчивает игру, выводя на экран сообщение message или THE_END[0],
         если message=None, и строки THE_END[1:]."""
        text = THE_END
        if message:
            text[0] = message

        if clear_screen:
            SpriteGroups.empty_all()

        for i, line in enumerate(THE_END):
            label = Label(line)
            if i == 0:
                label.font_size = THE_END_FIRST_LINE_FONT_SIZE
            else:
                label.font_size = THE_END_FONT_SIZE
            label.hide()
            self.the_end_labels += [label]

        self.tiles = None
        if self.music:
            self.music.stop()
        screen_w, screen_h = self.screen.get_rect().size
        total_h = sum(map(lambda l: l.h + LINE_SPACING, self.the_end_labels))
        total_h -= LINE_SPACING
        cur_y = screen_h // 2 - total_h // 2
        for label in self.the_end_labels:
            w = label.w
            label.set_pos(screen_w // 2 - w // 2, cur_y)
            label.show()
            cur_y += label.h + LINE_SPACING
        pygame.display.flip()
        self.is_end = True

    def set_loading_screen(self):
        """Устанавливает загрузочный экран."""
        clear(self.screen)
        screen_w, screen_h = self.screen.get_rect().size
        w, h = self.loading_label.w, self.loading_label.h
        self.loading_label.set_pos(screen_w // 2 - w // 2,
                                   screen_h // 2 - h // 2)
        self.loading_label.show()
        pygame.display.flip()
        self.is_loading = True

    def spawn_enemies(self, enemies):
        """Призывает врагов."""
        for enemy, *params in enemies:
            enemy_class = ENEMY_TABLE[enemy]
            enemy_class(self, RIGHT, *params)

    def end_loading(self):
        """Убирает загрузочный экран."""
        self.loading_label.hide()
        clear(self.screen)
        self.is_loading = False
