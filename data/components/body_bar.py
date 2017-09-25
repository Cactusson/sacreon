import pygame as pg

from .. import tools
from . import data
from .health_bar import HealthBar
from .status import Status


class BodyBar:
    def __init__(self, body):
        self.body = body
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.health_bar = HealthBar(self.body)
        self.status = Status(self.body)
        self.turn_icon = None

    def create_image(self):
        image = tools.transparent_surface(
            data.BODY_BAR_WIDTH, data.BODY_BAR_HEIGHT)
        return image

    def shift_rect(self):
        midbottom = (self.body.rect.center[0],
                     self.body.rect.top - data.BODY_BAR_GAP)
        self.rect.midbottom = midbottom
        self.health_bar.rect.topleft = self.rect.topleft
        self.status.rect.topleft = (self.rect.x + data.ICON_SIZE,
                                    self.rect.y + data.HEALTH_BAR_HEIGHT)
        self.status.update_positions_of_effects()
        if self.turn_icon:
            self.turn_icon.rect.topleft = (
                self.rect.x, self.health_bar.rect.bottom + 1)

    def update_health_bar(self):
        self.health_bar.update_image()

    def create_turn_icon(self):
        self.turn_icon = pg.sprite.Sprite()
        self.turn_icon.image = data.TURN_IMAGE
        self.turn_icon.rect = self.turn_icon.image.get_rect()

    def delete_turn_icon(self):
        self.turn_icon = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.health_bar.draw(surface)
        self.status.draw(surface)
        if self.turn_icon:
            surface.blit(self.turn_icon.image, self.turn_icon.rect)

    def update(self):
        self.shift_rect()
