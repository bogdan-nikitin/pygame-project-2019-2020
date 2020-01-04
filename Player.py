import pygame
import pyganim
from configuration import *
from Attacks import HeroDefaultAttack

MOVE_SPEED = 2
JUMP_SPEED = 5
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 24
GRAVITATION = 0.1

ANIMATION_DELAY = 100

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

ANIMATION_JUMP_LEFT = [('data/player/player_jump/jumpl.png', ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('data/player/player_jump/jumpr.png', ANIMATION_DELAY)]
ANIMATION_STAY_RIGHT = [('data/player/player_stay/stayr.png', ANIMATION_DELAY)]
ANIMATION_STAY_LEFT = [('data/player/player_stay/stayl.png', ANIMATION_DELAY)]


def make_animation(animation_list, delay):
    animation = []
    for elem in animation_list:
        animation.append((elem, delay))
    result = pyganim.PygAnimation(animation)
    return result


class Player(pygame.sprite.Sprite):
    def __init__(self, main, direction, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.screen = screen
        self.direction = direction
        self.image = pygame.image.load('data/player/player_stay/stayr.png')
        self.temp_image = pygame.image.load('data/player/initialization.png')
        self.start_x = x
        self.start_y = y
        self.x_v = 0
        self.y_v = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.up = self.left = self.right = False
        self.dead = False
        self.on_ground = False
        self.is_default_attack = False
        self.attack_count = 0
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
        if self.attack_count < 60:
            self.attack_count += 1
            if self.attack_count == 38:
                if not (self.left or self.right):
                    speed = 1
                else:
                    speed = 3
                self.main.hero_melee_attacks.add(
                    HeroDefaultAttack(self.direction, self.rect.x + 10, self.rect.y + 5, speed))
            if self.attack_count <= 40:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DMR[0], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DML[0], (0, 0))
                self.image = self.temp_image
            elif self.attack_count > 40:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DMR[1], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DML[1], (0, 0))
                self.image = self.temp_image
        else:
            self.attack_count = 0
            self.is_default_attack = False

    def move(self, color_key):
        if self.left:
            self.x_v = -MOVE_SPEED
            if not self.is_default_attack:
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
            if not self.is_default_attack:
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
            if not self.is_default_attack:
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
            if not self.is_default_attack:
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.anim_jump_right.blit(self.temp_image, (0, 0))
                else:
                    self.anim_jump_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image

    def update(self, solid_blocks):
        color_key = self.image.get_at((0, 0))
        if self.is_default_attack:
            self.default_attack(color_key)
        self.move(color_key)

        if not self.on_ground:
            self.y_v += GRAVITATION

        self.on_ground = False
        self.rect.x += self.x_v
        self.collide(self.x_v, 0, solid_blocks)
        self.rect.y += self.y_v
        self.collide(0, self.y_v, solid_blocks)

    def collide(self, x_v, y_v, solid_blocks):
        for block in solid_blocks:  # для твердых блоков
            if pygame.sprite.collide_rect(self, block):
                if x_v > 0:
                    self.rect.right = block.rect.left
                if x_v < 0:
                    self.rect.left = block.rect.right
                if y_v > 0:
                    self.rect.bottom = block.rect.top
                    self.on_ground = True
                    self.y_v = 0
                if y_v < 0:
                    self.rect.top = block.rect.bottom
                    self.y_v = 0
