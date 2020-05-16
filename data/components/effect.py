from . import data
from .tooltip import create_tooltip


class Effect:
    def __init__(self, name, source):
        self.name = name
        self.source = source
        self.image = self.get_info('image')
        self.description = self.get_info('description')
        self.turns_remain = self.get_info('turns')
        self.remove_on = self.get_info('remove_on')
        self.damage = self.get_info('damage')  # for poison
        self.bonus_attack = self.get_info('bonus_attack')  # for blessing
        self.bonus_crit_chance = self.get_info('bonus_crit_chance')  # ditto
        self.rect = self.image.get_rect()

    def get_info(self, parameter):
        info = data.EFFECTS[self.name]
        prototype_info = data.EFFECTS[info['prototype']]
        obj = info[parameter] if parameter in info else prototype_info[parameter]
        if isinstance(obj, list):
            obj = list(obj)
        return obj

    def on_creation(self, owner):
        owner.bonus_attack += self.bonus_attack
        owner.bonus_crit_chance += self.bonus_crit_chance

    def on_removal(self, owner):
        owner.bonus_attack -= self.bonus_attack
        owner.bonus_crit_chance -= self.bonus_crit_chance

    def on_turn(self, owner):
        if not owner.check_alive():
            return
        if self.damage:
            owner.get_damage(self.damage, self.source)

    def create_tooltip(self):
        remaining = 'Turns: {}'.format(self.turns_remain)
        text = [self.name, self.description, remaining]
        return create_tooltip(text, self.rect.topright)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
