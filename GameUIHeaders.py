from ColorPalette import *
from General import *

PANEL_BG_COLOR = TRADEWIND
PANEL_BOUND_COLOR = MINE_SHAFT
PANEL_BOUND = 4

LABEL_COLOR = ALTO
LABEL_COLOR_HOVER = CELERY
LABEL_ANTIALIAS = 1

BUTTON_INACTIVE_COLOR = FIORD
BUTTON_ACTIVE_COLOR = BAY_OF_MANY

CHECKBOX_BG_COLOR = FIORD
CHECKBOX_BOUND = 2
CHECKBOX_OFFSET = 2

CHECKBOX_PANEL_LINE_COLOR = ALTO

FONT_FILENAME = data_path('font.ttf')
FONT_SIZE = 20


class UIElement:
    pass


class Group(UIElement):
    pass


class Panel(UIElement):
    pass


class Label(UIElement):
    pass


class LabelButton(Label):
    pass


class Button(Panel):
    pass


class Checkbox(UIElement):
    pass


class CheckboxPanel(Panel):
    pass
