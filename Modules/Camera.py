"""Модуль для работы с камерой."""

from Modules.Enemies import *
from Modules.Sprites import *


class Camera:
    """Класс камеры."""
    # зададим начальный сдвиг камеры
    def __init__(self, screen):
        self.screen = screen
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if isinstance(obj, GameSprite):
            obj.x += self.dx
            obj.y += self.dy
            if isinstance(obj, MeleeEnemyWithMaxX):
                obj.start_x += self.dx
                obj.start_y += self.dy
        else:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        width, height = self.screen.get_rect().size
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
