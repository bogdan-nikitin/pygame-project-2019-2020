from General import *
from Constants import *
import SpriteGroups
import pygame
from GameUIHeaders import *
from ColorPalette import *
from multipledispatch import dispatch  # Модуль для "перегрузки" функций
from numbers import Number


class UIElement(pygame.sprite.Sprite, UIElement):
    """Класс элемента интерфейса."""
    def __init__(self, parent=None, groups=()):
        super().__init__(SpriteGroups.all_sprites, SpriteGroups.ui_group,
                         *groups)
        self._parent = parent
        if self._parent:
            self._parent.add_child(self)
        self._children = []
        self._rect = pygame.rect.Rect(0, 0, 0, 0)
        self._x, self._y, self._w, self._h = 0, 0, 0, 0
        self._is_active = True

    def show(self):
        self._is_active = True

    def hide(self):
        self._is_active = False

    @property
    def is_active(self):
        return self._is_active

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

    def _update_children_pos(self):
        for child in self._children:
            child: UIElement
            child._update_pos()
            child._update_children_pos()

    def _update_pos(self):
        x = self.x
        y = self.y
        rect_x, rect_y = x, y
        if self.parent:
            rect_x += self.parent.rect.x
            rect_y += self.parent.rect.y
            if isinstance(self.parent, Panel):
                bound = self.parent.bound
                rect_x += bound
                rect_y += bound
        self._rect.topleft = rect_x, rect_y
        self._x, self._y = x, y
        self._update_children_pos()

    def add_child(self, child):
        self._children += [child]

    def event(self, event: pygame.event.Event):
        if not self._is_active:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(*event.pos):
                self.on_mouse_up(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*event.pos):
                self.on_mouse_down(*event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(*event.pos):
                self.on_hover(*event.pos)
            else:
                self.no_hover(*event.pos)

    def on_hover(self, x, y):
        pass

    def on_mouse_up(self, x, y):
        pass

    def on_mouse_down(self, x, y):
        pass

    def no_hover(self, x, y):
        pass


class Group(UIElement):
    """Класс группы UI элементов, принимает размер родителя, графически не
    отображается"""
    def __init__(self, parent=None, groups=()):
        super().__init__(parent, groups)
        self._update_pos()

    def _update_pos(self):
        parent = self.parent
        if parent:
            self._rect = parent.rect
            self._x, self._y = parent.x, parent.y
            self._w, self._h = parent.w, parent.y


class Panel(UIElement, Panel):
    """Класс панели, графически отображается как прямоугольник с рамкой."""
    def __init__(self, parent=None, groups=()):
        super().__init__(*groups, parent=parent)
        self.bg_color = PANEL_BG_COLOR
        self._bound = PANEL_BOUND
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
    """Класс текста."""
    def __init__(self, text='', parent=None, groups=()):
        super().__init__(*groups, parent=parent)
        self._font_filename = FONT_FILENAME
        self._font_size = FONT_SIZE
        self._font = pygame.font.Font(self._font_filename, self._font_size)
        self._color = LABEL_COLOR
        self._antialias = LABEL_ANTIALIAS
        self._text = text
        self._text_render = None
        self.text = text
        self._update_pos()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._update_font()
        self._w, self._h = self._text_render.get_size()
        self._rect.size = self._w, self._h

    @property
    def antialias(self):
        return self._antialias

    @antialias.setter
    def antialias(self, value):
        self._antialias = value
        self._update_font()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._update_font()

    @property
    def text_render(self):
        return self._text_render

    @property
    def font_filename(self):
        return self._font_filename

    def _update_font(self):
        self._font = pygame.font.Font(self._font_filename, self._font_size)
        self._text_render = self._font.render(self._text, self._antialias,
                                              self._color)
        self._w, self._h = self._text_render.get_size()
        self._rect.size = self._w, self._h

    @dispatch(pygame.rect.Rect)
    def set_geometry(self, rect):
        new_rect = pygame.rect.Rect(rect.topleft, self.rect.size)
        super().set_geometry(new_rect)

    @dispatch(Number, Number, Number, Number)
    def set_geometry(self, x, y, w, h):
        super().set_geometry(x, y, self.w, self.h)

    def resize(self, w, h):
        pass

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value):
        self._font_size = value
        self._update_font()


class LabelButton(Label, LabelButton):
    """Класс текста-кнопки. При наведении курсора подсвечивается, при нажатии
    вызывает функцию clicked."""
    def __init__(self, text='', parent=None, groups=()):
        super().__init__(text, parent, groups)
        self.inactive_color = self.color
        self.active_color = LABEL_COLOR_HOVER
        self.clicked = lambda x, y: None

    def on_hover(self, x, y):
        self.color = self.active_color

    def no_hover(self, x, y):
        self.color = self.inactive_color

    def on_mouse_up(self, x, y):
        self.clicked(x, y)


class Button(Panel, Button):
    """Класс кнопки. При нажатии вызывает функцию clicked и меняет цвет."""
    def __init__(self, text='', parent=None, groups=()):
        super().__init__(parent, groups)
        self.bg_color = BUTTON_INACTIVE_COLOR
        self.inactive_bg_color = self.bg_color
        self.active_bg_color = BUTTON_ACTIVE_COLOR
        self.label = Label(text, self, groups)
        self._update_button_label()
        self.clicked = lambda x, y: None

    def resize(self, w, h):
        super().resize(w, h)
        self._update_button_label()

    @dispatch(pygame.rect.Rect)
    def set_geometry(self, rect):
        super().set_geometry(rect)
        self._update_button_label()

    @dispatch(Number, Number, Number, Number)
    def set_geometry(self, x, y, w, h):
        super().set_geometry(x, y, w, h)
        self._update_button_label()

    def _update_button_label(self):
        text_x = (self.w - self.label.w + self.bound) // 2
        text_y = (self.h - self.label.h + self.bound) // 2
        self.label.set_pos(text_x, text_y)

    def size_hint(self):
        return self.label.w, self.label.h

    def on_mouse_down(self, x, y):
        self.bg_color = self.active_bg_color

    def set_inactive(self):
        self.bg_color = self.inactive_bg_color

    def on_mouse_up(self, x, y):
        self.clicked(x, y)
        self.set_inactive()

    def no_hover(self, x, y):
        self.set_inactive()


class _CheckboxPanel(Panel, CheckboxPanel):
    """Класс окошка флажка, при нажатии изменяет атрибут родителя checked на
    противоположный."""
    def __init__(self, x, y, size, parent: Checkbox, groups=()):
        super().__init__(parent, groups)
        self.bg_color = CHECKBOX_BG_COLOR
        self.bound = CHECKBOX_BOUND
        self.set_geometry(x, y, size, size)

    @property
    def checked(self):
        return self.parent.checked

    def on_mouse_down(self, x, y):
        self.parent.checked = not self.checked


class Checkbox(UIElement, Checkbox):
    """Класс флажка с текстом."""
    def __init__(self, text='', parent=None, groups=()):
        super().__init__(parent, groups)
        self._text = ''
        self._groups = groups
        self._label = Label(text, parent=self, groups=groups)
        self._box = _CheckboxPanel(0, 0, self._label.h, self,
                                   self._groups)
        self._update_box()
        self.checked = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._label.text = value
        self._update_box()

    def _update_box(self):
        box_x = self._label.x + self._label.w + CHECKBOX_OFFSET
        box_y = self._label.y
        self._box.set_pos(box_x, box_y)
        self._rect.size = (self._box.rect.x - self._label.rect.x,
                           self._box.rect.y - self._label.rect.y)
        self._w, self._h = self._rect.size
