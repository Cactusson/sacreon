import pygame as pg


class Cage:
    WIDTH = 140
    HEIGHT = 140
    COLOR_FRAME = pg.Color('black')
    COLOR_IDLE = pg.Color('#4B2C34')
    COLOR_HOVER = pg.Color('#C31207')

    def __init__(self, center):
        self.image_idle, self.image_hover = self.create_images()
        self.image = self.image_idle
        self.rect = self.image.get_rect(center=center)
        self.hover = False
        self.victim = None

    def create_images(self):
        image = pg.Surface((self.WIDTH, self.HEIGHT)).convert()
        image.fill(self.COLOR_FRAME)
        gap = 10
        rect = (gap, gap, self.WIDTH - gap * 2, self.HEIGHT - gap * 2)
        image_idle = image.copy()
        image_idle.fill(self.COLOR_IDLE, rect)
        image_hover = image.copy()
        image_hover.fill(self.COLOR_HOVER, rect)
        return image_idle, image_hover

    def get_victim(self, victim):
        self.victim = victim
        self.victim.rect.center = self.rect.center

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.victim:
            self.victim.draw(surface)

    def update(self):
        """
        Check if the button is hovered.
        """
        if self.victim is None:
            return
        hover = self.rect.collidepoint(pg.mouse.get_pos())
        if hover:
            self.image = self.image_hover
        else:
            self.image = self.image_idle
        self.hover = hover
