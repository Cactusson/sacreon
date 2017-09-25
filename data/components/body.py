import random

from . import data
from .body_bar import BodyBar


class Body:
    def __init__(self, character, in_play=False, events=None):
        self.character = character
        self.in_play = in_play
        self.name = self.character.name
        self.faction = self.character.faction
        self.current_health = self.character.health
        self.current_mana = self.character.mana
        self.bonus_attack = 0
        self.bonus_crit_chance = 0
        self.image = character.image.copy()
        self.rect = self.image.get_rect()
        if self.in_play:
            self.body_bar = BodyBar(self)
            self.events = events
        else:
            self.body_bar = None

    @property
    def health(self):
        return self.character.health

    @property
    def mana(self):
        return self.character.mana

    @property
    def attack(self):
        return self.character.attack + self.bonus_attack

    @property
    def defense(self):
        return self.character.defense

    @property
    def speed(self):
        return self.character.speed

    @property
    def crit_chance(self):
        return self.character.crit_chance + self.bonus_crit_chance

    @property
    def stun_chance(self):
        return self.character.stun_chance

    @property
    def vampirism(self):
        return self.character.vampirism

    @property
    def health_regen(self):
        return self.character.health_regen

    @property
    def mana_regen(self):
        return self.character.mana_regen

    @property
    def crit_multi(self):
        return self.character.crit_multi

    @property
    def attack_range(self):
        return self.character.attack_range

    @property
    def bonus_damage_on_stun(self):
        return self.character.bonus_damage_on_stun

    @property
    def features(self):
        return self.character.features

    @property
    def level(self):
        return self.character.level

    @property
    def xp(self):
        return self.character.xp

    def calculate_damage(self):
        damage = self.attack
        return damage

    def crit_proc(self):
        return random.randint(1, 100) <= self.crit_chance

    def stun_proc(self):
        return random.randint(1, 100) <= self.stun_chance

    def get_damage(self, damage, source, crit=False):
        self.current_health = max(0, self.current_health - damage)
        self.body_bar.update_health_bar()
        event = dict(
            name='DAMAGE DEALT', victim=self)
        self.events.append(event)
        if not self.check_alive() and source.faction == 'GOOD':
            if source.check_alive():
                source.get_xp()

    def remove_mana(self, amount):
        self.current_mana -= amount

    def add_effect(self, effect):
        self.body_bar.status.add_effect(effect)

    def update_effects_on_start(self):
        effects = self.body_bar.status.get_effects()
        finish_turn = 'STUN' in effects
        self.body_bar.status.update_effects_on_start()
        return finish_turn

    def update_effects_on_finish(self):
        self.body_bar.status.update_effects_on_finish()

    def get_effects(self):
        return self.body_bar.status.get_effects()

    def restore_health(self, health):
        self.current_health = min(self.health, self.current_health + health)
        self.body_bar.update_health_bar()

    def restore_mana(self, mana):
        self.current_mana = min(self.mana, self.current_mana + mana)

    def regenerate(self):
        self.restore_health(self.health_regen)
        self.restore_mana(self.mana_regen)

    def check_alive(self):
        return self.current_health > 0

    def needed_exp(self):
        return self.character.needed_exp()

    def get_xp(self):
        if self.level >= data.MAX_LEVEL:
            return
        health = self.character.base_health
        mana = self.character.base_mana
        self.character.get_xp()
        if self.character.base_health > health:
            self.current_health += self.character.base_health - health
            self.body_bar.update_health_bar()
        if self.character.base_mana > mana:
            self.current_mana += self.character.base_mana - mana
        event = dict(name='XP GAINED', body=self)
        self.events.append(event)

    def event_new_global_turn(self):
        self.body_bar.create_turn_icon()

    def event_new_turn(self):
        self.body_bar.delete_turn_icon()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.in_play:
            self.body_bar.draw(surface)

    def update(self):
        self.body_bar.update()
