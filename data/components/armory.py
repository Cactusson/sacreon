import pygame as pg

from . import data
from .item_box import ItemBox


class Armory:
    def __init__(self, items, topleft=None, center=None):
        if not isinstance(items[0], list):
            items = [items]
        self.height = len(items)
        self.width = len(items[0])
        self.image = self.create_image()
        if topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        elif center:
            self.rect = self.image.get_rect(center=center)
        else:
            self.rect = self.image.get_rect()
        self.grid = self.create_grid(items)
        self.item_boxes = [box for row in self.grid for box in row]

    def create_image(self):
        width = (data.ITEM_BOX_SIZE * self.width +
                 data.ITEM_BOX_GAP * (self.width + 1))
        height = (data.ITEM_BOX_SIZE * self.height +
                  data.ITEM_BOX_GAP * (self.height + 1))
        image = pg.Surface((width, height)).convert()
        image.fill(data.ARMORY_COLOR)
        return image

    def create_grid(self, items):
        grid = []
        for row_num, items_row in enumerate(items):
            row = []
            for col_num, item in enumerate(items_row):
                x = (self.rect.x + data.ITEM_BOX_SIZE * col_num +
                     data.ITEM_BOX_GAP * (col_num + 1))
                y = (self.rect.y + data.ITEM_BOX_SIZE * row_num +
                     data.ITEM_BOX_GAP * (row_num + 1))
                item_box = ItemBox(item, (x, y))
                row.append(item_box)
            grid.append(row)
        return grid

    def get_items(self):
        if self.height == 1:
            return [item_box.item for item_box in self.item_boxes]
        else:
            return [[item_box.item for item_box in row] for row in self.grid]

    def try_to_add_item(self, item):
        for item_box in self.item_boxes:
            if item_box.item is not None:
                continue
            if item_box.rect.collidepoint(pg.mouse.get_pos()):
                item_box.add_item(item)
                return True
        return False

    def try_to_get_item(self):
        for item_box in self.item_boxes:
            if item_box.item is None:
                continue
            if (
                item_box.item.rect.collidepoint(pg.mouse.get_pos())
                and item_box is not None
            ):
                return item_box.remove_item(), item_box
        return None, None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for item_box in self.item_boxes:
            item_box.draw(surface)
