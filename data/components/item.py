import pygame as pg

from . import data
from .tooltip import create_tooltip


class Item:
    def __init__(self, name):
        self.name = name
        self.image = self.get_info('image')
        self.rect = self.image.get_rect()
        self.bonus_health = self.get_info('bonus_health')
        self.bonus_mana = self.get_info('bonus_mana')
        self.bonus_attack = self.get_info('bonus_attack')
        self.bonus_defense = self.get_info('bonus_defense')
        self.bonus_speed = self.get_info('bonus_speed')
        self.bonus_crit_chance = self.get_info('bonus_crit_chance')
        self.bonus_stun_chance = self.get_info('bonus_stun_chance')
        self.bonus_vampirism = self.get_info('bonus_vampirism')
        self.bonus_health_regen = self.get_info('bonus_health_regen')
        self.bonus_mana_regen = self.get_info('bonus_mana_regen')
        self.features = self.get_info('features')
        self.description = self.get_info('description')
        self.on_consume = self.get_info('on_consume')
        self.mouse_offset = [0, 0]

    def get_info(self, parameter):
        info = data.ITEMS[self.name]
        prototype_info = data.ITEMS[info['prototype']]
        if parameter in info:
            obj = info[parameter]
        else:
            obj = prototype_info[parameter]
        if isinstance(obj, list):
            obj = list(obj)
        return obj

    def create_mouse_offset(self):
        self.mouse_offset[0] = self.rect.center[0] - pg.mouse.get_pos()[0]
        self.mouse_offset[1] = self.rect.center[1] - pg.mouse.get_pos()[1]

    def clear_mouse_offset(self):
        self.mouse_offset = [0, 0]

    def adjust_pos(self):
        self.rect.centerx = pg.mouse.get_pos()[0] + self.mouse_offset[0]
        self.rect.centery = pg.mouse.get_pos()[1] + self.mouse_offset[1]

    def create_tooltip(self):
        text = [self.name] + self.description
        tooltip = create_tooltip(text, self.rect.topright)
        return tooltip

    def can_consume(self):
        return True if self.on_consume else False

    def consume(self, user):
        if self.on_consume['name'] == 'restore health':
            health = self.on_consume['points']
            user.restore_health(health)
        elif self.on_consume['name'] == 'restore mana':
            mana = self.on_consume['points']
            user.restore_mana(mana)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
