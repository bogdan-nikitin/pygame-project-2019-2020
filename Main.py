from Modules.Enemies import *
from Modules.Player import *
from Modules.Configuration import *
from Modules.Mapping import *
from Modules.MenuUI import *
from Modules.General import *
from Modules.GameUI import *
from Modules.Camera import *
from Modules.Enemies import *
from Modules import SpriteGroups
import pygame
import json
import sys


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


ENEMY_TABLE = {'Insect': Insect,
               'Knight': Knight,
               'Snake': Snake,
               'Rat': Rat,
               'Bat': Bat}

FPS = 30


class Main:
    """Основной класс игры, включающий в себя игровой цикл."""
    def __init__(self):
        pygame.init()
        self.hero = None
        self.hero_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.RESIZABLE)
        self.levels = None
        self.load_levels_config()
        self.tiles = None
        self.cur_level_name = None

        self.loading_label = Label(LOADING)
        self.loading_label.font_size = LOADING_FONT_SIZE
        self.loading_label.hide()
        self.is_loading = False

        self.the_end_labels = []
        self.is_end = False

        self.music = None

        self.load_next_level()
        self.tick = 0
        self.camera = Camera(self.screen)
        self.menu = Menu(self)
        self.menu.hide()
        self.is_paused = False
        self.full_screen = False
        self.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.running = True

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
                    if event.key == pygame.K_UP:
                        self.hero.up = True
                    if event.key == pygame.K_RIGHT:
                        self.hero.right = True
                        self.hero.direction = RIGHT
                    if event.key == pygame.K_LEFT:
                        self.hero.left = True
                        self.hero.direction = LEFT

            elif event.type == pygame.KEYUP:

                if not self.hero.stunned:
                    if (event.key == pygame.K_z and
                            not self.hero.is_default_attack and
                            not self.hero.is_range_attack and
                            self.hero.stamina >= HERO_DA_COST):
                        self.hero.stamina -= HERO_DA_COST
                        self.hero.is_default_attack = True
                    elif (event.key == pygame.K_x and
                          not self.hero.is_range_attack and
                          not self.hero.is_default_attack and
                          self.hero.stamina >= HERO_RA_COST):
                        self.hero.stamina -= HERO_RA_COST
                        self.hero.is_range_attack = True

                if event.key == pygame.K_UP:
                    self.hero.up = False
                if event.key == pygame.K_RIGHT:
                    self.hero.right = False
                if event.key == pygame.K_LEFT:
                    self.hero.left = False
                if event.key == pygame.K_ESCAPE:
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

            elif event.type == FULLSCREEN_EVENT_TYPE:
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
        SpriteGroups.ui_group.update(*args)
        if not self.is_paused:
            self.camera.update(self.hero)
            for sprite in SpriteGroups.all_sprites:
                if not isinstance(sprite, UIElement):
                    self.camera.apply(sprite)
            SpriteGroups.characters_group.update(*args)
            SpriteGroups.tiles_group.update(*args)
            self.hero.hero_melee_attacks.update()
            self.hero.hero_range_attacks.update()

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
        # изменение состояния персонажа(здоровье и прочее)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        while self.running:
            self.events()
            self.update(self.tick)
            self.render()
            self.tick = self.clock.tick(FPS)
        pygame.quit()

    def load_levels_config(self):
        with open(data_path(LEVELS_FILE)) as file:
            self.levels = json.load(file)

    def load_next_level(self):

        SpriteGroups.empty_all()

        if self.cur_level_name is None:
            self.cur_level_name = self.levels['firstLevel']
        else:
            next_level = self.levels[self.cur_level_name].get('nextStage')
            if not (next_level and next_level in self.levels):
                self.end_game()
                return
            self.cur_level_name = next_level

        if self.music:
            self.music.stop()

        level_data = self.levels[self.cur_level_name]
        file_name = level_data['mapFile']

        self.set_loading_screen()
        _, _, self.tiles = generate_level(load_level(file_name))
        self.hero = Player(self, RIGHT, *level_data['heroPos'])
        self.hero_group.add(self.hero)
        self.spawn_enemies(level_data.get('enemies', []))
        self.end_loading()

        if 'music' in level_data:
            self.music = pygame.mixer.Sound(data_path(level_data['music']))
            self.music.play(-1)

    def end_game(self, message=None, clear_screen=True):

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
        clear(self.screen)
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
        clear(self.screen)
        screen_w, screen_h = self.screen.get_rect().size
        w, h = self.loading_label.w, self.loading_label.h
        self.loading_label.set_pos(screen_w // 2 - w // 2,
                                   screen_h // 2 - h // 2)
        self.loading_label.show()
        pygame.display.flip()
        self.is_loading = True

    def spawn_enemies(self, enemies):
        for enemy, *params in enemies:
            enemy_class = ENEMY_TABLE[enemy]
            enemy_class(self, RIGHT, *params)

    def end_loading(self):
        self.loading_label.hide()
        clear(self.screen)
        self.is_loading = False


if __name__ == '__main__':
    game = Main()
    game.game_cycle()

