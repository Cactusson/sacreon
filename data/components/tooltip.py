import pygame as pg

from .. import prepare
from . import data
from .label import Label
from .multiline_label import MultilineLabel


tooltip_cache = {}


def create_tooltip(text, position):
    text = tuple(text)
    if text in tooltip_cache:
        tooltip = tooltip_cache[text]
    else:
        tooltip = Tooltip(text)
        tooltip_cache[text] = tooltip
    tooltip.shift_position(position)
    return tooltip


class Tooltip:
    def __init__(self, text):
        self.image = self.create_image(text)
        self.rect = self.image.get_rect()

    def shift_position(self, position):
        bottomleft = position[0] + 10, position[1] - 10
        self.rect.bottomleft = bottomleft
        self.rect.clamp_ip(prepare.SCREEN_RECT)

    def calculate_size(self, text):
        labels = []
        for line in text:
            if len(line) > 30:
                label = MultilineLabel(
                    line, data.TOOLTIP_FONT_SIZE, align='left')
            else:
                label = Label(line, data.TOOLTIP_FONT_SIZE)
            labels.append(label)
        width = max([lbl.rect.width for lbl in labels])
        height = (sum([lbl.rect.height for lbl in labels]) +
                  (len(labels) - 1) * data.TOOLTIP_GAP)
        return width, height

    def create_image(self, text):
        width, height = self.calculate_size(text)
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#D6D88B'))
        topleft = [0, 0]
        for line in text:
            if len(line) > 30:
                label = MultilineLabel(
                    line, data.TOOLTIP_FONT_SIZE, topleft=topleft,
                    align='left')
            else:
                label = Label(line, data.TOOLTIP_FONT_SIZE, topleft=topleft)
            label.draw(image)
            topleft[1] += label.rect.height + data.TOOLTIP_GAP
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
