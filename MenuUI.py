from General import *
from GameUI import *
import SpriteGroups
import pygame


MENU_W = 300
MENU_H = 200
MENU_PADDING = 15
MENU_LABEL_MARGIN_BOTTOM = 10

RESUME_EVENT = pygame.event.Event(pygame.USEREVENT + 1, {})
EXIT_EVENT = pygame.event.Event(pygame.USEREVENT + 2, {})
FULLSCREEN_EVENT_TYPE = pygame.USEREVENT + 3
FULLSCREEN_EVENT_ATTR = 'fullscreen'


class Menu(Panel):
    """Класс игрвого меню."""
    def __init__(self, main, groups=()):
        super().__init__()
        w, h = main.screen.get_rect().size
        self.set_geometry(w // 2 - MENU_W // 2, h // 2 - MENU_H // 2,
                          MENU_W, MENU_H)
        self.screen = main.screen

        self.menu_label = Label('Menu', self, groups)
        self.menu_label.font_size = 25
        w = self.menu_label.w
        self.menu_label.set_pos(self.w // 2 - w // 2, MENU_PADDING)
        distance_between_labels = (self.h - self.menu_label.y -
                                   self.menu_label.h - MENU_PADDING -
                                   MENU_LABEL_MARGIN_BOTTOM)

        self.resume_label = LabelButton('Resume', self, groups)
        distance_between_labels -= self.resume_label.h

        self.settings_label = LabelButton('Settings', self, groups)
        distance_between_labels -= self.settings_label.h

        self.exit_label = LabelButton('Exit', self, groups)
        distance_between_labels -= self.exit_label.h

        distance = distance_between_labels / 3

        w = self.resume_label.w
        self.resume_label.set_pos(self.w // 2 - w // 2,
                                  self.menu_label.y + self.menu_label.h +
                                  distance + MENU_LABEL_MARGIN_BOTTOM)
        self.resume_label.clicked = self.resume

        w = self.settings_label.w
        self.settings_label.set_pos(self.w // 2 - w // 2,
                                    self.resume_label.y + self.resume_label.h +
                                    distance)
        self.settings_label.clicked = self.settings

        w = self.exit_label.w
        self.exit_label.set_pos(self.w // 2 - w // 2,
                                self.settings_label.y + self.settings_label.h +
                                distance)
        self.exit_label.clicked = self.exit
        self.main = main
        self.settings_panel = Settings(self, groups)
        self.settings_panel.hide()

    def event(self, event):
        super().event(event)
        if event.type == pygame.VIDEORESIZE:
            w, h = event.size
            self.set_pos(w // 2 - self.w // 2, h // 2 - self.h // 2)

    @staticmethod
    def resume(x, y):
        pygame.event.post(RESUME_EVENT)

    @staticmethod
    def exit(x, y):
        pygame.event.post(EXIT_EVENT)

    def settings(self, x, y):
        self.hide()
        self.settings_panel.show()


class Settings(Panel):
    """Класс настроек."""
    def __init__(self, menu, groups=()):
        super().__init__()
        w, h = menu.main.screen.get_rect().size
        self.set_geometry(w // 2 - MENU_W // 2, h // 2 - MENU_H // 2,
                          MENU_W, MENU_H)
        self.screen = menu.main.screen

        self.settings_label = Label('Settings', self, groups)
        self.settings_label.font_size = 25
        w = self.settings_label.w
        self.settings_label.set_pos(self.w // 2 - w // 2, MENU_PADDING)

        self.full_screen_box = Checkbox('Fullscreen', self, groups)
        w, h = self.full_screen_box.w, self.full_screen_box.h

        self.full_screen_box.set_pos(self.w // 2 - w // 2,
                                     self.h // 2 + h // 2)

        self.back_label = LabelButton('Back', self, groups)
        w, h = self.back_label.w, self.back_label.h
        self.back_label.set_pos(self.w // 2 - w // 2,
                                self.h - MENU_PADDING - h)
        self.menu = menu
        self.back_label.clicked = self.back

    def back(self, x, y):
        dictionary = {FULLSCREEN_EVENT_ATTR: self.full_screen_box.checked}
        full_screen_event = pygame.event.Event(FULLSCREEN_EVENT_TYPE,
                                               dictionary)
        pygame.event.post(full_screen_event)
        self.hide()
        self.menu.show()

import Main
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([800, 800], pygame.RESIZABLE)
    m = Menu(Main.Main(screen))

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