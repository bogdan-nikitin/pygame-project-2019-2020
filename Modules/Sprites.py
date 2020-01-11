from Modules.General import *
from Modules import SpriteGroups
import pygame
from collections.abc import Iterable


class GameSprite(pygame.sprite.Sprite):
    """Класс спрайта, имеющего свойства x и y - координаты. При изменении
    координаты также меняется значение topleft у свойства rect. При изменении
    свойства rect меняются координаты x и y. Координаты сохраняют дробные
    значения."""
    def __init__(self, *groups):
        super().__init__(SpriteGroups.all_sprites, *groups)
        self._rect = None
        self.rect = self._rect
        self._x = 0
        self._y = 0
        self.x = self._x
        self.y = self._y

    @property
    def rect(self):
        if self._rect:
            return self._rect.copy()

    @rect.setter
    def rect(self, value: pygame.rect.Rect):
        self._rect = value
        self.normalize_pos()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if self._rect is not None:
            self._rect.x = self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if self._rect is not None:
            self._rect.y = self._y

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    def normalize_pos(self):
        """Выставляет координатам x и y текущее положение спрайта."""
        if self._rect is not None:
            self._x, self._y = self._rect.topleft

    def collide_shift(self, shift_x, shift_y, groups=(),
                      key=lambda sprite: True, collided=None, move=True):
        self.collide_move(self._x + shift_x, self._y + shift_y, groups, key,
                          collided, move)

    def collide_move(self, x, y, groups=(), key=lambda sprite: True,
                     collided=None, move=True):
        if not isinstance(groups, Iterable):
            groups = (groups,)
        x_shift, y_shift = x - self._x, y - self._y
        steps = int(max(map(abs, (x_shift, y_shift))))
        if not steps:
            return False
        x_step = x_shift / steps
        y_step = y_shift / steps
        moving_sprite = GameSprite()
        moving_sprite._rect = self._rect
        for i in range(1, steps + 1):
            if i == steps:
                moving_sprite.x, moving_sprite.y = x, y
            else:
                moving_sprite.x += x_step
                moving_sprite.y += y_step
            for group in groups:
                if not isinstance(group, Iterable):
                    group = (group,)
                for sprite in group:
                    if (key(sprite) and ((collided and collided(self, sprite))
                                         or
                                         moving_sprite._rect.colliderect(
                                             sprite.rect))):
                        if move and i != 1:
                            self.x += x_step * (i - 1)
                            self.y += y_step * (i - 1)
                        return False
        if move:
            self.x = x
            self.y = y
        return True


class ScalableSprite(pygame.sprite.Sprite):
    scale_multiplier = 1
    images_loaded = False

    @classmethod
    def set_image_size_multiplier(cls, multiplier):
        cls.scale_multiplier = multiplier
        cls.images_loaded = False


