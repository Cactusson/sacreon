import pygame as pg

from . import data


class ItemBox:
    def __init__(self, item, topleft):
        self.image = self.create_image()
        self.rect = self.image.get_rect(topleft=topleft)
        if item is not None:
            self.add_item(item)
        else:
            self.item = None

    def create_image(self):
        width = height = data.ITEM_BOX_SIZE
        image = pg.Surface((width, height)).convert()
        image.fill(data.ITEM_BOX_COLOR)
        return image

    def add_item(self, item):
        self.item = item
        self.item.rect.center = self.rect.center

    def remove_item(self):
        if self.item is None:
            return
        item = self.item
        self.item = None
        return item

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.item:
            self.item.draw(surface)
