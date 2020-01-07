import pygame
from configuration import *


class Attack(pygame.sprite.Sprite):
    def __init__(self, main, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.direction = direction
        self.speed = speed


class HeroDefaultAttack(Attack):
    def __init__(self, main, direction, x, y, speed):
        super().__init__(main, direction, speed)
        if direction == RIGHT:
            self.image = pygame.image.load('data/player/player_attack/trailr.png')
        else:
            self.image = pygame.image.load('data/player/player_attack/traill.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = 18
        self.y = 18
        self.damage = HERO_DA_DMG
        self.live = 7
        self.damaged = []

    def update(self):
        if self.direction == RIGHT:
            self.rect.y -= 3
            self.rect.x += self.speed
            self.x += 6
            self.y += 6
            self.image = pygame.transform.scale(self.image, (self.x, self.y))
        else:
            self.rect.y -= 3
            self.rect.x -= 6 + self.speed
            self.x += 6
            self.y += 6
            self.image = pygame.transform.scale(self.image, (self.x, self.y))
        self.live -= 1
        if self.live <= 0:
            self.kill()
        # self.collide()

    # def collide(self):
    #     for sprite in pygame.sprite.spritecollideany(self, all_sprites):
    #         if isinstance(sprite, MeleeEnemy):
    #             if sprite not in self.damaged:
    #                 sprite.hp -= HERO_DA_DMG
    #                 self.damaged.append(sprite)
    #     self.damaged.clear()


class HeroRangeAttack(Attack):
    def __init__(self, main, direction, x, y, speed):
        super().__init__(main, direction, speed)
        if direction == RIGHT:
            self.image = pygame.image.load('data/player/player_attack/daggerr.png')
        else:
            self.image = pygame.image.load('data/player/player_attack/daggerl.png')
        self.image = pygame.transform.scale(self.image, (24, 7))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = HERO_RA_DMG

    def update(self):
        if self.direction == RIGHT:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.x > WINDOW_WIDTH or self.rect.x < 0 - 24:  # 24 - длина изображения
            self.kill()
        # self.collide()

    # def collide(self):
    #     for sprite in pygame.sprite.spritecollideany(self, self.main.enemy_group):
    #         if isinstance(sprite, MeleeEnemy):
    #             sprite.hp -= HERO_RA_DMG
    #             self.kill()
    #          elif isinstance(sprite, ):  # если является твердым
    #              self.kill()
