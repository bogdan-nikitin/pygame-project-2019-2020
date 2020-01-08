from Enemies import *
from Player import *
from configuration import *
from Mapping import *
from GameUI import *
from General import *
import SpriteGroups
import pygame
import json
"""Заглушка для модуля Main"""


LEVELS_FILE = 'levels.json'
LOADING = 'Loading'
LOADING_FONT_SIZE = 30
THE_END = '''The end
Game was made by 
Bogdan Nikitin and EvolutionSup 
for the educational platform 
Yandex Lyceum'''.split('\n')
THE_END_FIRST_LINE_FONT_SIZE = 50
THE_END_FONT_SIZE = 20

LINE_SPACING = 10


class Main:
    def __init__(self):
        pygame.init()
        self.hero_group = pygame.sprite.Group()
        self.hero = Player(self, RIGHT, 2, 2)
        self.hero_group.add(self.hero)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.levels = None
        self.load_levels_config()
        self.tiles = None
        self.cur_level_name = None

        self.loading_label = Label(LOADING)
        self.loading_label.font_size = LOADING_FONT_SIZE
        self.loading_label.hide()
        self.is_loading = False

        self.the_end_labels = []
        for i, line in enumerate(THE_END):
            label = Label(line)
            if i == 0:
                label.font_size = THE_END_FIRST_LINE_FONT_SIZE
            else:
                label.font_size = THE_END_FONT_SIZE
            label.hide()
            self.the_end_labels += [label]
        self.is_end = False

        self.music = None

        self.load_next_level()
        self.running = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.USEREVENT:
                if not self.hero.dead:
                    self.hero.tick()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.hero.up = True
                if event.key == pygame.K_RIGHT:
                    self.hero.right = True
                    self.hero.direction = RIGHT
                if event.key == pygame.K_LEFT:
                    self.hero.left = True
                    self.hero.direction = LEFT

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.hero.up = False
                if event.key == pygame.K_RIGHT:
                    self.hero.right = False
                if event.key == pygame.K_LEFT:
                    self.hero.left = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.hero.stunned:
                    if (event.button == pygame.BUTTON_LEFT and
                            not self.hero.is_default_attack and
                            not self.hero.is_range_attack and
                            self.hero.stamina >= HERO_DA_COST):
                        self.hero.stamina -= HERO_DA_COST
                        self.hero.is_default_attack = True
                    elif (event.button == pygame.BUTTON_RIGHT and
                          not self.hero.is_range_attack and
                          not self.hero.is_default_attack and
                          self.hero.stamina >= HERO_RA_COST):
                        self.hero.stamina -= HERO_RA_COST
                        self.hero.is_range_attack = True

    def update(self):
        if not self.hero.dead:
            self.hero.update()
        self.hero.hero_melee_attacks.update()
        self.hero.hero_range_attacks.update()

    def render(self):
        clear(self.screen)
        SpriteGroups.tiles_group.draw(self.screen)
        self.hero_group.draw(self.screen)
        self.hero.hero_melee_attacks.draw(self.screen)
        self.hero.hero_range_attacks.draw(self.screen)
        SpriteGroups.ui_group.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def game_cycle(self):
        # изменение состояния персонажа(здоровье и прочее)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        while self.running:
            self.events()
            self.update()
            self.render()
        pygame.quit()

    def load_levels_config(self):
        with open(data_path(LEVELS_FILE)) as file:
            self.levels = json.load(file)

    def load_next_level(self):

        if self.cur_level_name is None:
            self.cur_level_name = self.levels['firstLevel']
        else:
            next_level = self.levels[self.cur_level_name].get('nextLevel')
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
        self.end_loading()

        if 'music' in level_data:
            self.music = pygame.mixer.Sound(data_path(level_data['music']))
            self.music.play(-1)

    def end_game(self):
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

    def end_loading(self):
        self.loading_label.hide()
        clear(self.screen)
        self.is_loading = False


# pygame.init()
# screen = pygame.display.set_mode([800, 800])
# m = Main(screen)
# m.end_game()
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     clear(screen)
#     if not m.is_loading and not m.is_end:
#         SpriteGroups.tiles_group.draw(screen)
#     SpriteGroups.ui_group.draw(screen)
#     pygame.display.flip()
#
if __name__ == '__main__':
    game = Main()
    game.game_cycle()

