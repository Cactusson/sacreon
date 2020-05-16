import pygame as pg

from . import data
from .effect import Effect
from .tooltip import create_tooltip


class Spell:
    def __init__(self, name):
        self.name = name
        self.create_images()
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.target = self.get_info('target')
        self.points = self.get_info('points')
        self.duration = self.get_info('duration')
        self.range = self.get_info('range')
        self.manacost = self.get_info('manacost')
        self.fatigue = self.get_info('fatigue')
        self.level_required = self.get_info('level_required')
        self.description = self.create_description()
        self.hover = False
        self.active = False
        self.blocked = False

    def create_images(self):
        width = height = data.ITEM_BOX_SIZE
        image = pg.Surface((width, height)).convert()
        rune = data.SPELLS[self.name]['image']
        rect = rune.get_rect()
        rect.center = width // 2, height // 2

        idle_image = image.copy()
        idle_image.fill(data.SPELL_IDLE_COLOR)
        idle_image.blit(rune, rect)

        hover_image = image.copy()
        hover_image.fill(data.SPELL_HOVER_COLOR)
        hover_image.blit(rune, rect)

        active_image = image.copy()
        active_image.fill(data.SPELL_ACTIVE_COLOR)
        active_image.blit(rune, rect)

        blocked_image = image.copy()
        blocked_image.fill(pg.Color('black'))
        blocked_image.blit(rune, rect)

        self.idle_image = idle_image
        self.hover_image = hover_image
        self.active_image = active_image
        self.blocked_image = blocked_image

    def create_description(self):
        description = self.get_info('description')
        if self.range:
            spell_range = 'RANGE: {}'.format(self.range)
            description.append(spell_range)
        manacost = 'MANACOST: {}'.format(self.manacost)
        description.append(manacost)
        return description

    def get_info(self, parameter):
        info = data.SPELLS[self.name]
        prototype_info = data.SPELLS[info['prototype']]
        obj = info[parameter] if parameter in info else prototype_info[parameter]
        if isinstance(obj, list):
            obj = list(obj)
        return obj

    def can_be_casted(self, caster, board):
        return True

    def cast(self, caster, target, bodies, board):
        if self.name == 'Heal':
            target.restore_health(self.points)
        elif self.name == 'Mass Heal':
            friends = [body for body in bodies if body.faction == 'GOOD']
            for unit in friends:
                unit.restore_health(self.points)
        elif self.name in ['Fireball', 'Huge Fireball']:
            target.get_damage(self.points, caster)
        elif self.name == 'Storm Bolt':
            target.get_damage(self.points, caster)
            target.add_effect(Effect('STUN', caster))
        elif self.name == 'Thunderclap':
            targets = board.get_enemies_around(caster)
            for target in targets:
                target.get_damage(self.points, caster)
                target.add_effect(Effect('STUN', caster))
        elif self.name == 'Poison':
            target.add_effect(Effect('POISON', caster))
        elif self.name == 'Strong Poison':
            target.add_effect(Effect('STRONG POISON', caster))
        elif self.name == 'Blessing':
            target.add_effect(Effect('BLESSING', caster))
        elif self.name == 'Blessy Blessing':
            target.add_effect(Effect('BLESSY BLESSING', caster))
        elif self.name == 'Teleport':
            square = board.get_square_by_obj(caster)
            square.remove_obj()
            target.get_obj(caster)

    def activate(self):
        self.active = True
        self.image = self.active_image

    def block(self, reason):
        if self.blocked:
            return
        self.blocked = True
        self.image = self.blocked_image
        if reason == 'LEVEL':
            text = '(LEVEL {} REQUIRED)'.format(self.level_required)
        elif reason == 'MANA':
            text = '(NOT ENOUGH MANA)'
        self.description.insert(0, text)

    def create_tooltip(self):
        text = [self.name] + self.description
        return create_tooltip(text, self.rect.topright)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.hover = self.rect.collidepoint(pg.mouse.get_pos())
        if not (self.active or self.blocked):
            self.image = self.hover_image if self.hover else self.idle_image
