import pygame as pg
import random

from .. import state_machine
from ..components import data
from ..components.armory import Armory
from ..components.buttons import Button
from ..components.item import Item
from ..components.label import Label


class Reward(state_machine._State):
    def start(self):
        items = self.create_items()
        armory_items = [[items[0], items[1]], [items[2], items[3]]]
        self.add_items(items)
        self.armory = Armory(armory_items, center=(500, 300))
        self.title = Label('REWARDS', 45, font_name='Amaranth-Bold',
                           center=(500, 75))
        self.continue_button = Button(
            'CONTINUE', 30, self.button_click, font_name='Amaranth-Bold',
            center=(500, 550))

    def create_items(self):
        items = []
        if random.randint(1, 2) == 1:
            items.append(Item(random.choice(data.CONSUMABLE_ITEMS)))
        else:
            items.append(Item(random.choice(data.COMMON_ITEMS)))
        items.append(Item(random.choice(data.RARE_ITEMS)))
        items.append(Item(random.choice(data.COMMON_ITEMS)))
        items.append(Item(random.choice(data.COMMON_ITEMS)))
        random.shuffle(items)
        return items

    def add_items(self, items):
        if not items:
            return
        for row_num in range(len(self.persist['armory_items'])):
            for col_num in range(len(self.persist['armory_items'][row_num])):
                if self.persist['armory_items'][row_num][col_num] is None:
                    item = items.pop(0)
                    self.persist['armory_items'][row_num][col_num] = item
                    if not items:
                        return

    def update_tooltip(self):
        self.tooltip = None
        items = [item_box.item for item_box in self.armory.item_boxes
                 if item_box.item is not None]
        for item in items:
            if item.rect.collidepoint(pg.mouse.get_pos()):
                self.tooltip = item.create_tooltip()

    def button_click(self, name):
        self.finish()

    def click(self):
        self.continue_button.click()

    def finish(self):
        self.next = 'LOBBY'
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click()

    def draw(self, surface):
        surface.fill(data.BG_COLOR)
        self.title.draw(surface)
        self.armory.draw(surface)
        self.continue_button.draw(surface)
        if self.tooltip:
            self.tooltip.draw(surface)

    def update(self, surface, dt):
        self.continue_button.update()
        self.update_tooltip()
        self.draw(surface)
