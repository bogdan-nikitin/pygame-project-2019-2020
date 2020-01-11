from Modules.Constants import *
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


def load_image(name, color_key=None):
    """Загружает изображение data/name и устанавливает изображению цветовой ключ
     color_key. Если color_key=-1, то в качестве color_key используется верхний
     левый угол зображения."""
    fullname = data_path(name)
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
