import pygame


def empty_all():
    for group in groups:
        group.empty()


class TilesGroup(pygame.sprite.Group):
    def draw(self, surface):
        """Рисует все спрайты на поверхности, начиная со спрайтов с наименьним
        z-index."""
        sprites = sorted(self.sprites(), key=lambda sprite: sprite.z_index)
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []


all_sprites = pygame.sprite.Group()
tiles_group = TilesGroup()
groups = [all_sprites, tiles_group]
