import pygame as pg
import random

from .. import state_machine
from ..components.cage import Cage
from ..components.multiline_label import MultilineLabel


class Sacreon(state_machine._State):
    CAGE_ONE_CENTER = (125, 475)
    CAGE_TWO_CENTER = (875, 475)
    LABEL_CENTER = (500, 235)
    TEXT_COLOR = pg.Color('#872341')

    def start(self):
        self.squad = self.persist['squad']
        self.victims, self.others = self.divide_squad()
        self.bodies = self.victims + self.others
        self.cages = self.create_cages()
        text = 'You will have to sacrifice one of your own to move forward.'
        self.text = MultilineLabel(
            text, 30, char_limit=30, center=self.LABEL_CENTER,
            color=self.TEXT_COLOR)

    def divide_squad(self):
        bodies = [char.create_body() for char in self.squad]
        victim_one = random.choice(bodies)
        bodies.remove(victim_one)
        if not bodies:
            return [victim_one], []
        victim_two = random.choice(bodies)
        bodies.remove(victim_two)
        for indx, body in enumerate(bodies):
            body.rect.center = (100 + 100 * indx, 50)
        return [victim_one, victim_two], bodies

    def create_cages(self):
        cages = [Cage(self.CAGE_ONE_CENTER), Cage(self.CAGE_TWO_CENTER)]
        for victim, cage in zip(self.victims, cages):
            cage.get_victim(victim)
        return cages

    def kill(self, victim):
        self.squad = [char for char in self.squad if char != victim.character]
        self.change_state('LOBBY')

    def left_click(self):
        for cage in self.cages:
            if cage.hover:
                self.kill(cage.victim)

    def right_click(self):
        for body in self.bodies:
            if body.rect.collidepoint(pg.mouse.get_pos()):
                self.change_state('CHARACTER_VIEW', character=body.character)

    def change_state(self, new_state, **kwargs):
        if new_state == 'CHARACTER_VIEW':
            character = kwargs['character']
            self.persist['character_to_view'] = character
        elif new_state == 'LOBBY':
            self.persist['squad'] = self.squad
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'LOBBY':
            self.start()

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click()
            elif event.button == 3:
                self.right_click()

    def draw(self, surface):
        surface.fill(pg.Color('#779977'))
        self.text.draw(surface)
        for cage in self.cages:
            cage.draw(surface)
        for body in self.others:
            body.draw(surface)

    def update(self, surface, dt):
        self.draw(surface)
        for cage in self.cages:
            cage.update()
