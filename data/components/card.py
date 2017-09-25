import pygame as pg

from . import data
from .label import Label
from .multilabel import MultiLabel


class Card:
    WIDTH = 225
    HEIGHT = 150
    LEFT_TOPLEFT = (0, 450)
    RIGHT_TOPLEFT = (775, 450)
    BODY_IMAGE_TOPLEFT = (10, 30)
    BODY_NAME_CENTER = (WIDTH // 2, 20)
    LABELS_TOPLEFT = (95, 37)
    LEVEL_LABEL_CENTER = (38, 100)
    XP_LABEL_CENTER = (38, 125)
    NAME_FONT_SIZE = 22
    FONT_SIZE = 15
    GAP = 5
    BG_COLOR = pg.Color('#9DD3CC')
    GOOD_COLOR = pg.Color('#388E3C')
    BAD_COLOR = pg.Color('#D53939')

    def __init__(self, side):
        self.image = None
        self.body = None
        if side == 'LEFT':
            self.topleft = self.LEFT_TOPLEFT
        elif side == 'RIGHT':
            self.topleft = self.RIGHT_TOPLEFT

    def create_image(self):
        image = pg.Surface((self.WIDTH, self.HEIGHT)).convert()
        image.fill(self.BG_COLOR)
        image.blit(self.body.image, self.BODY_IMAGE_TOPLEFT)
        labels = self.create_labels()
        for label in labels:
            label.draw(image)
        return image

    def create_labels(self):
        labels = []
        if self.body.faction == 'GOOD':
            color = self.GOOD_COLOR
            level = self.body.level
            xp = self.body.xp
            xp_needed = self.body.needed_exp()
            level_label = Label(
                'LVL {}'.format(level), self.FONT_SIZE,
                center=self.LEVEL_LABEL_CENTER)
            labels.append(level_label)
            if level < data.MAX_LEVEL:
                xp_label = Label(
                    '({}/{})'.format(xp, xp_needed), self.FONT_SIZE,
                    center=self.XP_LABEL_CENTER)
                labels.append(xp_label)
        elif self.body.faction == 'BAD':
            color = self.BAD_COLOR
        name_label = Label(
            self.body.name, self.NAME_FONT_SIZE, color=color,
            font_name='Amaranth-Bold', center=self.BODY_NAME_CENTER)
        texts = []
        health = 'HEALTH: {}/{}'.format(
            self.body.current_health, self.body.health)
        attack = 'ATTACK: {}'.format(self.body.attack)
        defense = 'DEFENSE: {}'.format(self.body.defense)
        speed = 'SPEED: {}'.format(self.body.speed)
        if self.body.mana > 0:
            mana = 'MANA: {}/{}'.format(
                self.body.current_mana, self.body.mana)
            texts = [health, mana, attack, defense, speed]
        else:
            texts = [health, attack, defense, speed]
        multilabel = MultiLabel(texts, self.FONT_SIZE, self.GAP,
                                topleft=self.LABELS_TOPLEFT)
        labels.extend([name_label, multilabel])
        return labels

    def get_body(self, body):
        self.body = body
        self.image = self.create_image()

    def update_image(self):
        self.image = self.create_image()

    def take_down(self):
        self.body = None
        self.image = None

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.topleft)
