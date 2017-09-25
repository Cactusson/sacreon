import pygame as pg

from . import data
from .spell import Spell


class SpellBook:
    def __init__(self, spells, center, level, mana=None):
        self.spells = [Spell(name) for name in spells]
        for spell in self.spells:
            if spell.level_required > level:
                spell.block('LEVEL')
            if mana is not None:
                if spell.manacost > mana:
                    spell.block('MANA')
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=center)
        self.place_spells()

    def create_image(self):
        width = (data.ITEM_BOX_SIZE * len(self.spells) +
                 data.ITEM_BOX_GAP * (len(self.spells) + 1))
        height = (data.ITEM_BOX_SIZE + data.ITEM_BOX_GAP * 2)
        image = pg.Surface((width, height)).convert()
        image.fill(data.SPELL_BOOK_COLOR)
        return image

    def place_spells(self):
        topleft = [self.rect.x + data.ITEM_BOX_GAP,
                   self.rect.y + data.ITEM_BOX_GAP]
        for spell in self.spells:
            spell.rect.topleft = topleft
            topleft[0] += spell.rect.width + data.ITEM_BOX_GAP

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for spell in self.spells:
            spell.draw(surface)

    def update(self):
        spells_changed = []
        spell_active = False
        for spell in self.spells:
            if spell.active:
                spell_active = True
            hover = spell.hover
            spell.update()
            if spell.hover != hover:
                spells_changed.append(spell)
        if spell_active:
            return []
        else:
            return spells_changed
