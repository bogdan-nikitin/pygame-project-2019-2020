from Modules.Attacks import *
from Modules.Configuration import *
from Modules import SpriteGroups, Mapping
from Modules.Sprites import *
from Modules.General import *
import pygame
import typing

MOVE_SPEED = 3
JUMP_SPEED = 4.5
PLAYER_WIDTH = 22
PLAYER_HEIGHT = 24

MAX_HP = 100
MAX_STAMINA = 100
HP_REGEN = 1
STAMINA_REGEN = 4

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


class Player(GameSprite, ScalableSprite):

    def __init__(self, main, direction, pos_x, pos_y):
        x, y = Mapping.tile_width * pos_x, Mapping.tile_height * pos_y
        pygame.sprite.Sprite.__init__(self, SpriteGroups.characters_group,
                                      SpriteGroups.all_sprites)
        self.main = main
        self.direction = direction

        self.image: typing.Optional[pygame.Surface] = None
        self.temp_image: typing.Optional[pygame.Surface] = None

        self.anim_stay_right: typing.Optional[pyganim.PygAnimation] = None
        self.anim_stay_left: typing.Optional[pyganim.PygAnimation] = None

        self.anim_jump_right: typing.Optional[pyganim.PygAnimation] = None
        self.anim_jump_left: typing.Optional[pyganim.PygAnimation] = None

        self.anim_walk_right: typing.Optional[pyganim.PygAnimation] = None
        self.anim_walk_left: typing.Optional[pyganim.PygAnimation] = None

        self.anim_dead_left: typing.Optional[pyganim.PygAnimation] = None
        self.anim_dead_right: typing.Optional[pyganim.PygAnimation] = None

        self.rect: typing.Optional[pygame.rect.Rect]

        if not self.images_loaded:
            self.load_images()

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

    def load_images(self):
        self.image = pygame.image.load(IMAGE_PATH)
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image,
                                            (int(w * Player.scale_multiplier),
                                             int(h * Player.scale_multiplier)))
        self.temp_image = pygame.image.load(INITIALIZATION_PATH)
        w, h = self.temp_image.get_size()
        self.temp_image = pygame.transform.scale(self.temp_image,
                                                 (int(w *
                                                      Player.scale_multiplier),
                                                  int(h *
                                                      Player.scale_multiplier)))

        self.anim_stay_right = pyganim.PygAnimation(ANIMATION_STAY_RIGHT)
        self.anim_stay_left = pyganim.PygAnimation(ANIMATION_STAY_LEFT)

        self.anim_jump_right = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.anim_jump_left = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)

        self.anim_walk_right = make_animation(ANIMATION_RIGHT, ANIMATION_DELAY)
        self.anim_walk_left = make_animation(ANIMATION_LEFT, ANIMATION_DELAY)

        self.anim_dead_left = pyganim.PygAnimation(ANIMATION_DEAD_LEFT)
        self.anim_dead_right = pyganim.PygAnimation(ANIMATION_DEAD_RIGHT)

        animations = [self.anim_stay_right, self.anim_stay_left,
                      self.anim_jump_right, self.anim_jump_left,
                      self.anim_walk_right, self.anim_walk_left,
                      self.anim_dead_left, self.anim_dead_right]

        for animation in animations:
            animation.play()
            w, h = animation.getMaxSize()
            animation.scale((int(w * Player.scale_multiplier),
                             int(h * Player.scale_multiplier)))

        self.rect = self.image.get_rect()

        Player.images_loaded = True

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
                    HeroDefaultAttack(self.main, self.direction,
                                      self.x, self.y, speed))
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
                    HeroRangeAttack(self.main, self.direction, self.x + 4,
                                    self.y + 6, speed))
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
                self.temp_image.fill(color_key)
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
                    self.temp_image.fill(color_key)
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
                self.temp_image.fill(color_key)
                if self.direction == RIGHT:
                    self.anim_jump_right.blit(self.temp_image, (0, 0))
                else:
                    self.anim_jump_left.blit(self.temp_image, (0, 0))
                self.image = self.temp_image

    def update(self, *args):
        tick = args[0] if args else 0
        if self.hp <= 0:
            self.dead = True
        color_key = self.image.get_at((0, 0))
        if self.dead:
            if self.dead_count > 0:
                self.dead_count -= 1
                self.temp_image.fill(color_key)
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
                self.default_attack(color_key)
            elif self.is_range_attack:
                self.range_attack(color_key)
            self.move(color_key)
        else:
            self.stun_count -= 1
            if self.stun_count == 0:
                self.stunned = False

        self.y_v += GRAVITATION

        self.x += self.x_v  # * tick / 1000
        self.collide(self.x_v, 0)  # * tick / 1000, 0)
        self.y += self.y_v  # * tick / 1000
        self.collide(0, self.y_v)  # * tick / 1000)

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
                if not self.main.is_end:
                    self.main.end_game()
