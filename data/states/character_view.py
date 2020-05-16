import pygame as pg

from .. import state_machine
from ..components import data
from ..components.armory import Armory
from ..components.attribute_label import AttributeLabel
from ..components.label import Label
from ..components.item import Item
from ..components.spell_book import SpellBook
from ..components.tooltip import create_tooltip
# from ..components.buttons import ButtonPic


class CharacterView(state_machine._State):
    WIDTH = 800
    HEIGHT = 500
    CENTER = (500, 300)
    IMAGE_TOPLEFT = (150, 180)
    NAME_CENTER = (500, 80)
    FEATURE_TEXT_CENTER = (500, 130)
    ATTR_TOP = 180
    ATTR_RIGHT = 435
    ATTR_LEFT = 445
    LEVEL_LABEL_TOPLEFT = (165, 295)
    ARMORY_LABEL_CENTER = (700, 180)
    ARMORY_CENTER = (700, 260)
    SPELL_BOOK_CENTER = (700, 440)
    SPELL_BOOK_LABEL_CENTER = (700, 360)
    ATTR_GAP = 10
    ATTR_FONT_SIZE = 20
    BG_COLOR = pg.Color('#D7C37A')

    def start(self):
        if 'body_to_view' in self.persist:
            self.body = self.persist['body_to_view']
            self.character = self.body.character
            del self.persist['body_to_view']
        elif 'character_to_view' in self.persist:
            self.body = None
            self.character = self.persist['character_to_view']
            del self.persist['character_to_view']
        self.underscreen = pg.display.get_surface().copy()
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.CENTER)
        self.character_image = self.create_character_image()
        if self.character.faction == 'GOOD':
            self.level_labels = self.create_level_labels()
        else:
            self.level_labels = []
        if self.character.spells:
            self.spell_book = SpellBook(
                self.character.spells, self.SPELL_BOOK_CENTER,
                self.character.level)
        else:
            self.spell_book = None
        self.labels = self.create_labels()
        labels, self.attributes_labels = self.create_attribute_labels()
        self.labels.extend(labels)
        items = [(Item(item.name) if item is not None else None)
                 for item in self.character.items]
        self.armory = Armory(items, center=self.ARMORY_CENTER)
        # self.close_button = ButtonPic()

    def create_image(self):
        image = pg.Surface((self.WIDTH, self.HEIGHT)).convert()
        image.fill(self.BG_COLOR)
        return image

    def create_character_image(self):
        width = height = 100
        image = pg.Surface((width, height)).convert()
        image.fill(pg.Color('#F5EDF7'))
        char_image = self.character.create_body().image
        char_rect = char_image.get_rect()
        char_rect.center = width // 2, height // 2
        image.blit(char_image, char_rect)
        return image

    def create_labels(self):
        name = Label(self.character.name, 35, font_name='Amaranth-Bold',
                     center=self.NAME_CENTER)
        feature = Label('Feature: ' + self.character.feature_text, 22,
                        center=self.FEATURE_TEXT_CENTER)
        armory = Label('ITEMS', 25, font_name='Amaranth-Bold',
                       center=self.ARMORY_LABEL_CENTER)
        labels = [name, feature, armory]
        if self.spell_book:
            spells = Label('SPELLS', 25, font_name='Amaranth-Bold',
                           center=self.SPELL_BOOK_LABEL_CENTER)
            labels.append(spells)
        return labels

    def create_level_labels(self):
        level_text = 'Level: {}'.format(self.character.level)
        self.level_label = Label(level_text, self.ATTR_FONT_SIZE,
                                 topleft=self.LEVEL_LABEL_TOPLEFT)
        labels = [self.level_label]
        if self.character.level < data.MAX_LEVEL:
            exp_text = 'XP: {}/{}'.format(self.character.xp,
                                          self.character.needed_exp())
            topleft = (self.LEVEL_LABEL_TOPLEFT[0],
                       self.LEVEL_LABEL_TOPLEFT[1] + 35)
            experience = Label(exp_text, self.ATTR_FONT_SIZE, topleft=topleft)
            labels.append(experience)
        return labels

    def create_attribute_labels(self):
        if self.body is not None:
            health = '{}/{}'.format(
                self.body.current_health, self.character.health)
            mana = '{}/{}'.format(
                self.body.current_mana, self.character.mana)
        else:
            health = '{}'.format(self.character.health)
            mana = '{}'.format(self.character.mana)
        base_health = self.character.base_health
        bonus_health = self.character.health - base_health
        base_mana = self.character.base_mana
        bonus_mana = self.character.mana - base_mana
        attack_value = self.body.attack if self.body else self.character.attack
        attack = '{}'.format(attack_value)
        base_attack = self.character.base_attack
        bonus_attack = attack_value - base_attack
        defense = '{}'.format(self.character.defense)
        base_defense = self.character.base_defense
        bonus_defense = self.character.defense - base_defense
        speed = '{}'.format(self.character.speed)
        base_speed = self.character.base_speed
        bonus_speed = self.character.speed - base_speed
        crit_value = self.body.crit_chance if self.body else self.character.crit_chance
        crit = '{}%'.format(crit_value)
        base_crit = '{}%'.format(self.character.base_crit_chance)
        bonus_crit = '{}%'.format(crit_value - self.character.base_crit_chance)
        stun = '{}%'.format(self.character.stun_chance)
        base_stun = '{}%'.format(self.character.base_stun_chance)
        bonus_stun = '{}%'.format(
            self.character.stun_chance - self.character.base_stun_chance)
        names = ['Health:', 'Mana:', 'Attack:', 'Defense:', 'Speed:',
                 'Crit chance:', 'Stun chance:']
        values = [health, mana, attack, defense, speed, crit, stun]
        bases = [base_health, base_mana, base_attack, base_defense, base_speed,
                 base_crit, base_stun]
        bonuses = [bonus_health, bonus_mana, bonus_attack, bonus_defense,
                   bonus_speed, bonus_crit, bonus_stun]

        labels = []
        attr_labels = []
        top = self.ATTR_TOP
        for name, value, base, bonus in zip(names, values, bases, bonuses):
            label = Label(
                name, self.ATTR_FONT_SIZE, topright=(self.ATTR_RIGHT, top))
            labels.append(label)
            attr_label = AttributeLabel(
                value, self.ATTR_FONT_SIZE, topleft=(self.ATTR_LEFT, top),
                base=base, bonus=bonus)
            attr_labels.append(attr_label)
            top += (max(label.rect.height, attr_label.rect.height)
                    + self.ATTR_GAP)
        return labels, attr_labels

    def create_tooltip_for_level(self):
        text = self.character.level_history
        if not text:
            return None
        return create_tooltip(text, self.level_label.rect.topright)

    def update_tooltip(self):
        self.tooltip = None
        items = [item_box.item for item_box in self.armory.item_boxes
                 if item_box.item is not None]
        for item in items:
            if item.rect.collidepoint(pg.mouse.get_pos()):
                self.tooltip = item.create_tooltip()
        if self.spell_book:
            for spell in self.spell_book.spells:
                if spell.rect.collidepoint(pg.mouse.get_pos()):
                    self.tooltip = spell.create_tooltip()
        for label in self.attributes_labels:
            if label.rect.collidepoint(pg.mouse.get_pos()):
                self.tooltip = label.create_tooltip()
        if self.level_labels and self.level_label.rect.collidepoint(
            pg.mouse.get_pos()
        ):
            self.tooltip = self.create_tooltip_for_level()

    def click(self):
        if not self.rect.collidepoint(pg.mouse.get_pos()):
            self.finish()

    def finish(self):
        self.next = self.previous
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        self.start()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click()

    def draw(self, surface):
        surface.blit(self.underscreen, (0, 0))
        surface.blit(self.image, self.rect)
        surface.blit(self.character_image, self.IMAGE_TOPLEFT)
        for label in self.labels:
            label.draw(surface)
        for label in self.level_labels:
            label.draw(surface)
        for label in self.attributes_labels:
            label.draw(surface)
        self.armory.draw(surface)
        if self.spell_book:
            self.spell_book.draw(surface)
        if self.tooltip:
            self.tooltip.draw(surface)

    def update(self, surface, dt):
        self.update_tooltip()
        self.draw(surface)
