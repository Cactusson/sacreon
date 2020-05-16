from .. import tools
from . import data


class Status:
    GAP = 5

    def __init__(self, body):
        self.body = body
        self.effects = []
        self.image = self.create_image()
        self.rect = self.image.get_rect()
        self.new_effects = []  # this is used so blessing won't be cancelled

    def create_image(self):
        width = data.BODY_BAR_WIDTH - data.ICON_SIZE
        height = data.BODY_BAR_HEIGHT - data.HEALTH_BAR_HEIGHT
        return tools.transparent_surface(width, height)

    def add_effect(self, effect):
        if effect.name == 'STUN' and 'STUN' in self.get_effects():
            return
        self.effects.append(effect)
        effect.on_creation(self.body)
        self.update_positions_of_effects()
        self.new_effects.append(effect)

    def get_effects(self):
        return [effect.name for effect in self.effects]

    def update_effects_on_start(self):
        """
        At the start of each turn.
        """
        self.new_effects = []
        remain = []
        for effect in self.effects:
            if effect.remove_on != 'START':
                remain.append(effect)
                continue
            effect.turns_remain -= 1
            effect.on_turn(self.body)
            if effect.turns_remain > 0:
                remain.append(effect)
            else:
                effect.on_removal(self.body)
        self.effects = remain
        self.update_positions_of_effects()

    def update_effects_on_finish(self):
        """
        At the end of each turn.
        """
        remain = []
        for effect in self.effects:
            if effect.remove_on != 'FINISH' or effect in self.new_effects:
                remain.append(effect)
                continue
            effect.turns_remain -= 1
            effect.on_turn(self.body)
            if effect.turns_remain > 0:
                remain.append(effect)
            else:
                effect.on_removal(self.body)
        self.effects = remain
        self.update_positions_of_effects()

    def update_positions_of_effects(self):
        for indx, effect in enumerate(self.effects):
            effect.rect.x = (self.rect.x + self.GAP +
                             (data.ICON_SIZE + self.GAP) * indx)
            effect.rect.y = self.rect.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for effect in self.effects:
            effect.draw(surface)
