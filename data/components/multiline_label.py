import pygame as pg

from .label import Label


class MultilineLabel(pg.sprite.Sprite):
    """
    Creates a single surface with multiple labels blitted to it.
    """
    def __init__(self, text, font_size, font_name=None, color=None,
                 center=None, topleft=None, bg=None, antialias=True,
                 char_limit=40, align='center', vert_space=0):
        pg.sprite.Sprite.__init__(self)
        lines = self.wrap_text(text, char_limit)
        labels = [Label(line, font_size, center=(0, 0),
                        font_name=font_name, color=color, bg=bg,
                        antialias=antialias) for line in lines]
        width = max([label.rect.width for label in labels])
        spacer = vert_space * (len(lines) - 1)
        height = sum([label.rect.height for label in labels])+spacer
        self.image = pg.Surface((width, height)).convert()
        self.image.set_alpha(0)
        self.image = self.image.convert_alpha()
        if center is not None:
            self.rect = self.image.get_rect(center=center)
        elif topleft is not None:
            self.rect = self.image.get_rect(topleft=topleft)
        else:
            self.rect = self.image.get_rect()
        aligns = {"left": {"left": 0},
                  "center": {"centerx": self.rect.width // 2},
                  "right": {"right": self.rect.width}}
        y = 0
        for label in labels:
            label.rect = label.image.get_rect(**aligns[align])
            label.rect.top = y
            label.draw(self.image)
            y += label.rect.height + vert_space

    def wrap_text(self, text, char_limit, separator=" "):
        """
        Splits a string into a list of strings no longer than char_limit.
        """
        words = text.split(separator)
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if len(word) + current_length <= char_limit:
                current_length += len(word) + len(separator)
                current_line.append(word)
            else:
                lines.append(separator.join(current_line))
                current_line = [word]
                current_length = len(word) + len(separator)
        if current_line:
            lines.append(separator.join(current_line))
        return lines

    def draw(self, surface):
        surface.blit(self.image, self.rect)
