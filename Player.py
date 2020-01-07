import pygame

from Attacks import HeroRangeAttack, HeroDefaultAttack
from configuration import *

MOVE_SPEED = 4
JUMP_SPEED = 10
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 24

MAX_HP = 100
MAX_STAMINA = 100
HP_REGEN = 1
STAMINA_REGEN = 4

ANIMATION_RIGHT = ['data/player/player_walk/walkr1.png',
                   'data/player/player_walk/walkr2.png',
                   'data/player/player_walk/walkr3.png',
                   'data/player/player_walk/walkr4.png', ]
ANIMATION_LEFT = ['data/player/player_walk/walkl1.png',
                  'data/player/player_walk/walkl2.png',
                  'data/player/player_walk/walkl3.png',
                  'data/player/player_walk/walkl4.png', ]

ANIMATION_ATTACK_DMR = [pygame.image.load('data/player/player_attack/mr1.png'),
                        pygame.image.load('data/player/player_attack/mr2.png'), ]
ANIMATION_ATTACK_DML = [pygame.image.load('data/player/player_attack/ml1.png'),
                        pygame.image.load('data/player/player_attack/ml2.png'), ]
ANIMATION_ATTACK_DRR = [pygame.image.load('data/player/player_attack/rr1.png'),
                        pygame.image.load('data/player/player_attack/rr2.png'), ]
ANIMATION_ATTACK_DRL = [pygame.image.load('data/player/player_attack/rl1.png'),
                        pygame.image.load('data/player/player_attack/rl2.png'), ]

ANIMATION_JUMP_LEFT = [('data/player/player_jump/jumpl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('data/player/player_jump/jumpr.png', ANIMATION_DELAY)]
ANIMATION_STAY_RIGHT = [('data/player/player_stay/stayr.png', ANIMATION_DELAY)]
ANIMATION_STAY_LEFT = [('data/player/player_stay/stayl.png', ANIMATION_DELAY)]


class Player(pygame.sprite.Sprite):
    def __init__(self, main, direction, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.direction = direction
        self.image = pygame.image.load('data/player/player_stay/stayr.png')
        self.temp_image = pygame.image.load('data/initialization.png')
        self.start_x = x
        self.start_y = y
        self.x_v = 0
        self.y_v = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hero_melee_attacks = pygame.sprite.Group()
        self.hero_range_attacks = pygame.sprite.Group()
        self.up = self.left = self.right = False
        self.dead = False
        self.on_ground = False
        self.is_default_attack = False
        self.is_range_attack = False
        self.stunned = False
        self.stun_count = 0
        self.da_count = 0
        self.ra_count = 0
        self.hp = MAX_HP
        self.stamina = MAX_STAMINA

        self.anim_stay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.anim_stay_right.play()

        self.anim_stay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)
        self.anim_stay_left.play()

        self.anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.anim_jump_right.play()

        self.anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.anim_jump_left.play()

        self.anim_walk_right = make_animation(ANIMATION_RIGHT, ANIMATION_DELAY)
        self.anim_walk_right.play()

        self.anim_walk_left = make_animation(ANIMATION_LEFT, ANIMATION_DELAY)
        self.anim_walk_left.play()

    def tick(self):
        if self.hp < MAX_HP:
            self.hp += HP_REGEN
        if self.stamina < MAX_STAMINA:
            self.stamina += STAMINA_REGEN

    def default_attack(self, color_key):
        if self.da_count < 30:
            self.da_count += 1
            if self.da_count == 18:
                if not (self.left or self.right):
                    speed = 2
                else:
                    speed = 7
                self.hero_melee_attacks.add(
                    HeroDefaultAttack(self.main, self.direction, self.rect.x + 4, self.rect.y, speed))
            if self.da_count <= 20:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DMR[0], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DML[0], (0, 0))
                self.image = self.temp_image
            elif self.da_count > 20:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DMR[1], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DML[1], (0, 0))
                self.image = self.temp_image
        else:
            self.da_count = 0
            self.is_default_attack = False

    def range_attack(self, color_key):
        if self.ra_count < 45:
            self.ra_count += 1
            if self.ra_count == 22:
                if not (self.left or self.right):
                    speed = 10
                else:
                    speed = 17
                self.hero_range_attacks.add(
                    HeroRangeAttack(self.main, self.direction, self.rect.x + 4, self.rect.y + 6, speed))
            if self.ra_count <= 25:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DRR[0], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DRL[0], (0, 0))
                self.image = self.temp_image
            elif self.ra_count > 25:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DRR[1], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DRL[1], (0, 0))
                self.image = self.temp_image
        else:
            self.ra_count = 0
            self.is_range_attack = False

    def move(self, color_key):
        if self.left:
            self.x_v = -MOVE_SPEED
            if not (self.is_default_attack or self.is_range_attack):
                self.temp_image.fill(color_key)
                if not self.up:
                    self.anim_walk_left.blit(self.temp_image, (0, 0))
                else:
                    if self.direction == RIGHT:
                        self.anim_jump_right.blit(self.temp_image, (0, 0))
                    else:
                        self.anim_jump_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image
        if self.right:
            self.x_v = MOVE_SPEED
            if not (self.is_default_attack or self.is_range_attack):
                self.temp_image.fill(color_key)
                if not self.up:
                    self.anim_walk_right.blit(self.temp_image, (0, 0))
                else:
                    if self.direction == RIGHT:
                        self.anim_jump_right.blit(self.temp_image, (0, 0))
                    else:
                        self.anim_jump_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image
        if not (self.left or self.right):
            self.x_v = 0
            if not (self.is_default_attack or self.is_range_attack):
                if self.on_ground:
                    self.temp_image.fill(color_key)
                    if self.direction == RIGHT:
                        self.anim_stay_right.blit(self.temp_image, (0, 0))
                    else:
                        self.anim_stay_left.blit(self.temp_image, (0, 0))
                    self.image = self.temp_image
        if self.up:
            if self.on_ground:
                self.y_v = -JUMP_SPEED
            if not (self.is_default_attack or self.is_range_attack):
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.anim_jump_right.blit(self.temp_image, (0, 0))
                else:
                    self.anim_jump_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image

    def update(self):
        if self.hp <= 0:
            self.dead = True
        color_key = self.image.get_at((0, 0))
        if not self.stunned:
            if self.is_default_attack:
                self.default_attack(color_key)
            elif self.is_range_attack:
                self.range_attack(color_key)
            self.move(color_key)
        else:
            self.stun_count -= 1
            if self.stun_count == 0:
                self.stunned = False

        if not self.on_ground:
            self.y_v += GRAVITATION

        self.on_ground = False
        self.rect.x += self.x_v
        # self.collide(self.x_v, 0)
        self.rect.y += self.y_v
        # self.collide(0, self.y_v)

    # def collide(self, x_v, y_v):
    #     for sprite in pygame.sprite.spritecollideany(self, all_sprites):
    #         if isinstance(sprite, ):  # если является твердым
    #             if x_v > 0:
    #                 self.rect.right = sprite.rect.left
    #             if x_v < 0:
    #                 self.rect.left = sprite.rect.right
    #             if y_v > 0:
    #                 self.rect.bottom = sprite.rect.top
    #                 self.on_ground = True
    #                 self.y_v = 0
    #             if y_v < 0:
    #                 self.rect.top = sprite.rect.bottom
    #                 self.y_v = 0
