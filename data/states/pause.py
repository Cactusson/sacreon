import pygame as pg

from .. import state_machine
from ..components.buttons import Button
from ..components.label import Label


class Pause(state_machine._State):
    WIDTH = 300
    HEIGHT = 400
    FRAME = 30
    COLOR = pg.Color('#A5E9E1')
    FRAME_COLOR = pg.Color('#388186')
    CENTER = (500, 300)
    TITLE_CENTER = (500, 200)
    RESUME_CENTER = (500, 300)
    QUIT_CENTER = (500, 400)

    def start(self):
        self.subsurface = pg.display.get_surface().copy()
        self.cover = pg.Surface(self.subsurface.get_size()).convert()
        self.cover.set_alpha(100)
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.CENTER)
        self.title = Label('PAUSE', 40, font_name='Amaranth-Bold',
                           center=self.TITLE_CENTER)
        self.buttons = self.create_buttons()

    def create_image(self):
        image = pg.Surface((self.WIDTH, self.HEIGHT)).convert()
        image.fill(self.FRAME_COLOR)
        rect = (self.FRAME, self.FRAME, self.WIDTH - self.FRAME * 2,
                self.HEIGHT - self.FRAME * 2)
        image.fill(self.COLOR, rect)
        return image

    def create_buttons(self):
        resume = Button('RESUME', 30, self.button_click,
                        center=self.RESUME_CENTER)
        quit = Button('QUIT', 30, self.button_click,
                      center=self.QUIT_CENTER)
        return [resume, quit]

    def button_click(self, name):
        if name == 'RESUME':
            self.change_state('FIGHT')
        elif name == 'QUIT':
            self.change_state('MAIN_MENU')

    def change_state(self, new_state):
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.change_state('FIGHT')
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    button.click()

    def draw(self, surface):
        surface.blit(self.subsurface, (0, 0))
        surface.blit(self.cover, (0, 0))
        surface.blit(self.image, self.rect)
        self.title.draw(surface)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, dt):
        for button in self.buttons:
            button.update()
        self.draw(surface)
