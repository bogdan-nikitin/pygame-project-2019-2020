from Constants import *
import os
import pygame
import re


DATA_PATH = 'data'


def draw_fps(screen, fps):
    font = pygame.font.Font(None, 30)
    text = font.render(str(int(fps)), 1, pygame.Color('yellow'))
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))


class GameSprite(pygame.sprite.Sprite):
    """Класс спрайта, имеющего свойства x и y - координаты. При изменении
    координаты также меняется значение topleft у свойства rect. При изменении
    свойства rect меняются координаты x и y. Координаты сохраняют дробные
    значения."""
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
        self.normalize_pos()

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

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    def normalize_pos(self):
        """Выставляет координатам x и y текущее положение спрайта."""
        if self.rect is not None:
            self.x, self.y = self.rect.topleft


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
    """Разрезает sheet на columns*rows частей."""
    frames = []
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                       sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


def data_path(path):
    """Возвращает путь к ресурсу, добавляя DATA_PATH к path."""
    return os.path.join(DATA_PATH, path)


def split_without_quotes(string, splitter=r'\s', quotes=r'[^\\][\'"]'):
    """Разделяет строку, подобно методу str.split, только при этом если
    разделитель splitter находится внутри кавычек quotes, то разделение не
    происходит. В качестве разделителя и кавычек могут выступать регулярные
    выражения. По умолчанию разделяет строку по пробельным символам, учитывая
    двойные и однинарные кавычки."""
    last_index = 0
    strings = []
    in_quotes = False
    for i in range(len(string)):
        splitter_match = re.match(splitter, string[i:])
        if splitter_match and not in_quotes:
            strings += [string[last_index:i]]
            last_index = i + splitter_match.end()
            continue
        quotes_match = re.match(quotes, string[i:])
        if quotes_match:
            in_quotes = not in_quotes
    if last_index <= len(string):
        strings += [string[last_index:]]
    return strings
