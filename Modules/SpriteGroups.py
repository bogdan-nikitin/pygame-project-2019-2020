import pygame
from Modules.GameUIHeaders import *


def empty_all():
    """Удаляет все спрайты."""
    for sprite in all_sprites:
        sprite.kill()


def empty_group(group):
    """Удаляет из всех групп спрайты из группы group."""
    # pygame.sprite.Group.empty() удаляет спрайты только из одной группы, так
    # что если спрайт содержится в других группах, то он продолжает существовать
    for sprite in group:
        sprite.kill()


def draw_ui(surface, sprite):
    if not sprite.is_active:
        return
    if isinstance(sprite, Panel):
        pygame.draw.rect(surface, sprite.bg_color, sprite.rect)
        pygame.draw.rect(surface, sprite.bound_color, sprite.rect,
                         sprite.bound)
        if isinstance(sprite, CheckboxPanel):
            if sprite.checked:
                rect = sprite.rect.copy()
                rect.size = rect.w - sprite.bound * 2, rect.h - sprite.bound * 2
                rect.center = sprite.rect.center
                pos = [(rect.topleft, rect.bottomright),
                       (rect.topright, rect.bottomleft)]
                for p1, p2 in pos:
                    pygame.draw.line(surface, CHECKBOX_PANEL_LINE_COLOR,
                                     p1, p2, CHECKBOX_PANEL_LINE_WIDTH)
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
characters_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
