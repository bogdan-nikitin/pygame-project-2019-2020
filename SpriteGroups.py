import pygame
from GameUIHeaders import *


# Все объявленные группы необходимо добавить в список groups


def empty_all():
    """Удаляет все спрайты."""
    for group in groups:
        group.empty()


def draw_ui(surface, sprite):
    if isinstance(sprite, Panel):
        pygame.draw.rect(surface, sprite.bg_color, sprite.rect)
        pygame.draw.rect(surface, sprite.bound_color, sprite.rect,
                         sprite.bound)
    elif isinstance(sprite, Label):
        surface.blit(sprite.text_render, sprite.rect.topleft)
    for child in sprite.children:
        draw_ui(surface, child)


class TilesGroup(pygame.sprite.Group):
    def draw(self, surface, active_only=True):
        """Рисует все спрайты на поверхности, начиная со спрайтов с наименьним
        z-index."""
        if active_only:
            active_sprites = filter(lambda sprite: sprite.is_active,
                                    self.sprites())
        else:
            active_sprites = self.sprites()
        sprites = sorted(active_sprites, key=lambda sprite: sprite.z_index)
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


class UIGroup(pygame.sprite.Group):
    def draw(self, surface):
        for spr in self.sprites():
            if spr.parent is None:
                draw_ui(surface, spr)

    def event(self, event: pygame.event.Event):
        for sprite in self:
            sprite.event(event)


all_sprites = pygame.sprite.Group()
tiles_group = TilesGroup()
ui_group = UIGroup()
groups = [all_sprites, tiles_group, ui_group]
