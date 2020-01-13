"""Модуль для создания снарядов, по типу клинков, огненных шаров и т.п."""

from Modules.Mapping import *
from Modules.EnemiesHeaders import *
from Modules.Configuration import *
from Modules.General import *
from Modules import SpriteGroups

FIREBALL_SPEED = 5
TRAIL_DURATION = 7


class Attack(GameSprite):
    """Абастрактный класс атаки."""
    def __init__(self, main, direction, speed):
        pygame.sprite.Sprite.__init__(self, SpriteGroups.all_sprites)
        self.main = main
        self.direction = direction
        self.speed = speed


class HeroAttack(Attack):
    """Класс атаки героя."""
    def __init__(self, main, direction, speed):
        super().__init__(main, direction, speed)
        self.damaged = []

    def collide(self):
        """Проверяет столкновения снаряда с блоками и врагами."""
        for sprite in pygame.sprite.spritecollide(self,
                                                  SpriteGroups.all_sprites,
                                                  False):
            if isinstance(sprite, Tile):
                if sprite.is_solid:
                    self.kill()
            if isinstance(sprite, (MeleeEnemy, FireMage)):
                if sprite not in self.damaged:
                    sprite.hp -= HERO_DA_DMG
                    self.damaged.append(sprite)
                    self.kill()
        self.damaged.clear()


class HeroDefaultAttack(HeroAttack):
    """Ближняя атака игрока."""
    def __init__(self, main, direction, x, y, speed):
        super().__init__(main, direction, speed)
        if direction == RIGHT:
            self.image = pygame.image.load(data_path('player/player_attack/'
                                           'trailr.png'))
        else:
            self.image = pygame.image.load(data_path('player/player_attack/'
                                           'traill.png'))
        self.rect = self.image.get_rect()
        self.x = x + 4 * (1 if direction == RIGHT else -1)
        self.y = y
        self.damage = HERO_DA_DMG
        self.live = TRAIL_DURATION

    def update(self, *args):
        # tick = args[0] if args else 0
        multiplier = 1 if self.direction == RIGHT else -1
        self.x += self.speed * multiplier
        self.live -= 1
        if self.live <= 0:
            self.kill()
        self.collide()


class HeroRangeAttack(HeroAttack):
    """Дальняя атака игрока."""
    def __init__(self, main, direction, x, y, speed):
        super().__init__(main, direction, speed)
        if direction == RIGHT:
            self.image = pygame.image.load(data_path('player/player_attack/'
                                                     'daggerr.png'))
        else:
            self.image = pygame.image.load(data_path('player/player_attack/'
                                                     'daggerl.png'))
        self.image = pygame.transform.scale(self.image, (24, 7))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.damage = HERO_RA_DMG

    def update(self, *args):
        if self.direction == RIGHT:
            self.x += self.speed
        else:
            self.x -= self.speed
            # 24 - длина изображения
        if self.x > WINDOW_WIDTH or self.x < 0 - 24:
            self.kill()
        self.collide()


# Классы ниже не доделаны, в проекте не используются

# class Fireball(pygame.sprite.Sprite):
#     def __init__(self, direction, start_x, start_y, target_x, target_y):
#         super().__init__()
#         if direction == RIGHT:
#             self.image = pygame.image.load(data_path
#             ('projectives/fballr.png'))
#         else:
#             self.image = pygame.image.load(data_path
#              ('projectives/fballl.png'))
#         self.rect = self.image.get_rect()
#         self.rect.x = start_x
#         self.rect.y = start_y
#         self.floating_point_x = start_x
#         self.floating_point_y = start_y
#
#         x_diff = target_x - start_x
#         y_diff = target_y - start_y
#         angle = math.atan2(y_diff, x_diff)
#
#         speed = FIREBALL_SPEED
#         self.change_x = math.cos(angle) * speed
#         self.change_y = math.sin(angle) * speed
#
#     def update(self, *args):
#         self.floating_point_y += self.change_y
#         self.floating_point_x += self.change_x
#         self.rect.y = int(self.floating_point_y)
#         self.rect.x = int(self.floating_point_x)
#
#         if (self.rect.x < 0 or self.rect.x > WINDOW_WIDTH or
#                 self.rect.y < 0 or self.rect.y > WINDOW_HEIGHT):
#             self.kill()
#
#     # def collide(self):
#     #     for sprite in pygame.sprite.spritecollideany(self, all_sprites):
#     #         if isinstance(sprite, PLayer):
#     #             sprite.hp -= FIREBALL_DMG
#     #             self.kill()
#     #          elif isinstance(sprite, ):  # если является твердым
#     #              self.kill()
#
#
# class AimedFireball(pygame.sprite.Sprite):
#     def __init__(self, target, start_x, start_y):
#         super().__init__()
#         self.image = pygame.image.load(data_path('projectives/aimedfb.png'))
#         self.rect = self.image.get_rect()
#         self.rect.x = start_x
#         self.rect.y = start_y
#         self.floating_point_x = start_x
#         self.floating_point_y = start_y
#         self.speed = FIREBALL_SPEED
#         self.target = target
#         self.aiming = True
#
#         x_diff = self.target.rect.x - start_x
#         y_diff = self.target.rect.y - start_y
#         angle = math.atan2(y_diff, x_diff)
#         self.prev_angle = angle
#
#         self.change_x = math.cos(angle) * self.speed
#         self.change_y = math.sin(angle) * self.speed
#
#     def update(self, *args):
#         self.floating_point_y += self.change_y
#         self.floating_point_x += self.change_x
#         self.rect.y = int(self.floating_point_y)
#         self.rect.x = int(self.floating_point_x)
#
#         if self.aiming:
#             x_diff = self.target.rect.x - self.rect.x
#             y_diff = self.target.rect.y - self.rect.y
#             angle = math.atan2(y_diff, x_diff)
#             self.prev_angle = angle
#             if abs(self.rect.x - self.target.rect.x) <= 10:
#                 self.aiming = False
#             self.change_x = math.cos(angle) * self.speed
#             self.change_y = math.sin(angle) * self.speed
#         else:
#             self.change_x = math.cos(self.prev_angle) * self.speed
#             self.change_y = math.sin(self.prev_angle) * self.speed
#
#         if (self.rect.x < 0 or self.rect.x > WINDOW_WIDTH or
#                 self.rect.y < 0 or self.rect.y > WINDOW_HEIGHT):
#             self.kill()
#
#     # def collide(self):
#     #     for sprite in pygame.sprite.spritecollideany(self, all_sprites):
#     #         if isinstance(sprite, PLayer):
#     #             sprite.hp -= AIMEDFB_DMG
#     #             self.kill()
#     #          elif isinstance(sprite, ):  # если является твердым
#     #              self.kill()
