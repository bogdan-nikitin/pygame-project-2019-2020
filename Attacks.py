import pygame
from configuration import *


class HeroDefaultAttack(pygame.sprite.Sprite):
    def __init__(self, direction, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        if direction == RIGHT:
            self.image = pygame.image.load('data/player/player_attack/trailr.png')
        else:
            self.image = pygame.image.load('data/player/player_attack/traill.png')
        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = 18
        self.y = 18
        self.speed = speed
        self.damage = HERO_DA_DMG
        self.live = 7

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


class HeroRangeAttack(pygame.sprite.Sprite):
    def __init__(self, direction, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        if direction == RIGHT:
            self.image = pygame.image.load('data/player/player_attack/daggerr.png')
        else:
            self.image = pygame.image.load('data/player/player_attack/daggerl.png')
        self.image = pygame.transform.scale(self.image, (24, 7))
        self.direction = direction
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = HERO_RA_DMG

    def update(self):
        if self.direction == RIGHT:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.x > WINDOW_WIDTH or self.rect.x < 0 - 24:  # 24 - длина изображения
            self.kill()
