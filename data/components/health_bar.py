import pygame as pg

from . import data
from .tooltip import create_tooltip


class HealthBar:
    def __init__(self, body):
        self.body = body
        self.update_image()
        self.rect = self.image.get_rect()

    def update_image(self):
        image = pg.Surface(
            (data.HEALTH_BAR_WIDTH, data.HEALTH_BAR_HEIGHT)).convert()
        image.fill(data.HEALTH_BAR_RED)
        fraction = self.body.current_health / self.body.health
        green_width = int(data.HEALTH_BAR_WIDTH * fraction)
        if green_width > 0:
            green_image = pg.Surface((green_width, 20)).convert()
            green_image.fill(data.HEALTH_BAR_GREEN)
            image.blit(green_image, (0, 0))
        self.image = image

    def create_tooltip(self):
        health = '{}/{}'.format(self.body.current_health, self.body.health)
        text = [health]
        tooltip = create_tooltip(text, self.rect.topright)
        return tooltip

    def draw(self, surface):
        surface.blit(self.image, self.rect)
