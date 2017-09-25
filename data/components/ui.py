import pygame as pg

from ..components import data
from ..components.armory import Armory
from ..components.card import Card
from ..components.phase_button import PhaseButton
from ..components.spell_book import SpellBook


class UI:
    def __init__(self, events):
        self.events = events
        self.cards = {'LEFT': Card('LEFT'), 'RIGHT': Card('RIGHT')}
        self.phase_buttons = []
        self.armory = None
        self.spell_book = None

    def take_down_card(self, side):
        self.cards[side].take_down()

    def new_body_for_card(self, side, body):
        self.cards[side].get_body(body)

    def get_body_from_card(self, side):
        return self.cards[side].body

    def update_cards(self):
        for card in self.cards.values():
            if card.body:
                card.update_image()

    def create_phase_buttons(self, move, attack, spells, items, finish):
        move = PhaseButton(
            'MOVE', self.phase_button_call, center=(300, 520), state=move)
        attack = PhaseButton(
            'ATTACK', self.phase_button_call, center=(400, 520),
            state=attack)
        spells = PhaseButton(
            'SPELLS', self.phase_button_call, center=(500, 520),
            state=spells)
        items = PhaseButton(
            'ITEMS', self.phase_button_call, center=(600, 520),
            state=items)
        finish = PhaseButton(
            'FINISH TURN', self.phase_button_call, center=(700, 520),
            state=finish)
        self.phase_buttons = [move, attack, items, spells, finish]

    def phase_button_call(self, button):
        self.something_clicked = True
        event = dict(name='PHASE BUTTON CLICKED', button=button)
        self.events.append(event)

    def open_items(self, active_body):
        items = active_body.character.items
        self.armory = Armory(items, center=data.UI_ARMORY_POS)

    def close_items(self):
        self.armory = None

    def click_on_armory(self):
        for item_box in self.armory.item_boxes:
            if item_box.item is None:
                continue
            if item_box.item.rect.collidepoint(pg.mouse.get_pos()):
                self.something_clicked = True
                if item_box.item.on_consume:
                    event = dict(name='ITEM CONSUMED', item=item_box.item)
                    self.events.append(event)
                    item_box.remove_item()

    def open_spell_book(self, active_body):
        spells = active_body.character.spells
        mana = active_body.current_mana
        self.spell_book = SpellBook(
            spells, data.UI_SPELL_BOOK_POS, active_body.level, mana=mana)

    def close_spell_book(self):
        self.spell_book = None

    def click_on_spell_book(self):
        for spell in self.spell_book.spells:
            if spell.rect.collidepoint(pg.mouse.get_pos()):
                self.something_clicked = True
                self.click_on_spell(spell)
                break

    def click_on_spell(self, spell):
        if spell.blocked:
            return
        event = dict(name='SPELL UNCLICKED')
        self.events.append(event)
        if not spell.active:
            event = dict(name='SPELL CLICKED', spell=spell)
            self.events.append(event)

    def update_tooltip(self, bodies):
        self.tooltip = None
        for button in self.phase_buttons:
            if button.rect.collidepoint(pg.mouse.get_pos()):
                self.tooltip = button.create_tooltip()
        if self.armory:
            items = [item_box.item for item_box in self.armory.item_boxes
                     if item_box.item is not None]
            for item in items:
                if item.rect.collidepoint(pg.mouse.get_pos()):
                    self.tooltip = item.create_tooltip()
        if self.spell_book:
            for spell in self.spell_book.spells:
                if spell.rect.collidepoint(pg.mouse.get_pos()):
                    self.tooltip = spell.create_tooltip()
        for body in bodies:
            for effect in body.body_bar.status.effects:
                if effect.rect.collidepoint(pg.mouse.get_pos()):
                    self.tooltip = effect.create_tooltip()
            if body.body_bar.health_bar.rect.collidepoint(
                    pg.mouse.get_pos()):
                self.tooltip = body.body_bar.health_bar.create_tooltip()

    def click(self):
        # something_clicked used because the UI is made the way that
        # armory and spell_book can overlap with board
        self.something_clicked = False
        for phase_button in self.phase_buttons:
            phase_button.click()
        if self.armory:
            self.click_on_armory()
        if self.spell_book:
            self.click_on_spell_book()
        return self.something_clicked

    def draw(self, surface):
        for card in self.cards.values():
            card.draw(surface)
        for phase_button in self.phase_buttons:
            phase_button.draw(surface)
        if self.armory:
            self.armory.draw(surface)
        if self.spell_book:
            self.spell_book.draw(surface)
        if self.tooltip:
            self.tooltip.draw(surface)

    def update(self, bodies):
        for phase_button in self.phase_buttons:
            phase_button.update()
        if self.spell_book:
            spells_changed = self.spell_book.update()
            events = []
            for spell in spells_changed:
                if spell.hover:
                    name = 'SPELL HOVERED'
                    event = dict(name=name, spell=spell)
                    events.append(event)
                else:
                    name = 'SPELL UNHOVERED'
                    event = dict(name=name, spell=spell)
                    events.insert(0, event)
            self.events.extend(events)
        self.update_tooltip(bodies)
