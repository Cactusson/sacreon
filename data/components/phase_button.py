import pygame as pg

from . import data
from .tooltip import create_tooltip


class PhaseButton(pg.sprite.Sprite):
    COLORS = {
        'IDLE': pg.Color('black'),
        'HOVER': pg.Color('white'),
        'ACTIVE': pg.Color('green'),
        'BLOCKED': pg.Color('grey'),
    }
    BG = {
        'IDLE': None,
        'HOVER': pg.Color('purple'),
        'ACTIVE': None,
        'BLOCKED': None,
    }

    def __init__(self, name, call, font_name=None, topleft=None,
                 center=None, state='BLOCKED'):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.call = call
        self.hovered = False
        self.state = state
        self.images = data.BUTTONS[self.name]
        self.image = self.images[self.state]
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            self.rect = self.image.get_rect()

    def create_tooltip(self):
        text = [self.name]
        tooltip = create_tooltip(text, self.rect.topright)
        return tooltip

    def hover(self):
        if self.state == 'IDLE':
            self.state = 'HOVER'
            self.image = self.images[self.state]

    def unhover(self):
        if self.state == 'HOVER':
            self.state = 'IDLE'
            self.image = self.images[self.state]

    def click(self):
        if self.hovered:
            self.call(self)

    def update(self):
        """
        Check if the button is hovered.
        """
        if self.state == 'BLOCKED':
            return
        hover = self.rect.collidepoint(pg.mouse.get_pos())
        if hover:
            self.hover()
        else:
            self.unhover()
        self.hovered = hover

    def draw(self, surface):
        surface.blit(self.image, self.rect)
