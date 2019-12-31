from Constants import *
import os
import pygame


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self._rect = None
        self.rect = self._rect
        self._x = 0
        self._y = 0
        self.x = self._x
        self.y = self._y

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value
        if self.rect is not None:
            self.x, self.y = self.rect.topleft

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if self.rect is not None:
            self.rect.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if self.rect is not None:
            self.rect.y = self._y

    def set_pos(self, x, y):
        self.x = x
        self.y = y


def load_image(name, color_key=None):
    """Загружает изображение data/name и устанавливает изображению цветовой ключ
     color_key. Если color_key=-1, то в качестве color_key используется верхний
     левый угол зображения."""
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def clear(screen):
    """Очищает экран screen, заливая его цветом Constants.BG_COLOR."""
    screen.fill(BG_COLOR)


def is_pressed(key):
    """Возвращает True или False, в зависимости от того, нажата ли клавиша key.
    Номера клавиш используются из библиотеки pygame"""
    return bool(pygame.key.get_pressed()[key])


def cut_sheet(sheet, columns, rows):
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames
