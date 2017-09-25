import pygame as pg

from .label import Label
from .tooltip import create_tooltip


class AttributeLabel(Label):
    def __init__(self, text, font_size, font_name=None, color=None,
                 center=None, topleft=None, topright=None, bg=None,
                 width=None, height=None, antialias=True, base=0, bonus=0):
        if bonus != 0 and bonus != '0%':
            color = pg.Color('#1B8057')
        Label.__init__(self, text, font_size, font_name, color,
                       center, topleft, topright, bg, width, height, antialias)
        self.base = base
        self.bonus = bonus

    def create_tooltip(self):
        base = 'Base: {}'.format(self.base)
        if self.bonus != 0 and self.bonus != '0%':
            bonus = 'Bonus: +{}'.format(self.bonus)
            text = [base, bonus]
        else:
            text = [base]
        tooltip = create_tooltip(text, self.rect.topright)
        return tooltip
