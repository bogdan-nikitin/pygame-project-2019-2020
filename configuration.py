import pyganim
"""Все конастанты в Constants"""
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

RIGHT = 1
LEFT = -1

GRAVITATION = 0.2

ANIMATION_DELAY = 100
ANIMATION_CAST_DELAY = 500

HERO_DA_DMG = 35
HERO_DA_COST = 20
HERO_RA_DMG = 25
HERO_RA_COST = 25

FIREBALL_DMG = 40
FIREBALL_COST = 50
AIMEDFB_DMG = 30
AIMEDFB_COST = 100


def make_animation(animation_list, delay):  # в General
    animation = []
    for elem in animation_list:
        animation.append((elem, delay))
    result = pyganim.PygAnimation(animation)
    return result
