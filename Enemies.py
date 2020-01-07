import pygame
from Player import Player
from configuration import *

INSECT_DMG = 20
INSECT_IMPULSE = 5
INSECT_MAX_HP = 35
INSECT_MS = 3

KNIGHT_DMG = 40
KNIGHT_IMPULSE = 7
KNIGHT_MAX_HP = 80
KNIGHT_MS = 3

RAT_DMG = 35
RAT_IMPULSE = 4
RAT_MAX_HP = 40
RAT_MS = 3

SNAKE_DMG = 20
SNAKE_IMPULSE = 6
SNAKE_MAX_HP = 65
SNAKE_MS = 3

INSECT_RIGHT = ['data/enemies/insect/walkr1.png',
                'data/enemies/insect/walkr2.png',
                'data/enemies/insect/walkr3.png',
                'data/enemies/insect/walkr4.png', ]
INSECT_LEFT = ['data/enemies/insect/walkl1.png',
               'data/enemies/insect/walkl2.png',
               'data/enemies/insect/walkl3.png',
               'data/enemies/insect/walkl4.png', ]
INSECT_STAY_RIGHT = [('data/enemies/insect/stayr.png', ANIMATION_DELAY)]
INSECT_STAY_LEFT = [('data/enemies/insect/stayl.png', ANIMATION_DELAY)]
INSECT_DEAD_RIGHT = [('data/enemies/insect/deadr.png', ANIMATION_DELAY)]
INSECT_DEAD_LEFT = [('data/enemies/insect/deadl.png', ANIMATION_DELAY)]

KNIGHT_RIGHT = ['data/enemies/knight/walkr1.png',
                'data/enemies/knight/walkr2.png', ]
KNIGHT_LEFT = ['data/enemies/knight/walkl1.png',
               'data/enemies/knight/walkl2.png', ]
KNIGHT_STAY_RIGHT = [('data/enemies/knight/stayr.png', ANIMATION_DELAY)]
KNIGHT_STAY_LEFT = [('data/enemies/knight/stayl.png', ANIMATION_DELAY)]
KNIGHT_DEAD_RIGHT = [('data/enemies/knight/deadr.png', ANIMATION_DELAY)]
KNIGHT_DEAD_LEFT = [('data/enemies/knight/deadl.png', ANIMATION_DELAY)]

RAT_RIGHT = ['data/enemies/rat/walkr1.png',
             'data/enemies/rat/walkr2.png',
             'data/enemies/rat/walkr3.png', ]
RAT_LEFT = ['data/enemies/rat/walkl1.png',
            'data/enemies/rat/walkl2.png',
            'data/enemies/rat/walkl3.png', ]
RAT_STAY_RIGHT = [('data/enemies/rat/stayr.png', ANIMATION_DELAY)]
RAT_STAY_LEFT = [('data/enemies/rat/stayl.png', ANIMATION_DELAY)]
RAT_DEAD_RIGHT = [('data/enemies/rat/deadr.png', ANIMATION_DELAY)]
RAT_DEAD_LEFT = [('data/enemies/rat/deadl.png', ANIMATION_DELAY)]

SNAKE_RIGHT = ['data/enemies/snake/walkr1.png',
               'data/enemies/snake/walkr2.png',
               'data/enemies/snake/walkr3.png', ]
SNAKE_LEFT = ['data/enemies/snake/walkl1.png',
              'data/enemies/snake/walkl2.png',
              'data/enemies/snake/walkl3.png', ]
SNAKE_STAY_RIGHT = [('data/enemies/snake/stayr.png', ANIMATION_DELAY)]
SNAKE_STAY_LEFT = [('data/enemies/snake/stayl.png', ANIMATION_DELAY)]
SNAKE_DEAD_RIGHT = [('data/enemies/snake/deadr.png', ANIMATION_DELAY)]
SNAKE_DEAD_LEFT = [('data/enemies/snake/deadl.png', ANIMATION_DELAY)]


class MeleeEnemy(pygame.sprite.Sprite):
    def __init__(self, main, direction, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.main = main
        self.direction = direction
        self.start_x = x
        self.start_y = y
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

    def move(self, color_key):
        self.temp_image.fill(color_key)
        if self.left:
            self.x_v = self.ms
            self.anim_walk_left.blit(self.temp_image, (0, 0))
            self.image = self.temp_image
        if self.right:
            self.x_v = self.ms
            self.anim_walk_right.blit(self.temp_image, (0, 0))
        if self.dead:
            self.x_v = 0
            if self.direction == RIGHT:
                self.anim_dead_right.blit(self.temp_image, (0, 0))
            else:
                self.anim_dead_left.blit(self.temp_image, (0, 0))
        self.image = self.temp_image

    def update(self):
        if not self.dead:
            if self.direction == RIGHT:
                self.right = True
                self.left = False
            else:
                self.right = False
                self.left = True
            if self.hp <= 0:
                self.dead = True
            color_key = self.image.get_at((0, 0))
            self.move(color_key)
            if not self.on_ground:
                self.y_v += GRAVITATION

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
    #                self.y_v = 0
    #            if y_v < 0:
    #                self.rect.top = sprite.rect.bottom
    #                self.y_v = 0
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


class Insect(MeleeEnemy):
    def __init__(self, main, direction, x, y, max_x):
        super().__init__(main, direction, x, y)
        self.max_x = max_x  # максимальное расстояние, на котрое можно отойти от начального положения
        self.temp_image = pygame.image.load('data/enemies/insect/stayr.png')
        self.image = pygame.image.load('data/enemies/insect/stayr.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = INSECT_MAX_HP
        self.damage = INSECT_DMG
        self.impulse = INSECT_IMPULSE
        self.ms = INSECT_MS

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


class Knight(MeleeEnemy):
    def __init__(self, main, direction, x, y, max_x):
        super().__init__(main, direction, x, y)
        self.max_x = max_x  # максимальное расстояние, на котрое можно отойти от начального положения
        self.temp_image = pygame.image.load('data/enemies/knight/stayr.png')
        self.image = pygame.image.load('data/enemies/knight/stayr.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = KNIGHT_MAX_HP
        self.damage = KNIGHT_DMG
        self.impulse = KNIGHT_IMPULSE
        self.ms = KNIGHT_MS

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


class Rat(MeleeEnemy):
    def __init__(self, main, direction, x, y, max_x):
        super().__init__(main, direction, x, y)
        self.max_x = max_x  # максимальное расстояние, на котрое можно отойти от начального положения
        self.temp_image = pygame.image.load('data/enemies/rat/stayr.png')
        self.image = pygame.image.load('data/enemies/rat/stayr.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = RAT_MAX_HP
        self.damage = RAT_DMG
        self.impulse = RAT_IMPULSE
        self.ms = RAT_MS

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


class Snake(MeleeEnemy):
    def __init__(self, main, direction, x, y, max_x):
        super().__init__(main, direction, x, y)
        self.max_x = max_x  # максимальное расстояние, на котрое можно отойти от начального положения
        self.temp_image = pygame.image.load('data/enemies/snake/stayr.png')
        self.image = pygame.image.load('data/enemies/snake/stayr.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = SNAKE_MAX_HP
        self.damage = SNAKE_DMG
        self.impulse = SNAKE_IMPULSE
        self.ms = SNAKE_MS

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
