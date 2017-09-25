import pygame as pg

from .. import tools
from . import data


class Hoop:
    def __init__(self):
        self.image = self.create_image()
        self.rect = self.image.get_rect()

    def create_image(self):
        size = int(1.6 * max(data.BODY_SIZE))
        image = tools.transparent_surface(size, size)
        width = 7
        center = size // 2, size // 2
        radius = size // 2
        pg.draw.circle(image, pg.Color('#CA3E6B'), center, radius, width)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
