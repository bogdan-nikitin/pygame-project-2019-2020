import pygame
import pyganim
from configuration import *

ANIMATION_RIGHT = ['data/player/player_walk/walkr1.png',
                   'data/player/player_walk/walkr2.png',
                   'data/player/player_walk/walkr3.png',
                   'data/player/player_walk/walkr4.png', ]
ANIMATION_LEFT = ['data/player/player_walk/walkl1.png',
                  'data/player/player_walk/walkl2.png',
                  'data/player/player_walk/walkl3.png',
                  'data/player/player_walk/walkl4.png', ]
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
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((22, 24))
        self.screen = screen
        self.image = pygame.image.load('data/player/initialization.png')
        self.x = x
        self.y = y
        self.x_v = 0
        self.y_v = 0
        self.rect = pygame.image.load('data/player/player_stay/stayr.png').get_rect()
        self.rect.x = x
        self.rect.y = y
        self.on_ground = False

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

    def update(self, direction, left, right, up, solid_blocks):
        # color_key = self.image.get_at((0, 0))
        if left:
            self.x_v = -MOVE_SPEED
            if not up:
                # self.image.fill(COLOR_KEY)
                self.anim_walk_left.blit(self.screen, (self.rect.left, self.rect.top))
        if right:
            self.x_v = MOVE_SPEED
            if not up:
                # self.image.fill(COLOR_KEY)
                self.anim_walk_right.blit(self.screen, (self.rect.left, self.rect.top))
        if not (left or right):
            self.x_v = 0
            if not up:
                if direction == RIGHT:
                    # self.image.fill(COLOR_KEY)
                    self.anim_stay_right.blit(self.screen, (self.rect.left, self.rect.top))
                else:
                    # self.image.fill(COLOR_KEY)
                    self.anim_stay_left.blit(self.screen, (self.rect.left, self.rect.top))
        if up:
            if self.on_ground:
                self.y_v = -JUMP_SPEED
            if direction == RIGHT:
                # self.image.fill(COLOR_KEY)
                self.anim_jump_right.blit(self.screen, (self.rect.left, self.rect.top))
            else:
                # self.image.fill(COLOR_KEY)
                self.anim_jump_left.blit(self.screen, (self.rect.left, self.rect.top))

        if not self.on_ground:
            self.y_v += GRAVITATION

        self.on_ground = False
        self.x += self.x_v
        self.rect.x += self.x_v
        self.collide(self.x_v, 0, solid_blocks)
        self.y += self.y_v
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
