from .. import tools
from .label import Label


class MultiLabel:
    """
    Bunch of labels in a column.
    """
    def __init__(self, texts, font_size, gap, font_name=None, colors=None,
                 center=None, topleft=None, bg=None):
        if len(texts) == 1:
            raise Exception(
                'There should be more than one line of text for MultiLabel.')
        self.image = self.create_image(
            texts, colors, font_size, gap, font_name, bg)
        if topleft:
            self.rect = self.image.get_rect(topleft=topleft)
        elif center:
            self.rect = self.image.get_rect(center=center)
        else:
            self.rect = self.image.get_rect()

    def create_image(self, texts, colors, font_size, gap, font_name, bg):
        if colors is None:
            colors = [None for _ in range(len(texts))]
        labels = [
            Label(text, font_size, font_name=font_name, color=color, bg=bg)
            for text, color in zip(texts, colors)]
        width = max([label.rect.width for label in labels])
        height = (sum([label.rect.height for label in labels]) +
                  gap * len(labels) - 1)
        image = tools.transparent_surface(width, height)
        topleft = [0, 0]
        for label in labels:
            label.rect.topleft = topleft
            label.draw(image)
            topleft[1] += label.rect.height + gap
        return image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
