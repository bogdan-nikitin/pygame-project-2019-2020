from General import *
from Constants import *
import SpriteGroups
import pygame
from GameUIHeaders import *
from multipledispatch import dispatch  # Модуль для "перегрузки" функций
from numbers import Number


PANEL_BG_COLOR = pygame.Color(102, 187, 187, a=100)
PANEL_BOUND_COLOR = pygame.Color(51, 51, 51)
LABEL_COLOR = pygame.Color(221, 221, 221)
FONT_FILENAME = data_path('font.ttf')
FONT_SIZE = 20


class UIElement(UIElement, pygame.sprite.Sprite):
    def __init__(self, *groups, parent=None):
        super().__init__(SpriteGroups.all_sprites, SpriteGroups.ui_group,
                         *groups)
        self._parent = parent
        if self._parent:
            self._parent.add_child(self)
        self._children = []
        self._rect = pygame.rect.Rect(0, 0, 0, 0)
        self._x, self._y, self._w, self._h = 0, 0, 0, 0

    @dispatch(pygame.rect.Rect)
    def set_geometry(self, rect):
        self._rect = rect
        self._update_children_pos()

    @dispatch(Number, Number, Number, Number)
    def set_geometry(self, x, y, w, h):
        self._x, self._y, self._w, self._h = x, y, w, h
        if self._parent:
            x += self._parent.rect.x
            y += self._parent.rect.y
        self._rect = pygame.rect.Rect(x, y, w, h)
        self._update_children_pos()

    def get_geometry(self):
        return self._x, self._y, self._w, self._h

    @property
    def rect(self):
        return self._rect

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def children(self):
        return self._children

    @property
    def parent(self):
        return self._parent

    def resize(self, w, h):
        self._w, self._h = w, h
        self._rect.size = w, h

    def set_pos(self, x, y):
        self._x, self._y = x, y
        if self.parent:
            x += self.parent.rect.x
            y += self.parent.rect.y
        self._rect.topleft = x, y
        self._update_children_pos()

    def get_parent(self):
        return self._parent

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def _update_children_pos(self):
        for child in self._children:
            child: UIElement
            child._update_pos()

    def _update_pos(self):
        x = self.x
        y = self.y
        if self.parent:
            x += self.parent.x
            y += self.parent.y
            if isinstance(self.parent, Panel):
                self._x += self.parent.bound
                self._y += self.parent.bound
        self._rect.topleft = x, y

    def add_child(self, child):
        self._children += [child]


class Panel(UIElement, Panel):
    def __init__(self, *groups, parent=None):
        super().__init__(*groups, parent=parent)
        self.bg_color = PANEL_BG_COLOR
        self._bound = 4
        self.bound_color = PANEL_BOUND_COLOR

    def set_bg_color(self, color):
        self.bg_color = color

    @property
    def bound(self):
        return self._bound

    @bound.setter
    def bound(self, bound):
        self._bound = bound
        self._update_children_pos()


class Label(UIElement, Label):
    def __init__(self, text='', *groups, parent=None):
        super().__init__(*groups, parent=parent)
        self._font_filename = FONT_FILENAME
        self._font_size = FONT_SIZE
        self._font = pygame.font.Font(self._font_filename, self._font_size)
        self.color = LABEL_COLOR
        self._antialias = 1
        self._text = text
        self._text_render = None
        self._update_font()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._update_font()

    @property
    def text_render(self):
        return self._text_render

    @property
    def font_filename(self):
        return self._font_filename

    def _update_font(self):
        self._text_render = self._font.render(self._text, self._antialias,
                                              self.color)
        self._x, self._y = self._rect.topleft
        self._w, self._h = self._text_render.get_size()
        self._rect = pygame.rect.Rect(self._x, self._y, self._w, self._h)
        self._update_pos()


# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode([500, 500])
#     p = Panel()
#     l = Label('kek', parent=p)
#     l.set_pos(10, 10)
#     p.set_geometry(100, 100, 100, 100)
#     l.set_pos(20, 20)
#     p.set_geometry(20, 20, 150, 200)
#     p.bound = 5
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         clear(screen)
#         SpriteGroups.ui_group.draw(screen)
#         pygame.display.flip()
#     pygame.quit()
