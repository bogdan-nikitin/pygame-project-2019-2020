"""Содержит класс игрока."""

from Modules.Attacks import *
from Modules.Configuration import *
from Modules import SpriteGroups, Mapping
from Modules.Sprites import *
from Modules.General import *
import pygame

MOVE_SPEED = 3
JUMP_SPEED = 4.5
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 24

# DA - Default attack
DA_COUNT = 20
DA_ANIMATION_CHANGE = 20
DA_ATTACK_SPAWN = 18
DA_SPEED = 2
DA_INCREASED_SPEED = 5

# RA - Range attack
RA_COUNT = 25
RA_ANIMATION_CHANGE = 25
RA_ATTACK_SPAWN = 22
RA_SPEED = 7
RA_INCREASED_SPEED = 10

MAX_HP = 100
MAX_STAMINA = 100
HP_REGEN = 1
STAMINA_REGEN = 8

ANIMATION_RIGHT = [data_path('player/player_walk/walkr1.png'),
                   data_path('player/player_walk/walkr2.png'),
                   data_path('player/player_walk/walkr3.png'),
                   data_path('player/player_walk/walkr4.png'), ]
ANIMATION_LEFT = [data_path('player/player_walk/walkl1.png'),
                  data_path('player/player_walk/walkl2.png'),
                  data_path('player/player_walk/walkl3.png'),
                  data_path('player/player_walk/walkl4.png'), ]

ANIMATION_ATTACK_DMR = [
    pygame.image.load(data_path('player/player_attack/mr1.png')),
    pygame.image.load(data_path('player/player_attack/mr2.png')),
                        ]
ANIMATION_ATTACK_DML = [
    pygame.image.load(data_path('player/player_attack/ml1.png')),
    pygame.image.load(data_path('player/player_attack/ml2.png')),
                        ]
ANIMATION_ATTACK_DRR = [
    pygame.image.load(data_path('player/player_attack/rr1.png')),
    pygame.image.load(data_path('player/player_attack/rr2.png')),
                        ]
ANIMATION_ATTACK_DRL = [
    pygame.image.load(data_path('player/player_attack/rl1.png')),
    pygame.image.load(data_path('player/player_attack/rl2.png')),
                        ]

ANIMATION_JUMP_LEFT = [(data_path('player/player_jump/jumpl.png'),
                        ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [(data_path('player/player_jump/jumpr.png'),
                         ANIMATION_DELAY)]
ANIMATION_STAY_RIGHT = [(data_path('player/player_stay/stayr.png'),
                         ANIMATION_DELAY)]
ANIMATION_STAY_LEFT = [(data_path('player/player_stay/stayl.png'),
                        ANIMATION_DELAY)]

ANIMATION_DEAD_LEFT = [(data_path('player/player_dead/deadl.png'),
                        ANIMATION_DELAY)]
ANIMATION_DEAD_RIGHT = [(data_path('player/player_dead/deadr.png'),
                        ANIMATION_DELAY)]
IMAGE_PATH = data_path('player/player_stay/stayr.png')
INITIALIZATION_PATH = data_path('initialization.png')


class Player(GameSprite, AnimatedSprite):

    def __init__(self, main, direction, pos_x, pos_y):
        x, y = Mapping.tile_width * pos_x, Mapping.tile_height * pos_y
        super().__init__(SpriteGroups.characters_group)
        self.main = main
        self.direction = direction

        if not type(self).images_loaded:
            self.load_images(type(self))

        self.start_x = x
        self.start_y = y
        self.x_v = 0
        self.y_v = 0
        self.x = x
        self.y = y
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

        # Кол-во кадров до исчезновения трупа
        self.dead_count = PLAYER_DEAD_COUNT

    def load_images(self, cls):
        self.image = pygame.image.load(IMAGE_PATH)

        self.temp_image = pygame.image.load(INITIALIZATION_PATH)

        self.anim_stay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.anim_stay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)

        self.anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)

        self.anim_walk_right = make_animation(ANIMATION_RIGHT, ANIMATION_DELAY)
        self.anim_walk_left = make_animation(ANIMATION_LEFT, ANIMATION_DELAY)

        self.anim_dead_left = pyganim.PygAnimation(ANIMATION_DEAD_LEFT)
        self.anim_dead_right = pyganim.PygAnimation(ANIMATION_DEAD_RIGHT)

        super().load_images(cls)

    def tick(self):
        if self.hp < MAX_HP:
            self.hp += HP_REGEN
        if self.stamina < MAX_STAMINA:
            self.stamina += STAMINA_REGEN
        if self.stamina > MAX_STAMINA:
            self.stamina = MAX_STAMINA

    def default_attack(self):
        if self.da_count < DA_COUNT:
            self.da_count += 1
            if self.da_count == DA_ATTACK_SPAWN:
                if not (self.left or self.right):
                    speed = DA_SPEED
                else:
                    speed = DA_INCREASED_SPEED
                self.hero_melee_attacks.add(
                    HeroDefaultAttack(self.main, self.direction,
                                      self.x, self.y, speed))
            if self.da_count <= DA_ANIMATION_CHANGE:
                self.temp_image.fill(TRANSPARENT)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DMR[0], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DML[0], (0, 0))
                self.image = self.temp_image
            elif self.da_count > DA_ANIMATION_CHANGE:
                self.temp_image.fill(TRANSPARENT)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DMR[1], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DML[1], (0, 0))
                self.image = self.temp_image
        else:
            self.da_count = 0
            self.is_default_attack = False

    def range_attack(self):
        if self.ra_count < RA_COUNT:
            self.ra_count += 1
            if self.ra_count == RA_ATTACK_SPAWN:
                if not (self.left or self.right):
                    speed = RA_SPEED
                else:
                    speed = RA_INCREASED_SPEED
                self.hero_range_attacks.add(
                    HeroRangeAttack(self.main, self.direction, self.x + 4,
                                    self.y + 6, speed))
            if self.ra_count <= RA_ANIMATION_CHANGE:
                self.temp_image.fill(TRANSPARENT)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DRR[0], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DRL[0], (0, 0))
                self.image = self.temp_image
            elif self.ra_count > RA_ANIMATION_CHANGE:
                self.temp_image.fill(TRANSPARENT)
                if self.direction == RIGHT:
                    self.temp_image.blit(ANIMATION_ATTACK_DRR[1], (0, 0))
                else:
                    self.temp_image.blit(ANIMATION_ATTACK_DRL[1], (0, 0))
                self.image = self.temp_image
        else:
            self.ra_count = 0
            self.is_range_attack = False

    def move(self):
        if self.left:
            self.x_v = -MOVE_SPEED
            if not (self.is_default_attack or self.is_range_attack):
                self.temp_image.fill(TRANSPARENT)
                if self.on_ground:
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
                self.temp_image.fill(TRANSPARENT)
                if self.on_ground:
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
                    self.temp_image.fill(TRANSPARENT)
                    if self.direction == RIGHT:
                        self.anim_stay_right.blit(self.temp_image, (0, 0))
                    else:
                        self.anim_stay_left.blit(self.temp_image, (0, 0))
                    self.image = self.temp_image
        if self.up:
            if self.on_ground:
                self.y_v = -JUMP_SPEED
                self.on_ground = False
            if not (self.is_default_attack or self.is_range_attack):
                self.temp_image.fill(TRANSPARENT)
                if self.direction == RIGHT:
                    self.anim_jump_right.blit(self.temp_image, (0, 0))
                else:
                    self.anim_jump_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image

    def update(self, *args):
        # tick = args[0] if args else 0
        if self.hp <= 0:
            self.dead = True
        if self.dead:
            if self.dead_count > 0:
                self.dead_count -= 1
                self.temp_image.fill(TRANSPARENT)
                self.x_v = 0
                if self.direction == RIGHT:
                    self.anim_dead_right.blit(self.temp_image, (0, 0))
                else:
                    self.anim_dead_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image
            else:
                self.kill()
                self.main.end_game(YOU_DIED_MESSAGE, False)
        elif not self.stunned:
            if self.is_default_attack:
                self.default_attack()
            elif self.is_range_attack:
                self.range_attack()
            self.move()
        else:
            self.stun_count -= 1
            if self.stun_count == 0:
                self.stunned = False

        self.y_v += GRAVITATION

        self.x += self.x_v
        self.collide(self.x_v, 0)
        self.y += self.y_v
        self.collide(0, self.y_v)

    def collide(self, x_v, y_v):
        for sprite in pygame.sprite.spritecollide(self,
                                                  SpriteGroups.tiles_group,
                                                  False):
            if sprite.is_solid:  # если является твердым
                clip = self.rect.clip(sprite.rect)
                if x_v > 0:
                    self.x -= clip.w
                elif x_v < 0:
                    self.x += clip.w
                if y_v > 0:
                    self.y -= clip.h
                    self.on_ground = True
                    self.y_v = 0
                elif y_v < 0:
                    self.y += clip.h
            elif sprite.is_exit and self.up:
                self.main.load_next_level()
                return

    def kill(self):
        Player.images_loaded = False
        super().kill()
