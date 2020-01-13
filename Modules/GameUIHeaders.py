from Modules.ColorPalette import *
from Modules.General import *


"""Заголовочный файл по типу таковых в C++. Необходим для распознавания класса 
UI при отрисовке в SpriteGroups. Также содержат некоторые константы, которые 
используются в модулях GameUI и SpriteGroups."""
# Просто имортировать модуль GameUI в SpriteGroups невозможно из-за того, что
# в GameUI импортируется модуль SpriteGroups.

# Некоторые классы имеют функцию __init__. Это сделано для того чтобы объявить
# наличие тех или иных аттрибутов у класса, чтобы впоследствии в SpriteGroups
# не было предупреждений насчёт отсутсвия таких аттрибутов у класса.

PANEL_BG_COLOR = TRADEWIND
PANEL_BOUND_COLOR = MINE_SHAFT
PANEL_BOUND = 4

LABEL_COLOR = ALTO
LABEL_COLOR_HOVER = CELERY
LABEL_ANTIALIAS = 1

BUTTON_INACTIVE_COLOR = FIORD
BUTTON_ACTIVE_COLOR = BAY_OF_MANY

CHECKBOX_BG_COLOR = FIORD
CHECKBOX_BOUND = 3
CHECKBOX_OFFSET = 2

CHECKBOX_PANEL_LINE_COLOR = ALTO
CHECKBOX_PANEL_LINE_WIDTH = 4

BAR_LIGHT_COLOR = ALTO
BAR_COLOR = BOULDER
LIGHT_WIDTH = 1
BAR_WIDTH = 2
BAR_BG_COLOR = BLACK

LEFT_TOP_BAR_MARGIN_LEFT = LEFT_TOP_BAR_MARGIN_TOP = 30
LEFT_TOP_BAR_HEIGHT = 20
LEFT_TOP_BAR_WIDTH = 150
LEFT_TOP_BAR_SPACING = 10

HP_BAR_COLOR = APPLE
HP_BAR_POS = 0

STAMINA_BAR_COLOR = INDIGO
STAMINA_BAR_POS = 1

FONT_FILENAME = data_path('font.ttf')
FONT_SIZE = 20


class UIElement:
    def __init__(self, parent=None, groups=()):
        self.rect = None


class Group(UIElement):
    pass


class Panel(UIElement):
    def __init__(self, parent=None, groups=()):
        super().__init__()
        self.bound, self.bg_color, self.bound_color = [None] * 3


class Label(UIElement):
    def __init__(self, text='', parent=None, groups=()):
        super().__init__()
        self.text_render = None


class LabelButton(Label):
    def __init__(self, text='', parent=None, groups=()):
        super().__init__()
    pass


class Button(Panel):
    def __init__(self, text='', parent=None, groups=()):
        super().__init__()
    pass


class Checkbox(UIElement):
    def __init__(self, x, y, size, parent, groups=()):
        super().__init__()


class CheckboxPanel(Panel):
    def __init__(self, text='', parent=None, groups=()):
        super().__init__()
        self.checked = None
