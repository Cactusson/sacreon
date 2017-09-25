import pygame as pg

from .animation import Animation
from .label import Label
from .task import Task


class FlyingLabel(Label):
    def __init__(self, text, font_size=25, font_name=None, color=None,
                 center=None, topleft=None, start=True):
        Label.__init__(self, text, font_size, font_name, color, center,
                       topleft, antialias=False)
        self.distance = 50
        self.duration = 1000
        self.animations = pg.sprite.Group()
        self.tasks = pg.sprite.Group()
        self.alpha = 255
        self.alpha_step = 40
        self.image.set_alpha(self.alpha)
        if start:
            self.start()

    def start(self):
        x = self.rect.x
        y = self.rect.y - self.distance
        animation = Animation(
            x=x, y=y, duration=self.duration, round_values=True,
            transition='out_quad')
        animation.callback = self.disappear
        animation.start(self.rect)
        self.animations.add(animation)

    def disappear(self):
        if self.alpha == 0:
            self.kill()
            return
        self.alpha = max(0, self.alpha - self.alpha_step)
        self.image.set_alpha(self.alpha)
        task = Task(self.disappear, 100)
        self.tasks.add(task)

    def update(self, dt):
        self.animations.update(dt * 1000)
        self.tasks.update(dt * 1000)
