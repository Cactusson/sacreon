import pygame as pg

from .. import state_machine
from ..components.buttons import Button
from ..components.label import Label


class MainMenu(state_machine._State):
    BG_COLOR = pg.Color('#A5E9E1')
    TITLE_COLOR = pg.Color('#388186')
    TITLE_CENTER = (500, 125)
    NEW_GAME_CENTER = (500, 325)
    QUIT_CENTER = (500, 450)

    def start(self):
        self.title = Label('SACREON', 90, font_name='Amaranth-Bold',
                           color=self.TITLE_COLOR, center=self.TITLE_CENTER)
        self.buttons = self.create_buttons()

    def create_buttons(self):
        new_game = Button(
            'NEW GAME', 35, self.button_click, center=self.NEW_GAME_CENTER)
        quit = Button('QUIT', 35, self.button_click, center=self.QUIT_CENTER)
        return [new_game, quit]

    def button_click(self, name):
        if name == 'NEW GAME':
            self.change_state('LOBBY')
        elif name == 'QUIT':
            self.quit = True

    def change_state(self, new_state):
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    button.click()

    def draw(self, surface):
        surface.fill(self.BG_COLOR)
        self.title.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, dt):
        for button in self.buttons:
            button.update()
        self.draw(surface)
