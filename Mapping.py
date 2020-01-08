from General import *
import pygame
import json
import csv
import SpriteGroups
import os


TILE_CONFIG_FILE = 'tile_config.json'
tile_width = tile_height = 16


def load_tile_config():
    """Загружает конфигурацию всех плиток из файла DATA_PATH/TILE_CONFIG_FILE.
    """
    global tile_config

    with open(data_path(TILE_CONFIG_FILE)) as file:
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
    """Загружает уровень по пути DATA_PATH/filename."""
    filename = data_path(filename)
    with open(filename, 'r') as mapFile:
        reader = csv.reader(mapFile, delimiter=';', quotechar='"')
        return [row for row in reader]


def generate_level(level):
    """Генерирует уровень, возвращая его размер и словарь плиток, где ключами
    являются их координаты."""
    x, y = None, None
    tiles = {}
    for y in range(len(level)):
        for x in range(len(level[y])):
            tiles[(y, x)] = []
            for i, current_tile in enumerate(level[y][x].split(',')):
                if current_tile:
                    is_active = '*' not in current_tile
                    is_exit = '#' in current_tile
                    current_tile = current_tile.replace('#', '')
                    current_tile = current_tile.replace('*', '')
                    if ':' in current_tile:
                        tile_type, lever_id = map(int, current_tile.split(':'))
                    else:
                        tile_type, lever_id = int(current_tile), None
                    tiles[(y, x)] += [Tile(tile_type, x, y, i, lever_id,
                                           is_exit, is_active)]
    return x + 1, max(map(len, level)), tiles


tile_config = {}
load_tile_config()


class Tile(GameSprite):
    """Класс плитки - основной единицы карты уровня."""

    images_loaded = False
    tile_images = None
    sheet = None
    sheet_size = 20, 16
    image_size_multiplier = 1

    def __init__(self, tile_type, pos_x, pos_y, z_index=0, lever_id=None,
                 is_exit=False, is_active=True):

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
        if self.lever_state == 0:
            active_lever_tile = config.get('activeLeverTile', None)
            inactive_lever_tile = self.tile_type
        elif self.lever_state == 1:
            active_lever_tile = self.tile_type
            inactive_lever_tile = config.get('inactiveLeverTile', None)
        else:
            active_lever_tile, inactive_lever_tile = [None] * 2

        self.lever_tiles = [inactive_lever_tile, active_lever_tile]

        self.is_interactive = self.is_lever

        self.damage = config.get('damage', 0)
        self.is_trap = self.damage != 0

        animation = [self.tile_type] + config.get('animation', [0])
        self.animation_frames = animation[::2]
        self.animation_delays = animation[1::2]
        self.time_passed = 0
        self.current_frame = 0

        self.is_exit = is_exit

        self.is_active = is_active

        if self.is_trap:
            self.mask = pygame.mask.from_surface(self.image)

    @staticmethod
    def load_images():
        """Загружает текстуры для плиток, увеличивая их в Tile.multiplier раз.
        """

        Tile.tile_images = load_image('tiles.png', (0, 0, 0))

        w, h = Tile.tile_images.get_size()
        multiplier = Tile.image_size_multiplier
        tile_images = pygame.transform.scale(Tile.tile_images,
                                             (w * multiplier,
                                              h * multiplier))

        Tile.sheet = cut_sheet(tile_images, *Tile.sheet_size)
        Tile.images_loaded = True

    @staticmethod
    def set_image_size_multiplier(multiplier):
        """Устанавливает множитель размера для текстур."""
        global tile_width, tile_height
        Tile.image_size_multiplier = multiplier
        tile_width *= multiplier
        tile_height *= multiplier
        Tile.images_loaded = False

    def update(self, *args):
        """Обновляет спрайты. В качестве аргумента необходимо передать
        количество миллисекунд, прошедших с предыдущего обновления."""
        animation_len = len(self.animation_frames)
        if animation_len > 1 and len(args) > 0:
            self.time_passed += args[0] / 1000
            delay = self.animation_delays[self.current_frame]
            while delay - self.time_passed <= 0:
                self.current_frame = (self.current_frame + 1) % animation_len
                self.time_passed -= delay
                tile_type = self.animation_frames[self.current_frame]
                self.image = Tile.sheet[tile_type - 1]

    def interact(self):
        """Взаимодействие со спрайтом. Если спрайт является рычагом, то его
        состояние переключается, а активность всех спрайтов с тем же lever_id
        инвертируется, т.е. при нажатии на рычаг все включенные спрайты
        отключаются, а все выключенные - включаются."""
        if self.is_lever:
            self.lever_state = (self.lever_state + 1) % 2
            tile_type = self.lever_tiles[self.lever_state]
            if tile_type:
                self.image = Tile.sheet[tile_type - 1]
            for sprite in SpriteGroups.tiles_group:
                if sprite.lever_id == self.lever_id and not sprite.is_lever:
                    sprite.is_active = not sprite.is_active
