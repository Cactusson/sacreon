import pygame as pg

from .. import state_machine
from ..components import data
from ..components.armory import Armory
from ..components.attribute_label import AttributeLabel
from ..components.buttons import Button
from ..components.hoop import Hoop
from ..components.label import Label
from ..components.tooltip import create_tooltip


class ArmoryView(state_machine._State):
    ITEM_BOX_GAP = 110
    ITEM_BOX_TOPLEFT = (600, 400)
    LEVEL_TOPLEFT = (700, 305)
    ATTR_TOP = 340
    ATTR_RIGHT = 780
    ATTR_LEFT = 790
    ATTR_GAP = 10
    ATTR_FONT_SIZE = 20
    NAME_LABEL_CENTER = (750, 135)
    ARMORY_TOPLEFT = (100, 170)
    CHAR_ARMORY_TOPLEFT = (600, 170)
    BACK_BUTTON_CENTER = (100, 550)

    def start(self):
        self.bodies = self.persist['bodies']
        del self.persist['bodies']
        self.hoop = Hoop()
        self.armory = Armory(
            self.persist['armory_items'], topleft=self.ARMORY_TOPLEFT)
        self.name_label = None
        self.clicked_item = None
        self.previous_item_box = None
        self.back_button = Button(
            'BACK', 30, self.button_click, font_name='Amaranth-Bold',
            center=self.BACK_BUTTON_CENTER)
        self.activate_body(self.bodies[0])

    def create_char_armory(self):
        self.char_armory = Armory(
            self.active_body.character.items, topleft=self.CHAR_ARMORY_TOPLEFT)

    def activate_body(self, body):
        self.active_body = body
        self.hoop.rect.center = self.active_body.rect.center
        self.create_char_armory()
        self.create_level_label()
        self.create_attributes()
        self.name_label = Label(
            self.active_body.name, 30, font_name='Amaranth-Bold',
            center=self.NAME_LABEL_CENTER)

    def create_level_label(self):
        level = self.active_body.level
        level_text = 'Level {}'.format(level)
        if level < data.MAX_LEVEL:
            xp = self.active_body.xp
            needed = self.active_body.needed_exp()
            level_text += ' ({}/{})'.format(xp, needed)
        self.level_label = Label(level_text, self.ATTR_FONT_SIZE,
                                 topleft=self.LEVEL_TOPLEFT)

    def create_attributes(self):
        character = self.active_body.character
        character.calculate_attributes()
        self.labels, self.attribute_labels = self.create_attribute_labels(
            character)

    def try_to_get_item(self):
        item, item_box = self.armory.try_to_get_item()
        if item is None:
            item, item_box = self.char_armory.try_to_get_item()
        return item, item_box

    def click_on_item(self, item, item_box):
        self.clicked_item = item
        self.clicked_item.create_mouse_offset()
        self.previous_item_box = item_box
        self.persist['armory_items'] = self.armory.get_items()
        self.active_body.character.load_items(self.char_armory.get_items())

    def drop_item(self):
        success = self.char_armory.try_to_add_item(self.clicked_item)
        if not success:
            success = self.armory.try_to_add_item(self.clicked_item)
        if not success:
            self.previous_item_box.add_item(self.clicked_item)
        self.clicked_item.clear_mouse_offset()
        self.clicked_item = None
        self.previous_item_box = None
        self.persist['armory_items'] = self.armory.get_items()
        self.active_body.character.load_items(self.char_armory.get_items())
        self.create_attributes()

    def create_attribute_labels(self, character):
        health = '{}'.format(character.health)
        base_health = character.base_health
        bonus_health = character.health - base_health
        mana = '{}'.format(character.mana)
        base_mana = character.base_mana
        bonus_mana = character.mana - base_mana
        attack_value = character.attack
        attack = '{}'.format(attack_value)
        base_attack = character.base_attack
        bonus_attack = attack_value - base_attack
        defense = '{}'.format(character.defense)
        base_defense = character.base_defense
        bonus_defense = character.defense - base_defense
        speed = '{}'.format(character.speed)
        base_speed = character.base_speed
        bonus_speed = character.speed - base_speed
        crit_value = character.crit_chance
        crit = '{}%'.format(crit_value)
        base_crit = '{}%'.format(character.base_crit_chance)
        bonus_crit = '{}%'.format(crit_value - character.base_crit_chance)
        stun = '{}%'.format(character.stun_chance)
        base_stun = '{}%'.format(character.base_stun_chance)
        bonus_stun = '{}%'.format(
            character.stun_chance - character.base_stun_chance)
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
        text = self.active_body.character.level_history
        if not text:
            return None
        tooltip = create_tooltip(text, self.level_label.rect.topright)
        return tooltip

    def update_tooltip(self):
        self.tooltip = None
        armory_items = [item_box.item for item_box in self.armory.item_boxes
                        if item_box.item is not None]
        char_items = [item_box.item for item_box in
                      self.char_armory.item_boxes if item_box.item is not None]
        items = armory_items + char_items
        for item in items:
            if item.rect.collidepoint(pg.mouse.get_pos()):
                self.tooltip = item.create_tooltip()
        for label in self.attribute_labels:
            if label.rect.collidepoint(pg.mouse.get_pos()):
                self.tooltip = label.create_tooltip()
        if self.level_label.rect.collidepoint(pg.mouse.get_pos()):
            self.tooltip = self.create_tooltip_for_level()

    def left_click(self):
        for body in self.bodies:
            if body.rect.collidepoint(pg.mouse.get_pos()):
                if body != self.active_body:
                    self.activate_body(body)
        item, item_box = self.try_to_get_item()
        if item:
            self.click_on_item(item, item_box)
        self.back_button.click()

    def right_click(self):
        for body in self.bodies:
            if body.rect.collidepoint(pg.mouse.get_pos()):
                self.change_state('CHARACTER_VIEW', character=body.character)

    def unclick(self):
        if self.clicked_item:
            self.drop_item()

    def change_state(self, new_state, **kwargs):
        if new_state == 'CHARACTER_VIEW':
            character = kwargs['character']
            self.persist['character_to_view'] = character
        self.next = new_state
        self.done = True

    def button_click(self, name):
        self.change_state('LOBBY')

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'LOBBY':
            self.start()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.change_state('LOBBY')
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click()
            elif event.button == 3:
                self.right_click()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.unclick()

    def draw(self, surface):
        surface.fill(pg.Color('#A4E5D9'))
        for body in self.bodies:
            body.draw(surface)
        self.hoop.draw(surface)
        self.armory.draw(surface)
        self.char_armory.draw(surface)
        for label in self.labels:
            label.draw(surface)
        for label in self.attribute_labels:
            label.draw(surface)
        self.level_label.draw(surface)
        self.name_label.draw(surface)
        self.back_button.draw(surface)
        if self.clicked_item:
            self.clicked_item.draw(surface)
        if self.tooltip:
            self.tooltip.draw(surface)

    def update(self, surface, dt):
        if self.clicked_item:
            self.clicked_item.adjust_pos()
        self.back_button.update()
        self.update_tooltip()
        self.draw(surface)
