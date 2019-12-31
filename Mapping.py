from General import *
import pygame
import json
import csv
import SpriteGroups


TILE_CONFIG_FILE = 'tile_config.json'
tile_width = tile_height = 16


# Информация о tile_config.json перенесена в файл README.md


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
    tiles = {}
    for y in range(len(level)):
        for x in range(len(level[y])):
            tiles[(y, x)] = []
            for i, current_tile in enumerate(level[y][x].split(',')):
                if current_tile:
                    if ':' in current_tile:
                        tile_type, lever_id = map(int, current_tile.split(':'))
                    else:
                        tile_type, lever_id = int(current_tile), None
                    tiles[(y, x)] += [Tile(tile_type, x, y, i)]
    return x + 1, max(map(len, level)), tiles


tile_config = {}
load_tile_config()


class Tile(GameSprite):
    """Класс плитки - основной единицы карты уровня.
    Перед использованием класса должны быть объявлены переменные
    all_tiles: pygame.sprite.Group и tiles_group: TilesGroup."""

    images_loaded = False
    tile_images = None
    sheet = None
    sheet_size = 20, 16
    image_size_multiplier = 1

    def __init__(self, tile_type, pos_x, pos_y, z_index=0, lever_id=None):

        if not Tile.images_loaded:
            self.load_images()

        super().__init__(SpriteGroups.all_sprites, SpriteGroups.tiles_group)
        self.z_index = z_index
        self.image = Tile.sheet[tile_type - 1]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)

        self.tile_type = tile_type

        config = tile_config.get(tile_type, {})

        self.is_solid = config.get('isSolid', False)
        self.is_platform = config.get('isPlatform', False)

        self.lever_state = config.get('leverState', -1)
        self.is_lever = self.lever_state != -1
        self.lever_id = lever_id

        self.is_interactive = self.is_lever

        self.damage = config.get('damage', 0)
        self.is_trap = self.damage != 0

        if self.is_trap:
            self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def load_images():
        global tile_width, tile_height

        Tile.tile_images = load_image('tiles.png', (0, 0, 0))

        w, h = Tile.tile_images.get_size()
        multiplier = Tile.image_size_multiplier
        Tile.tile_images = pygame.transform.scale(Tile.tile_images,
                                                  (w * multiplier,
                                                   h * multiplier))
        tile_width *= multiplier
        tile_height *= multiplier

        Tile.sheet = cut_sheet(Tile.tile_images, *Tile.sheet_size)
        Tile.images_loaded = True

    @staticmethod
    def set_image_size_multiplier(multiplier):
        Tile.image_size_multiplier = multiplier
