import pygame
from Modules.Player import *
from Modules.Attacks import *
from Modules.Configuration import *
from Modules.EnemiesHeaders import *
from Modules import Mapping
from Modules.ColorPalette import *

DEAD_COUNT = 60

INSECT_DMG = 20
INSECT_IMPULSE = 4
INSECT_MAX_HP = 35
INSECT_MS = 3
INSECT_STUN_POWER = 20

KNIGHT_DMG = 40
KNIGHT_IMPULSE = 5
KNIGHT_MAX_HP = 80
KNIGHT_MS = 3
KNIGHT_STUN_POWER = 30

RAT_DMG = 35
RAT_IMPULSE = 4
RAT_MAX_HP = 40
RAT_MS = 3
RAT_STUN_POWER = 25

SNAKE_DMG = 20
SNAKE_IMPULSE = 4
SNAKE_MAX_HP = 65
SNAKE_MS = 3
SNAKE_STUN_POWER = 15

BAT_DMG = 15
BAT_IMPULSE = 3
BAT_MAX_HP = 20
BAT_MS = 3
BAT_YV = 1
BAT_STAN_POWER = 10

FIREMAGE_HP = 120
FIREMAGE_MP = 100
FIREMAGE_MP_REG = 10

WRAITH_HP = 500
WRAITH_MP = 100
WRAITH_MP_REG = 10

INSECT_RIGHT = [data_path('enemies/insect/walkr1.png'),
                data_path('enemies/insect/walkr2.png'),
                data_path('enemies/insect/walkr3.png'),
                data_path('enemies/insect/walkr4.png'), ]
INSECT_LEFT = [data_path('enemies/insect/walkl1.png'),
               data_path('enemies/insect/walkl2.png'),
               data_path('enemies/insect/walkl3.png'),
               data_path('enemies/insect/walkl4.png'), ]
INSECT_STAY_RIGHT = [(data_path('enemies/insect/stayr.png'), ANIMATION_DELAY)]
INSECT_STAY_LEFT = [(data_path('enemies/insect/stayl.png'), ANIMATION_DELAY)]
INSECT_DEAD_RIGHT = [(data_path('enemies/insect/deadr.png'), ANIMATION_DELAY)]
INSECT_DEAD_LEFT = [(data_path('enemies/insect/deadl.png'), ANIMATION_DELAY)]

KNIGHT_RIGHT = [data_path('enemies/knight/walkr1.png'),
                data_path('enemies/knight/walkr2.png'), ]
KNIGHT_LEFT = [data_path('enemies/knight/walkl1.png'),
               data_path('enemies/knight/walkl2.png'), ]
KNIGHT_STAY_RIGHT = [(data_path('enemies/knight/stayr.png'), ANIMATION_DELAY)]
KNIGHT_STAY_LEFT = [(data_path('enemies/knight/stayl.png'), ANIMATION_DELAY)]
KNIGHT_DEAD_RIGHT = [(data_path('enemies/knight/deadr.png'), ANIMATION_DELAY)]
KNIGHT_DEAD_LEFT = [(data_path('enemies/knight/deadl.png'), ANIMATION_DELAY)]

RAT_RIGHT = [data_path('enemies/rat/walkr1.png'),
             data_path('enemies/rat/walkr2.png'),
             data_path('enemies/rat/walkr3.png'), ]
RAT_LEFT = [data_path('enemies/rat/walkl1.png'),
            data_path('enemies/rat/walkl2.png'),
            data_path('enemies/rat/walkl3.png'), ]
RAT_STAY_RIGHT = [(data_path('enemies/rat/stayr.png'), ANIMATION_DELAY)]
RAT_STAY_LEFT = [(data_path('enemies/rat/stayl.png'), ANIMATION_DELAY)]
RAT_DEAD_RIGHT = [(data_path('enemies/rat/deadr.png'), ANIMATION_DELAY)]
RAT_DEAD_LEFT = [(data_path('enemies/rat/deadl.png'), ANIMATION_DELAY)]

SNAKE_RIGHT = [data_path('enemies/snake/walkr1.png'),
               data_path('enemies/snake/walkr2.png'),
               data_path('enemies/snake/walkr3.png'), ]
SNAKE_LEFT = [data_path('enemies/snake/walkl1.png'),
              data_path('enemies/snake/walkl2.png'),
              data_path('enemies/snake/walkl3.png'), ]
SNAKE_STAY_RIGHT = [(data_path('enemies/snake/stayr.png'), ANIMATION_DELAY)]
SNAKE_STAY_LEFT = [(data_path('enemies/snake/stayl.png'), ANIMATION_DELAY)]
SNAKE_DEAD_RIGHT = [(data_path('enemies/snake/deadr.png'), ANIMATION_DELAY)]
SNAKE_DEAD_LEFT = [(data_path('enemies/snake/deadl.png'), ANIMATION_DELAY)]

BAT_RIGHT = [data_path('enemies/bat/walkr1.png'),
             data_path('enemies/bat/walkr2.png'),
             data_path('enemies/bat/walkr3.png'),
             data_path('enemies/bat/walkr4.png'), ]
BAT_LEFT = [data_path('enemies/bat/walkl1.png'),
            data_path('enemies/bat/walkl2.png'),
            data_path('enemies/bat/walkl3.png'),
            data_path('enemies/bat/walkl4.png'), ]
BAT_STAY_RIGHT = [(data_path('enemies/bat/stayr.png'), ANIMATION_DELAY)]
BAT_STAY_LEFT = [(data_path('enemies/bat/stayl.png'), ANIMATION_DELAY)]
BAT_DEAD_RIGHT = [(data_path('enemies/bat/deadr.png'), ANIMATION_DELAY)]
BAT_DEAD_LEFT = [(data_path('enemies/bat/deadl.png'), ANIMATION_DELAY)]

MAGE_STAY_RIGHT = pygame.image.load(data_path('enemies/firemage/stayr.png'))
MAGE_STAY_LEFT = pygame.image.load(data_path('enemies/firemage/stayl.png'))
MAGE_DEAD_RIGHT = [(data_path('enemies/firemage/deadr.png'), ANIMATION_DELAY)]
MAGE_DEAD_LEFT = [(data_path('enemies/firemage/deadl.png'), ANIMATION_DELAY)]
MAGE_CAST_RIGHT = pygame.image.load(data_path('enemies/firemage/castr.png'))
MAGE_CAST_LEFT = pygame.image.load(data_path('enemies/firemage/castl.png'))

WRAITH_STAY_RIGHT = pygame.image.load(data_path('enemies/wraith/stayr.png'))
WRAITH_STAY_LEFT = pygame.image.load(data_path('enemies/wraith/stayl.png'))
WRAITH_DEAD_RIGHT = [(data_path('enemies/wraith/deadr.png'), ANIMATION_DELAY)]
WRAITH_DEAD_LEFT = [(data_path('enemies/wraith/deadl.png'), ANIMATION_DELAY)]
WRAITH_CAST_RIGHT = [pygame.image.load(data_path('enemies/wraith/castr1.png')),
                     pygame.image.load(data_path('enemies/wraith/castr2.png'))]
WRAITH_CAST_LEFT = [pygame.image.load(data_path('enemies/wraith/castl1.png')),
                    pygame.image.load(data_path('enemies/wraith/castL2.png'))]


class MeleeEnemy(GameSprite, MeleeEnemy):
    def __init__(self, main, direction, pos_x, pos_y):
        super().__init__(SpriteGroups.enemies_group)
        self.temp_image = None
        self.anim_walk_left = None
        self.anim_walk_right = None
        self.anim_stay_left = None
        self.anim_stay_right = None
        self.ms = None  # ms - movement speed, скорость движения
        self.hp = None
        self.image = None
        self.anim_dead_left = None
        self.anim_dead_right = None
        self.damage = None
        self.impulse = None
        self.stun_power = None

        pygame.sprite.Sprite.__init__(self, SpriteGroups.characters_group,
                                      SpriteGroups.all_sprites)
        self.main = main

        self.direction = direction

        self.start_x = pos_x * Mapping.tile_width
        self.start_y = pos_y * Mapping.tile_height

        self.x_v = 0
        self.y_v = 0

        if self.direction == RIGHT:
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        self.dead = False
        self.on_ground = False

        # Счётчик, показывающий через сколько кадров исчезнет труп врага
        self.dead_count = DEAD_COUNT

        self.setup_properties()

        self.x = self.start_x
        self.y = self.start_y

    def move(self):
        self.temp_image.fill(TRANSPARENT)
        if self.left:
            self.x_v = -self.ms
            self.anim_walk_left.blit(self.temp_image, (0, 0))
        if self.right:
            self.x_v = self.ms
            self.anim_walk_right.blit(self.temp_image, (0, 0))
        self.image = self.temp_image

    def update(self, *args):
        if not self.dead:
            if self.direction == RIGHT:
                self.right = True
                self.left = False
            else:
                self.right = False
                self.left = True
            if self.hp <= 0:
                self.dead = True

            self.move()

            self.y_v += GRAVITATION

            self.on_ground = False
            self.x += self.x_v
            self.collide(self.x_v, 0, )
            self.y += self.y_v
            self.collide(0, self.y_v, )

        else:
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

    def collide(self, x_v, y_v):
        for sprite in pygame.sprite.spritecollide(self,
                                                  SpriteGroups.all_sprites,
                                                  False):
            if isinstance(sprite, Tile) and sprite.is_solid:
                clip = self.rect.clip(sprite.rect)
                if y_v > 0:
                    self.y -= clip.h
                    self.on_ground = True
                    self.y_v = 0
                elif y_v < 0:
                    self.y += clip.h
                if x_v > 0:
                    self.x -= clip.w
                    self.direction = -self.direction
                elif x_v < 0:
                    self.x += clip.w
                    self.direction = -self.direction

            if isinstance(sprite, Player):
                if not sprite.stunned:
                    sprite.hp -= self.damage
                    sprite.stunned = True
                    sprite.stun_count = self.stun_power
                    if sprite.x_v == 0:
                        if self.direction == RIGHT:
                            sprite.x_v = self.impulse
                        else:
                            sprite.x_v = -self.impulse
                    else:
                        if sprite.x_v > 0:
                            sprite.x_v = 0
                            sprite.x_v = -self.impulse
                        elif sprite.x_v < 0:
                            sprite.x_v = 0
                            sprite.x_v = self.impulse

    def setup_properties(self):
        pass


class MeleeEnemyWithMaxX(MeleeEnemy):
    def __init__(self, main, direction, pos_x, pos_y, max_x=-1):
        super().__init__(main, direction, pos_x, pos_y)
        # максимальное расстояние, на котрое можно отойти от начального
        # положения
        self.max_x = max_x * Mapping.tile_width

    def update(self, *args):
        if not self.dead:
            if self.max_x > 0:
                if abs(self.start_x - self.x) >= self.max_x:
                    self.direction *= -1
        super().update(*args)


class Insect(MeleeEnemyWithMaxX):
    def setup_properties(self):
        self.temp_image = pygame.image.load(data_path(
            'enemies/insect/stayr.png'))
        self.image = pygame.image.load(data_path(
            'enemies/insect/stayr.png'))
        self.rect = self.image.get_rect()
        self.hp = INSECT_MAX_HP
        self.damage = INSECT_DMG
        self.impulse = INSECT_IMPULSE
        self.ms = INSECT_MS
        self.stun_power = INSECT_STUN_POWER

        self.anim_stay_right = pyganim.PygAnimation(INSECT_STAY_RIGHT)
        self.anim_stay_right.play()

        self.anim_stay_left = pyganim.PygAnimation(INSECT_STAY_LEFT)
        self.anim_stay_left.play()

        self.anim_dead_right = pyganim.PygAnimation(INSECT_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(INSECT_DEAD_LEFT)
        self.anim_dead_left.play()

        self.anim_walk_right = make_animation(INSECT_RIGHT, ANIMATION_DELAY)
        self.anim_walk_right.play()

        self.anim_walk_left = make_animation(INSECT_LEFT, ANIMATION_DELAY)
        self.anim_walk_left.play()


class Knight(MeleeEnemyWithMaxX):
    def setup_properties(self):
        self.temp_image = pygame.image.load(data_path(
            'enemies/knight/stayr.png'))
        self.image = pygame.image.load(data_path('enemies/knight/stayr.png'))
        self.rect = self.image.get_rect()
        self.hp = KNIGHT_MAX_HP
        self.damage = KNIGHT_DMG
        self.impulse = KNIGHT_IMPULSE
        self.ms = KNIGHT_MS
        self.stun_power = KNIGHT_STUN_POWER

        self.anim_stay_right = pyganim.PygAnimation(KNIGHT_STAY_RIGHT)
        self.anim_stay_right.play()

        self.anim_stay_left = pyganim.PygAnimation(KNIGHT_STAY_LEFT)
        self.anim_stay_left.play()

        self.anim_dead_right = pyganim.PygAnimation(KNIGHT_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(KNIGHT_DEAD_LEFT)
        self.anim_dead_left.play()

        self.anim_walk_right = make_animation(KNIGHT_RIGHT, ANIMATION_DELAY)
        self.anim_walk_right.play()

        self.anim_walk_left = make_animation(KNIGHT_LEFT, ANIMATION_DELAY)
        self.anim_walk_left.play()


class Rat(MeleeEnemyWithMaxX):
    def setup_properties(self):
        self.temp_image = pygame.image.load(data_path('enemies/rat/stayr.png'))
        self.image = pygame.image.load(data_path('enemies/rat/stayr.png'))
        self.rect = self.image.get_rect()
        self.hp = RAT_MAX_HP
        self.damage = RAT_DMG
        self.impulse = RAT_IMPULSE
        self.ms = RAT_MS
        self.stun_power = RAT_STUN_POWER

        self.anim_stay_right = pyganim.PygAnimation(RAT_STAY_RIGHT)
        self.anim_stay_right.play()

        self.anim_stay_left = pyganim.PygAnimation(RAT_STAY_LEFT)
        self.anim_stay_left.play()

        self.anim_dead_right = pyganim.PygAnimation(RAT_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(RAT_DEAD_LEFT)
        self.anim_dead_left.play()

        self.anim_walk_right = make_animation(RAT_RIGHT, ANIMATION_DELAY)
        self.anim_walk_right.play()

        self.anim_walk_left = make_animation(RAT_LEFT, ANIMATION_DELAY)
        self.anim_walk_left.play()


class Snake(MeleeEnemyWithMaxX):
    def setup_properties(self):
        self.temp_image = pygame.image.load(data_path(
            'enemies/snake/stayr.png'))
        self.image = pygame.image.load(data_path(
            'enemies/snake/stayr.png'))
        self.rect = self.image.get_rect()
        self.hp = SNAKE_MAX_HP
        self.damage = SNAKE_DMG
        self.impulse = SNAKE_IMPULSE
        self.ms = SNAKE_MS
        self.stun_power = SNAKE_STUN_POWER

        self.anim_stay_right = pyganim.PygAnimation(SNAKE_STAY_RIGHT)
        self.anim_stay_right.play()

        self.anim_stay_left = pyganim.PygAnimation(SNAKE_STAY_LEFT)
        self.anim_stay_left.play()

        self.anim_dead_right = pyganim.PygAnimation(SNAKE_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(SNAKE_DEAD_LEFT)
        self.anim_dead_left.play()

        self.anim_walk_right = make_animation(SNAKE_RIGHT, ANIMATION_DELAY)
        self.anim_walk_right.play()

        self.anim_walk_left = make_animation(SNAKE_LEFT, ANIMATION_DELAY)
        self.anim_walk_left.play()


class Bat(MeleeEnemy):
    def __init__(self, main, direction, x, y, max_x, max_y):
        super().__init__(main, direction, x, y)
        # максимальное расстояние, на котрое можно отойти от начального
        # положения
        self.max_x = max_x
        self.max_y = max_y
        self.temp_image = pygame.image.load(data_path('enemies/bat/stayr.png'))
        self.image = pygame.image.load(data_path('enemies/bat/stayr.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = BAT_MAX_HP
        self.damage = BAT_DMG
        self.impulse = BAT_IMPULSE
        self.ms = BAT_MS
        self.y_v = BAT_YV

        self.anim_stay_right = pyganim.PygAnimation(BAT_STAY_RIGHT)
        self.anim_stay_right.play()

        self.anim_stay_left = pyganim.PygAnimation(BAT_STAY_LEFT)
        self.anim_stay_left.play()

        self.anim_dead_right = pyganim.PygAnimation(BAT_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(BAT_DEAD_LEFT)
        self.anim_dead_left.play()

        self.anim_walk_right = make_animation(BAT_RIGHT, ANIMATION_DELAY)
        self.anim_walk_right.play()

        self.anim_walk_left = make_animation(BAT_LEFT, ANIMATION_DELAY)
        self.anim_walk_left.play()

    def update(self, *args):
        if not self.dead:
            if self.direction == RIGHT:
                self.right = True
                self.left = False
            else:
                self.right = False
                self.left = True
            if self.hp <= 0:
                self.dead = True
            self.move()

            self.on_ground = False
            self.rect.y += self.y_v
            if self.direction == RIGHT:
                self.rect.x += self.x_v
            else:
                self.rect.x -= self.x_v
            # self.collide(self.x_v, 0, )
            # self.collide(0, self.y_v, )

            if abs(self.start_x - self.rect.x) > self.max_x:
                self.direction = -self.direction
            if abs(self.start_y - self.rect.y) > self.max_y:
                self.y_v = -self.y_v
        else:
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

    # def collide(self, x_v, y_v):
    #    for sprite in pygame.sprite.spritecollideany(self, all_sprites):
    #        if isinstance(sprite, ):  # если является твердым
    #            if x_v > 0:
    #                self.rect.right = sprite.rect.left
    #                self.direction =- self.direction
    #            if x_v < 0:
    #                self.rect.left = sprite.rect.right
    #                self.direction =- self.direction
    #            if y_v > 0:
    #                self.rect.bottom = sprite.rect.top
    #                self.on_ground = True
    #                self.y_v = - self.y_v
    #            if y_v < 0:
    #                self.rect.top = sprite.rect.bottom
    #                self.y_v = -self.y_v
    #        if isinstance(sprite, Player):
    #            if not sprite.stunned:
    #                sprite.hp -= self.damage
    #                sprite.stunned = True
    #                sprite.stun_count = 30
    #                if sprite.x_v == 0:
    #                    if self.direction == RIGHT:
    #                        sprite.x_v = INSECT_IMPULSE
    #                    else:
    #                        sprite.x_v = -INSECT_IMPULSE
    #                else:
    #                   if sprite.x_v > 0:
    #                        sprite.x_v = 0
    #                        sprite.x_v = -INSECT_IMPULSE
    #                   elif sprite.x_v < 0:
    #                        sprite.x_v = 0
    #                        sprite.x_v = INSECT_IMPULSE


class FireMage(pygame.sprite.Sprite, FireMage):
    def __init__(self, main, direction, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self, SpriteGroups.characters_group,
                                      SpriteGroups.all_sprites)
        self.main = main
        self.direction = direction
        self.y_v = 0
        self.start_x = Mapping.tile_width * pos_x
        self.start_y = Mapping.tile_height * pos_y
        self.temp_image = pygame.image.load(data_path(
            'enemies/firemage/stayr.png'))
        self.image = pygame.image.load(data_path(
            'enemies/firemage/stayr.png'))
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.hp = FIREMAGE_HP
        self.mp = FIREMAGE_MP
        self.dead = False
        self.on_ground = False
        self.attack = False
        self.attack_cd = 0
        self.dead_count = 60

        self.anim_dead_right = pyganim.PygAnimation(MAGE_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(MAGE_DEAD_LEFT)
        self.anim_dead_left.play()

    def update(self, *args):
        if not self.dead:
            if self.mp < FIREMAGE_MP:
                self.mp += FIREMAGE_MP_REG
            if self.mp >= FIREMAGE_MP:
                self.mp = FIREMAGE_MP

            if self.main.hero.rect.x > self.rect.x:
                self.direction = RIGHT
            else:
                self.direction = LEFT
            if self.hp <= 0:
                self.dead = True
            if abs(self.main.hero.rect.x - self.rect.x) <= 600:
                self.attack = True

            self.temp_image.fill(TRANSPARENT)
            if 0 <= self.attack_cd <= 30:
                if self.direction == RIGHT:
                    self.temp_image.blit(MAGE_CAST_RIGHT, (0, 0))
                else:
                    self.temp_image.blit(MAGE_CAST_LEFT, (0, 0))

            else:
                if self.direction == RIGHT:
                    self.temp_image.blit(MAGE_STAY_RIGHT, (0, 0))
                else:
                    self.temp_image.blit(MAGE_STAY_LEFT, (0, 0))
            self.image = self.temp_image

            if self.attack:
                self.attack_cd -= 1
                if self.attack_cd < 0:
                    self.attack_cd = 60
                if self.mp >= FIREBALL_COST and self.attack_cd == 0:
                    self.mp -= FIREBALL_COST
                    fireball = Fireball(self.direction, self.rect.x + 9,
                                        self.rect.y + 9,
                                        self.main.hero.rect.x + 5,
                                        self.main.hero.rect.y + 5)
                    # добавить fireball в соотвутсвующие группы спрайтов
                    self.main.proj.add(fireball)
            else:
                self.attack_cd = 0

            if not self.on_ground:
                self.y_v += GRAVITATION

            self.on_ground = False
            self.attack = False
            self.rect.y += self.y_v
        else:
            self.attack = False
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


class Wraith(pygame.sprite.Sprite):
    def __init__(self, main, direction, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.direction = direction
        self.y_v = 0
        self.start_x = x
        self.start_y = y
        self.temp_image = pygame.image.load(data_path('enemies/wraith/stayr.png'))
        self.image = pygame.image.load(data_path('enemies/wraith/stayr.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = WRAITH_HP
        self.mp = WRAITH_MP
        self.dead = False
        self.on_ground = False
        self.attack = False
        self.attack_cd = 0
        self.dead_count = 60

        self.anim_dead_right = pyganim.PygAnimation(WRAITH_DEAD_RIGHT)
        self.anim_dead_right.play()

        self.anim_dead_left = pyganim.PygAnimation(WRAITH_DEAD_LEFT)
        self.anim_dead_left.play()

    def update(self, *args):
        if not self.dead:
            if self.mp < WRAITH_MP:
                self.mp += WRAITH_MP_REG
            if self.mp >= WRAITH_MP:
                self.mp = WRAITH_MP

            if self.main.hero.rect.x > self.rect.x:
                self.direction = RIGHT
            else:
                self.direction = LEFT
            if self.hp <= 0:
                self.dead = True
            if abs(self.main.hero.rect.x - self.rect.x) <= 1000:
                self.attack = True

            self.temp_image.fill(TRANSPARENT)
            if 0 <= self.attack_cd <= 30:
                if 0 <= self.attack_cd <= 15:
                    if self.direction == RIGHT:
                        self.temp_image.blit(WRAITH_CAST_RIGHT[0], (0, 0))
                    else:
                        self.temp_image.blit(WRAITH_CAST_LEFT[0], (0, 0))
                else:
                    if self.direction == RIGHT:
                        self.temp_image.blit(WRAITH_CAST_RIGHT[1], (0, 0))
                    else:
                        self.temp_image.blit(WRAITH_CAST_LEFT[1], (0, 0))

            else:
                if self.direction == RIGHT:
                    self.temp_image.blit(WRAITH_STAY_RIGHT, (0, 0))
                else:
                    self.temp_image.blit(WRAITH_STAY_LEFT, (0, 0))
            self.image = self.temp_image

            if self.attack:
                self.attack_cd -= 1
                if self.attack_cd < 0:
                    self.attack_cd = 60
                if self.mp >= AIMEDFB_COST and self.attack_cd == 0:
                    self.mp -= AIMEDFB_COST
                    aimed_fireball = AimedFireball(self.main.hero, self.rect.x + 9, self.rect.y + 9)
                    # добавить aimed_fireball в соотвутсвующие группы спрайтов
            else:
                self.attack_cd = 0

            if not self.on_ground:
                self.y_v += GRAVITATION

            self.on_ground = False
            self.attack = False
            self.rect.y += self.y_v
        else:
            self.attack = False
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