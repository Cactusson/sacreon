import pygame as pg

from .. import prepare


class Label(pg.sprite.Sprite):
    """
    Just some text.
    """
    def __init__(self, text, font_size, font_name=None, color=None,
                 center=None, topleft=None, topright=None, bg=None, width=None,
                 height=None, antialias=True):
        pg.sprite.Sprite.__init__(self)
        if font_name is not None:
            self.font = pg.font.Font(prepare.FONTS[font_name], font_size)
        else:
            self.font = pg.font.Font(
                prepare.FONTS['ABeeZee-Regular'], font_size)
        if color is not None:
            self.color = color
        else:
            self.color = pg.Color('black')
        self.text = text
        self.image = self.make_image(antialias, bg, width, height)
        if center:
            self.rect = self.image.get_rect(center=center)
        elif topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        elif topright:
            self.rect = self.image.get_rect(topright=topright)
        else:
            self.rect = self.image.get_rect()

    def make_image(self, antialias, bg, width, height):
        if width and height:
            image = pg.Surface((width, height)).convert()
            if bg:
                image.fill(bg)
            else:
                image.set_alpha(0)
                image = image.convert_alpha()
            text = self.font.render(self.text, antialias, self.color)
            rect = text.get_rect(center=(width // 2, height // 2))
            image.blit(text, rect)
        else:
            image = self.font.render(self.text, antialias, self.color, bg)
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
