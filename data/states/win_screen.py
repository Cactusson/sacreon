import pygame as pg

from .. import state_machine
from ..components.buttons import Button
from ..components.label import Label


class WinScreen(state_machine._State):
    BG_COLOR = pg.Color('#7DCE94')
    TITLE_CENTER = (500, 250)
    BUTTON_CENTER = (500, 550)

    def start(self):
        self.title = Label('YOU WON!', 90, font_name='Amaranth-Bold',
                           center=self.TITLE_CENTER)
        self.button = Button('GOOD', 35, self.button_click,
                             center=self.BUTTON_CENTER)

    def finish(self):
        self.next = 'MAIN_MENU'
        self.done = True

    def button_click(self, name):
        self.finish()

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.button.click()

    def draw(self, surface):
        surface.fill(self.BG_COLOR)
        self.title.draw(surface)
        self.button.draw(surface)

    def update(self, surface, dt):
        self.button.update()
        self.draw(surface)
