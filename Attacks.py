import pygame
from configuration import *

HERO_DA_DMG = 35


class HeroDefaultAttack(pygame.sprite.Sprite):
    def __init__(self, direction, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        if direction == RIGHT:
            self.image = pygame.image.load('data/player/player_attack/trailr.png')
        else:
            self.image = pygame.image.load('data/player/player_attack/traill.png')
        self.direction = direction
        self.rect = pygame.Rect(x, y, 20, 30)  # противникам, касающимся данного прямоугольника, будет наносится урон
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = HERO_DA_DMG

    def update(self):
        if self.direction == RIGHT:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
