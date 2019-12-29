from Constants import *
import os
import pygame


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
