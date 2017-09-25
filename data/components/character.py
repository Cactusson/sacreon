import pygame as pg
import random

from . import data
from .body import Body
from .item import Item


class Character:
    def __init__(self, name):
        self.name = name
        self.faction = self.get_info('faction')
        self.create_image()
        self.base_health = self.get_info('health')
        self.base_mana = self.get_info('mana')
        self.base_attack = self.get_info('attack')
        self.base_defense = self.get_info('defense')
        self.base_speed = self.get_info('speed')
        self.base_crit_chance = self.get_info('crit_chance')
        self.base_stun_chance = self.get_info('stun_chance')
        self.base_vampirism = self.get_info('vampirism')
        self.base_health_regen = self.get_info('health_regen')
        self.base_mana_regen = self.get_info('mana_regen')
        self.crit_multi = self.get_info('crit_multi')
        self.attack_range = self.get_info('attack_range')
        self.bonus_damage_on_stun = self.get_info('bonus_damage_on_stun')
        self.level_bonuses = self.get_info('level_bonuses')
        self.base_features = self.get_info('features')
        self.feature_text = self.get_info('feature_text')
        self.spells = self.get_info('spells')
        self.items = [None, None, None]
        self.level_history = []
        if self.faction == 'GOOD':
            self.level = 1
            self.xp = 0
        if 'RANDOM_ITEM' in self.base_features:
            self.get_random_item()
        self.calculate_attributes()

    def get_info(self, parameter):
        info = data.CHARACTERS[self.name]
        prototype_info = data.CHARACTERS[info['prototype']]
        if parameter in info:
            obj = info[parameter]
        else:
            obj = prototype_info[parameter]
        if isinstance(obj, list):
            obj = list(obj)
        return obj

    def create_image(self):
        self.image = pg.transform.scale(self.get_info('image'), data.BODY_SIZE)

    def calculate_attributes(self):
        self.health = self.base_health
        self.mana = self.base_mana
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.speed = self.base_speed
        self.crit_chance = self.base_crit_chance
        self.stun_chance = self.base_stun_chance
        self.vampirism = self.base_vampirism
        self.health_regen = self.base_health_regen
        self.mana_regen = self.base_mana_regen
        self.features = list(self.base_features)
        for item in self.items:
            if item is None:
                continue
            self.health += item.bonus_health
            self.mana += item.bonus_mana
            self.attack += item.bonus_attack
            self.defense += item.bonus_defense
            self.speed += item.bonus_speed
            self.crit_chance += item.bonus_crit_chance
            self.stun_chance += item.bonus_stun_chance
            self.vampirism += item.bonus_vampirism
            self.health_regen += item.bonus_health_regen
            self.mana_regen += item.bonus_mana_regen
            self.features.extend(item.features)

    def get_random_item(self):
        name = random.choice(data.ITEMS_FOR_AI)
        item = Item(name)
        self.items[0] = item

    def load_items(self, items):
        self.items = items
        self.calculate_attributes()

    def needed_exp(self):
        if self.level == data.MAX_LEVEL:
            return self.xp
        else:
            return data.EXPERIENCE_TABLE[self.level]

    def get_xp(self):
        if self.level >= data.MAX_LEVEL:
            return
        self.xp += 1
        if self.xp >= self.needed_exp():
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = 0
        entry = 'LEVEL {}: '.format(self.level)
        bonus = random.choice(self.level_bonuses)
        if bonus == 'HEALTH':
            self.base_health += data.BONUS_LVL_HEALTH
            entry += '+{} health'.format(data.BONUS_LVL_HEALTH)
        elif bonus == 'ATTACK':
            self.base_attack += data.BONUS_LVL_ATTACK
            entry += '+{} attack'.format(data.BONUS_LVL_ATTACK)
        elif bonus == 'MANA':
            self.base_mana += data.BONUS_LVL_MANA
            entry += '+{} mana'.format(data.BONUS_LVL_MANA)

        if 'REGEN' in self.features:
            self.base_health_regen += 1
        if 'BONUS_ON_STUN' in self.features:
            self.bonus_damage_on_stun += 1

        self.calculate_attributes()
        self.level_history.append(entry)

    def create_body(self, in_play=False, events=None):
        return Body(self, in_play, events)
