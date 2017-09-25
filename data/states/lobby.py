import pygame as pg
import random

from .. import state_machine
from ..components import data
from ..components.buttons import Button
from ..components.character import Character
from ..components.multilabel import MultiLabel


class Lobby(state_machine._State):

    def first_start(self):
        self.clean_items()
        self.squad = self.create_squad()
        self.map = data.MAP
        self.map_index = 0
        self.buttons = self.create_buttons()
        self.start()

    def start(self):
        self.bodies = [char.create_body() for char in self.squad]
        for indx, body in enumerate(self.bodies):
            body.rect.center = (100 + 100 * indx, 50)
        colors = [
            (pg.Color('#FF006C') if indx == self.map_index else
             pg.Color('black')) for indx in range(len(self.map))]
        self.map_labels = MultiLabel(
            self.map, 25, 20, colors=colors, center=(500, 300))

    def create_squad(self):
        people = data.HEROES.copy()
        random.shuffle(people)
        names = people[:data.ROSTER_AMOUNT]
        squad = [Character(name) for name in names]
        return squad

    def create_buttons(self):
        back = Button('BACK', 30, self.button_call, center=(50, 550))
        armory = Button('ARMORY', 30, self.button_call, center=(500, 550))
        go = Button('GO', 30, self.button_call, center=(950, 550))
        buttons = [back, armory, go]
        return buttons

    def clean_items(self):
        self.persist['armory_items'] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def move_to_next_location(self):
        self.clean_items()
        if self.map[self.map_index] == 'Dungeon':
            self.move_to_dungeon()
        elif self.map[self.map_index] == 'Sacreon':
            self.move_to_sacreon()

    def move_to_dungeon(self):
        dungeon_indx = self.map[:self.map_index].count('Dungeon')
        dungeon = data.DUNGEONS[dungeon_indx].copy()
        dungeon['monsters'] = [Character(name) for name in dungeon['monsters']]
        self.persist['squad'] = self.squad
        self.persist['dungeon_info'] = dungeon
        self.change_state('FIGHT')

    def move_to_sacreon(self):
        self.persist['squad'] = self.squad
        self.change_state('SACREON')

    def after_location(self):
        self.squad = self.persist['squad']
        if not self.squad:
            self.game_lost()
            return
        self.map_index += 1
        if self.map_index >= len(self.map):
            self.game_won()
            return
        if self.previous == 'FIGHT':
            self.give_reward()
        else:
            self.start()

    def game_lost(self):
        self.next = 'LOSE_SCREEN'
        self.done = True

    def game_won(self):
        self.next = 'WIN_SCREEN'
        self.done = True

    def give_reward(self):
        self.next = 'REWARD'
        self.done = True

    def button_call(self, name):
        if name == 'BACK':
            self.change_state('MAIN_MENU')
        elif name == 'ARMORY':
            self.change_state('ARMORY_VIEW')
        elif name == 'GO':
            self.move_to_next_location()

    def left_click(self):
        for button in self.buttons:
            button.click()

    def right_click(self):
        for body in self.bodies:
            if body.rect.collidepoint(pg.mouse.get_pos()):
                self.change_state('CHARACTER_VIEW', character=body.character)

    def change_state(self, new_state, **kwargs):
        if new_state == 'CHARACTER_VIEW':
            character = kwargs['character']
            self.persist['character_to_view'] = character
        elif new_state == 'ARMORY_VIEW':
            self.persist['bodies'] = self.bodies
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'MAIN_MENU':
            self.first_start()
        elif self.previous in ['FIGHT', 'SACREON']:
            self.after_location()
        elif self.previous == 'REWARD':
            self.start()

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click()
            elif event.button == 3:
                self.right_click()

    def draw(self, surface):
        surface.fill(pg.Color('#A4E5D9'))
        for body in self.bodies:
            body.draw(surface)
        self.map_labels.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, dt):
        for button in self.buttons:
            button.update()
        self.draw(surface)
