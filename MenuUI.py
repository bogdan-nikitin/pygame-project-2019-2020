from General import *
from GameUI import *
import SpriteGroups
import pygame


MENU_W = 400
MENU_H = 300
MENU_PADDING = 15


class Menu(Panel):
    def __init__(self, screen, groups=()):
        super().__init__()
        w, h = screen.get_rect().size
        self.set_geometry(w // 2 - MENU_W // 2, h // 2 - MENU_H // 2,
                          MENU_W, MENU_H)
        self.screen = screen
        self.menu_label = Label('Menu', self, groups)
        self.menu_label.font_size = 20
        w, h = self.menu_label.w, self.menu_label.h
        self.menu_label.set_pos(self.w // 2 - w // 2, MENU_PADDING)

    def event(self, event):
        super().event(event)
        if event.type == pygame.VIDEORESIZE:
            w, h = event.size
            self.set_pos(w // 2 - self.w // 2, h // 2 - self.h // 2)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([800, 800], pygame.RESIZABLE)
    m = Menu(screen)

    clock = pygame.time.Clock()
    running = True
    while running:
        tick = clock.tick()
        for event in pygame.event.get():
            SpriteGroups.ui_group.event(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        clear(screen)
        SpriteGroups.ui_group.draw(screen)
        draw_fps(screen, clock.get_fps())
        pygame.display.flip()
    pygame.quit()
