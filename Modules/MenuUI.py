"""Содержит классы игрового меню, которое вызывается на кнопку Esc."""

from Modules.GameUI import *

MENU_W = 300
MENU_H = 200
MENU_PADDING = 15
MENU_LABEL_MARGIN_BOTTOM = 10

RESUME_EVENT = pygame.event.Event(pygame.USEREVENT + 1, {})
EXIT_EVENT = pygame.event.Event(pygame.USEREVENT + 2, {})
FULL_SCREEN_EVENT_TYPE = pygame.USEREVENT + 3
FULL_SCREEN_EVENT_ATTR = 'fullscreen'

# Ключи для словаря settings_data в классе Menu
FULL_SCREEN_PARAM = 'full_screen'


class Menu(Panel):
    """Класс игрвого меню."""

    def __init__(self, main, settings_data=None, groups=()):
        super().__init__()
        self._settings_data = settings_data or {}
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

    @property
    def settings_data(self):
        return self._settings_data


class Settings(Panel):
    """Класс настроек."""

    def __init__(self, menu, groups=()):
        super().__init__()
        w, h = menu.main.screen.get_rect().size
        self.set_geometry(w // 2 - MENU_W // 2, h // 2 - MENU_H // 2,
                          MENU_W, MENU_H)
        self.screen = menu.main.screen

        self.menu = menu

        self.settings_label = Label('Settings', self, groups)
        self.settings_label.font_size = 25
        w = self.settings_label.w
        self.settings_label.set_pos(self.w // 2 - w // 2, MENU_PADDING)

        self.full_screen_box = Checkbox('Fullscreen', self, groups)
        full_screen = self.menu.settings_data.get(FULL_SCREEN_PARAM, False)
        self.full_screen_box.set_checked(full_screen)
        self.menu.settings_data[FULL_SCREEN_PARAM] = full_screen
        self.full_screen_box.check_state_changed = self.on_full_screen_change
        w, h = self.full_screen_box.w, self.full_screen_box.h

        self.full_screen_box.set_pos(self.w // 2 - w // 2,
                                     self.h // 2 + h // 2)

        self.back_label = LabelButton('Back', self, groups)
        w, h = self.back_label.w, self.back_label.h
        self.back_label.set_pos(self.w // 2 - w // 2,
                                self.h - MENU_PADDING - h)
        self.back_label.clicked = self.back

    def back(self, x, y):
        """Вызывается при нажатии кнопки назад, скрывает настройки и показывает
        меню. Также приминяет выбранные настройки."""
        self.hide()
        self.menu.show()

    def on_full_screen_change(self, state):
        self.menu.settings_data[FULL_SCREEN_PARAM] = state
        dictionary = {FULL_SCREEN_EVENT_ATTR: self.full_screen_box.checked}
        full_screen_event = pygame.event.Event(FULL_SCREEN_EVENT_TYPE,
                                               dictionary)
        pygame.event.post(full_screen_event)
