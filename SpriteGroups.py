import pygame


# Все объявленные группы необходимо добавить в список groups


def empty_all():
    """Удаляет все спрайты."""
    for group in groups:
        group.empty()


def draw_ui(surface, sprite):
    if type(sprite) == 'Panel':
        pass


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
                print(type(spr))
                pass


all_sprites = pygame.sprite.Group()
tiles_group = TilesGroup()
ui_group = UIGroup()
groups = [all_sprites, tiles_group, ui_group]
