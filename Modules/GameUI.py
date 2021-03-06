"""Содержит классы игрового интерфейса."""

from numbers import Number

from multipledispatch import dispatch  # Модуль для "перегрузки" функций

from Modules import SpriteGroups
from Modules.GameUIHeaders import *


class UIElement(pygame.sprite.Sprite, UIElement):
    """Абастрактный класс элемента интерфейса."""

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
        for child in self.children:
            child.show()

    def hide(self):
        self._is_active = False
        for child in self.children:
            child.hide()

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
        if not self.is_active:
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
        """Вызывается при входе курсора в границы элемента."""
        pass

    def on_mouse_up(self, x, y):
        pass

    def on_mouse_down(self, x, y):
        pass

    def no_hover(self, x, y):
        """Вызывается при выходе курсора из-за границ элемента."""
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
        self.parent.check_state_changed(self.checked)


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

    def set_checked(self, checked: bool):
        self.checked = checked
        self.check_state_changed(checked)

    def check_state_changed(self, state):
        pass


class Bar(Panel):
    """Бар (по типу загрузочного бара)."""

    def __init__(self, parent=None, groups=()):
        super().__init__(*groups, parent=parent)
        self.bg_color = BAR_LIGHT_COLOR
        self.bound = 0
        self._inner_panel = Panel(self, groups)
        self._inner_panel.bg_color = BAR_COLOR
        self._inner_panel.bound = 0
        self._bar_bg = Panel(self._inner_panel, groups)
        self._bar_bg.bound = 0
        self._bar_bg.bg_color = BAR_BG_COLOR
        self._bar = Panel(self._bar_bg, groups)
        self._bar.bg_color = BAR_BG_COLOR
        self._bar.bound = 0
        self._bar_w = 0
        self._value = 100

    @property
    def bar_color(self):
        return self._bar.bg_color

    @bar_color.setter
    def bar_color(self, value):
        self._bar.bg_color = value

    def resize(self, w, h):
        super().resize(w, h)
        self._inner_panel.set_geometry(self.x + LIGHT_WIDTH,
                                       self.y + LIGHT_WIDTH,
                                       w - LIGHT_WIDTH,
                                       h - LIGHT_WIDTH)
        self._bar_w = w - BAR_WIDTH * 2
        self._bar_bg.set_geometry(self.x + BAR_WIDTH - LIGHT_WIDTH,
                                  self.y + BAR_WIDTH - LIGHT_WIDTH,
                                  self._bar_w,
                                  h - BAR_WIDTH * 2)
        self._bar.resize(int(self._bar_w * self._value / 100), self._bar_bg.h)

    def _update_bar(self):
        self._bar.resize(int(self._bar_w * self._value / 100), self._bar_bg.h)

    @dispatch(pygame.rect.Rect)
    def set_geometry(self, rect):
        self._rect = rect
        self._update_children_pos()

    @dispatch(Number, Number, Number, Number)
    def set_geometry(self, x, y, w, h):
        self.resize(w, h)
        self.set_pos(x, y)
        self._update_bar()

    @property
    def value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        if self._value < 0:
            self._value = 0
        self._update_bar()

    @value.setter
    def value(self, value):
        self._set_value(value)


class HookedBar(Bar):
    """Цепляющийся бар. При инициализации и вызове update устанавливает значение
    self.hook_value(self.hook).
    hook - значение, к которому "цепляется" бар;
    hook_value - функция, по которой бар вычисляет собственное значение;
    max_hook_value - максимально возможное значение self.hook_value(self.hook).
    """

    def __init__(self, hook, hook_value: lambda x: x, max_hook_value,
                 parent=None, groups=()):
        super().__init__(*groups, parent=parent)
        self.max_hook_value = max_hook_value
        self.hook = hook
        self.hook_value = hook_value
        self.value = self.hook_value(self.hook)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._set_value(value / self.max_hook_value * 100)

    def update(self, *args):
        super().update(*args)
        self.value = self.hook_value(self.hook)


class LeftTopHookedBar(HookedBar):
    """Класс бара, привязанного к левому верхнему углу экрана. Наследован от
    hooked_bar. В конструкте принимает аргумент pos - позиция бара
    (начинается с 0) и аргументы для конструктора HookedBar."""

    def __init__(self, pos, hook, hook_value: lambda x: x,
                 max_hook_value, parent=None, groups=()):
        super().__init__(hook, hook_value, max_hook_value, *groups,
                         parent=parent)
        x = LEFT_TOP_BAR_MARGIN_LEFT
        y = (LEFT_TOP_BAR_MARGIN_TOP +
             pos * (LEFT_TOP_BAR_HEIGHT + LEFT_TOP_BAR_SPACING))
        self.set_geometry(x, y, LEFT_TOP_BAR_WIDTH, LEFT_TOP_BAR_HEIGHT)


class HPBar(LeftTopHookedBar):
    """Полоса здоровья."""

    def __init__(self, hero, max_hp, parent=None, groups=()):
        super().__init__(HP_BAR_POS, hero, lambda h: h.hp, max_hp, *groups,
                         parent=parent)
        self.bar_color = HP_BAR_COLOR


class StaminaBar(LeftTopHookedBar):
    """Полоса выносливости."""

    def __init__(self, hero, max_stamina, parent=None, groups=()):
        super().__init__(STAMINA_BAR_POS, hero, lambda h: h.stamina,
                         max_stamina, *groups, parent=parent)
        self.bar_color = STAMINA_BAR_COLOR
