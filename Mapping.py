from General import *
import pygame
import json
import csv


TILE_CONFIG_FILE = 'tile_config.json'
TILE_WIDTH = TILE_HEIGHT = 16


# Файл tile_config.json содержит информацию о тайлах.
# Данные записываются в формате
# "*номер*": {"isSolid": true/false,
#             "isPlatform": true/false,
#             "leverState": -1/0/1,
#             "damage": *число*}
# ИЛИ
# "*начало*:*конец*": {"isSolid": true/false,
#                      "isPlatform": true/false,
#                      "leverState": -1/0/1,
#                      "damage": *число*}
# Во втором случае всем тайлам, в промежутке от *начало* до *конец*,
# присваиваются одинаковые характеристики.
# Некоторые характеристики можно не указывать, тогда им будет выставлено
# стандартное значение - false (или 0 для damage и -1 для leverState)
# Тайлы, не объявленные в этом файле,
# будут иметь стандартное значение для всех характеристик.


def load_tile_config():
    global tile_config

    with open('data/' + TILE_CONFIG_FILE) as file:
        tile_config_data = json.load(file)

    for key, value in tile_config_data.items():
        if ':' in key:
            start, end = map(int, key.split(':'))
            keys = list(range(start, end + 1))
        else:
            keys = [int(key)]
        for k in keys:
            tile_config[k] = value


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        reader = csv.reader(mapFile, delimiter=';', quotechar='"')
        return [row for row in reader]


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(max(map(len, level))):
            for i, current_tile in enumerate(level[y][x].split(',')):
                if ':' in current_tile:
                    tile_type, lever_id = map(int, current_tile.split(':'))
                else:
                    tile_type, lever_id = int(current_tile), None
                Tile(tile_type, x, y, i)
    return x, y


pygame.init()
screen = pygame.display.set_mode([500] * 2)


tile_config = {}
load_tile_config()


# w, h = tile_images.get_size()
# multiplier = 3
# tile_images = pygame.transform.scale(tile_images, (w * multiplier,
#                                                    h * multiplier))
# TILE_WIDTH, TILE_HEIGHT = TILE_WIDTH * multiplier, TILE_HEIGHT * multiplier


class Tile(pygame.sprite.Sprite):

    tile_images = load_image('tiles.png', (0, 0, 0))
    sheet = cut_sheet(tile_images, 20, 16)

    def __init__(self, tile_type, pos_x, pos_y, z_index=0, lever_id=None):
        global all_sprites, tiles_group
        super().__init__(all_sprites, tiles_group)
        self.z_index = z_index
        self.image = Tile.sheet[tile_type - 1]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)
        config = tile_config.get(tile_type, {})

        self.is_solid = config.get('isSolid', False)
        self.is_platform = config.get('isPlatform', False)

        self.lever_state = config.get('leverState', -1)
        self.is_lever = self.lever_state != -1
        self.lever_id = lever_id

        self.is_interactive = self.is_lever

        self.damage = config.get('damage', 0)
        self.is_trap = self.damage != 0


class TilesGroup(pygame.sprite.Group):
    def draw(self, surface):
        """Рисует все спрайты на поверхности, начиная со спрайтов с наименьним
        z-index."""
        sprites = sorted(self.sprites(), key=lambda sprite: sprite.z_index)
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


# all_sprites = pygame.sprite.Group()
# tiles_group = TilesGroup()
#
#
# # for i in range(200):
# #     for j in range(100):
# #         pos = i, j
# #         Tile(301, *pos, z_index=1)
# #         Tile(41, *pos)
#
#
# screen = pygame.display.set_mode(generate_level(load_level('test_level.txt')))
#
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     clear(screen)
#     tiles_group.draw(screen)
#     pygame.display.flip()
pygame.quit()
