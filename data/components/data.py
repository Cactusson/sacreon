import pygame as pg

from .. import prepare


# COLORS
BG_COLOR = pg.Color('#F2E9D0')
BOARD_COLOR = pg.Color('#BB5A5A')
HC = pg.Color('#7A12D5')
AC = pg.Color('#599A0C')
SQUARE_COLOR_IDLE = pg.Color('#E79E85')
SQUARE_COLOR_ACTION = pg.Color('#3EC483')
SQUARE_COLOR_HOVER = pg.Color('#3D93A3')
SQUARE_COLOR_HL = pg.Color('#cf8e77')
ITEM_BOX_COLOR = pg.Color('#AACFD0')
ARMORY_COLOR = pg.Color('#2772DB')
SPELL_BOOK_COLOR = pg.Color('#455D7A')
SPELL_IDLE_COLOR = pg.Color('#E3E3E3')
SPELL_HOVER_COLOR = pg.Color('#A4E5D9')
SPELL_ACTIVE_COLOR = pg.Color('#66C6BA')
HEALTH_BAR_GREEN = pg.Color('#7DCE94')
HEALTH_BAR_RED = pg.Color('#DD356E')
LABEL_DAMAGE = pg.Color('#DD356E')
LABEL_HEALTH = pg.Color('#7DCE94')
LABEL_XP = pg.Color('blue')


# POSITIONS
BOARD_CENTER = (500, 225)
UI_ARMORY_POS = (500, 400)
UI_SPELL_BOOK_POS = (500, 400)


# SIZES
SQUARE_SIZE = 100
BODY_SIZE = (48, 54)
ITEM_BOX_SIZE = 100
BODY_BAR_WIDTH = 80
BODY_BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 80
HEALTH_BAR_HEIGHT = 10
ICON_SIZE = 10


# DISTANCES
SQUARE_GAP = 2
ITEM_BOX_GAP = 5
TOOLTIP_GAP = 10
BODY_BAR_GAP = 5
FLYING_LABEL_GAP = 25


# FONT SIZES
TOOLTIP_FONT_SIZE = 17


# GAME CONSTANTS
EXPERIENCE_TABLE = [0, 2, 2]
MAX_LEVEL = len(EXPERIENCE_TABLE)
BONUS_LVL_HEALTH = 5
BONUS_LVL_ATTACK = 3
BONUS_LVL_MANA = 2


# IMAGES FOR BUTTONS
BUTTONS = {
    'MOVE': {
        'IDLE': prepare.GFX['ui']['button_move_idle'],
        'HOVER': prepare.GFX['ui']['button_move_hover'],
        'ACTIVE': prepare.GFX['ui']['button_move_active'],
        'BLOCKED': prepare.GFX['ui']['button_move_blocked'],
    },
    'ATTACK': {
        'IDLE': prepare.GFX['ui']['button_attack_idle'],
        'HOVER': prepare.GFX['ui']['button_attack_hover'],
        'ACTIVE': prepare.GFX['ui']['button_attack_active'],
        'BLOCKED': prepare.GFX['ui']['button_attack_blocked'],
    },
    'SPELLS': {
        'IDLE': prepare.GFX['ui']['button_spells_idle'],
        'HOVER': prepare.GFX['ui']['button_spells_hover'],
        'ACTIVE': prepare.GFX['ui']['button_spells_active'],
        'BLOCKED': prepare.GFX['ui']['button_spells_blocked'],
    },
    'ITEMS': {
        'IDLE': prepare.GFX['ui']['button_items_idle'],
        'HOVER': prepare.GFX['ui']['button_items_hover'],
        'ACTIVE': prepare.GFX['ui']['button_items_active'],
        'BLOCKED': prepare.GFX['ui']['button_items_blocked'],
    },
    'FINISH TURN': {
        'IDLE': prepare.GFX['ui']['button_finish_turn_idle'],
        'HOVER': prepare.GFX['ui']['button_finish_turn_hover'],
        'ACTIVE': prepare.GFX['ui']['button_finish_turn_active'],
        'BLOCKED': prepare.GFX['ui']['button_finish_turn_blocked'],
    },
}


MAP = ['Dungeon', 'Sacreon', 'Dungeon', 'Sacreon', 'Dungeon']
HEROES = ['AMANDA', 'ALEX', 'ESCOBAR', 'MARLA', 'BOBSKY', 'RONDA', 'JESUS',
          'CLEMENTINE', 'MIA', 'JOSH']
ROSTER_AMOUNT = 6

DUNGEONS = [
    {
        'width': 9,
        'height': 4,
        'monsters': ['SPIDER', 'SPIDER', 'SPIDER',
                     'SPIDER', 'SPIDER', 'SPIDER'],
    },
    {
        'width': 9,
        'height': 4,
        'monsters': ['BLUE SPIDER', 'BLUE SPIDER', 'BLUE SPIDER',
                     'GREEN SPIDER', 'GREEN SPIDER', 'GREEN SPIDER'],
    },
    {
        'width': 9,
        'height': 4,
        'monsters': ['BLUE SPIDER', 'BLUE SPIDER', 'GREEN SPIDER',
                     'GREEN SPIDER', 'RED SPIDER', 'RED SPIDER'],
    },
]


CHARACTERS = {
    'BASE': {
        'faction': 'GOOD',
        'health': 8,
        'mana': 0,
        'attack': 2,
        'defense': 0,
        'speed': 3,
        'crit_chance': 10,
        'stun_chance': 0,
        'vampirism': 0,
        'health_regen': 0,
        'mana_regen': 0,
        'crit_multi': 2.0,
        'attack_range': 1,
        'bonus_damage_on_stun': 0,
        'spells': [],
        'level_bonuses': ['HEALTH', 'ATTACK'],
        'features': [],
    },
    'AMANDA': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['amanda'],
        'health': 9,
        'attack': 3,
        'crit_chance': 20,
        'crit_multi': 2.5,
        'feature_text': 'Crit strikes deal 2.5x damage.',
    },
    'BOBSKY': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['bobsky'],
        'health': 9,
        'attack': 2,
        'mana': 3,
        'spells': ['Heal', 'Mass Heal'],
        'level_bonuses': ['HEALTH', 'ATTACK', 'MANA'],
        'feature_text': 'Can cast healing spells.',
    },
    'JOSH': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['josh'],
        'health': 8,
        'attack': 3,
        'mana': 3,
        'spells': ['Storm Bolt', 'Thunderclap'],
        'level_bonuses': ['HEALTH', 'ATTACK', 'MANA'],
        'feature_text': 'Can cast stunning spells.',
    },
    'RONDA': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['ronda'],
        'health': 9,
        'attack': 2,
        'mana': 3,
        'speed': 4,
        'spells': ['Poison', 'Strong Poison'],
        'level_bonuses': ['HEALTH', 'ATTACK', 'MANA'],
        'feature_text': 'Can cast poisoning spells.',
    },
    'CLEMENTINE': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['clementine'],
        'health': 8,
        'attack': 2,
        'mana': 4,
        'speed': 3,
        'spells': ['Fireball', 'Huge Fireball'],
        'level_bonuses': ['HEALTH', 'ATTACK', 'MANA'],
        'feature_text': 'Can cast damaging spells.',
    },
    'JESUS': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['jesus'],
        'health': 9,
        'attack': 2,
        'mana': 3,
        'spells': ['Blessing', 'Blessy Blessing'],
        'level_bonuses': ['HEALTH', 'ATTACK', 'MANA'],
        'feature_text': 'Can cast empowering spells.',
    },
    'MARLA': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['marla'],
        'health': 9,
        'attack': 3,
        'mana': 3,
        'spells': ['Teleport'],
        'feature_text': 'Can teleport.',
    },
    'MIA': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['mia'],
        'health': 8,
        'attack': 3,
        'attack_range': 2,
        'feature_text': 'Can attack within the range of 2.',
    },
    'ALEX': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['alex'],
        'health': 10,
        'attack': 2,
        'health_regen': 2,
        'speed': 4,
        'features': ['REGEN'],
        'feature_text': 'Regenerates 2/3/4 health at the start of each turn.',
    },
    'ESCOBAR': {
        'prototype': 'BASE',
        'image': prepare.GFX['characters']['darth'],
        'health': 11,
        'attack': 2,
        'stun_chance': 15,
        'bonus_damage_on_stun': 2,
        'features': ['BONUS_ON_STUN'],
        'feature_text': 'Bonus 2/3/4 damage with each stun.',
    },
    'SPIDER': {
        'prototype': 'BASE',
        'faction': 'BAD',
        'image': prepare.GFX['characters']['spider'],
        'health': 8,
        'attack': 2,
        'feature_text': 'Absolutely nothing remarkable.',
    },
    'BLUE SPIDER': {
        'prototype': 'BASE',
        'faction': 'BAD',
        'image': prepare.GFX['characters']['blue_spider'],
        'health': 10,
        'attack': 4,
        'features': ['RANDOM_ITEM'],
        'feature_text': 'Gets one random item.',
    },
    'GREEN SPIDER': {
        'prototype': 'BASE',
        'faction': 'BAD',
        'image': prepare.GFX['characters']['green_spider'],
        'health': 12,
        'attack': 3,
        'health_regen': 2,
        'feature_text': 'Regenerates 2 HP each turn.',
    },
    'RED SPIDER': {
        'prototype': 'BASE',
        'faction': 'BAD',
        'image': prepare.GFX['characters']['red_spider'],
        'health': 14,
        'attack': 5,
        'defense': 2,
        'vampirism': 100,
        'feature_text': 'Heals 100% of damage dealt.',
    },
}


COMMON_ITEMS = ['Sword', 'Ring of Life', 'Axe', 'Mana Diamond', 'Boots',
                'Shield']
CONSUMABLE_ITEMS = ['Health Potion', 'Mana Potion']
RARE_ITEMS = ['Flail', 'Mask of Vampirism', 'Desolator', 'Cross',
              'Ring of Regeneration']
ITEMS_FOR_AI = ['Sword', 'Ring of Life', 'Axe', 'Boots', 'Shield', 'Flail',
                'Mask of Vampirism', 'Desolator', 'Cross',
                'Ring of Regeneration']


ITEMS = {
    'Base': {
        'description': [],
        'bonus_health': 0,
        'bonus_mana': 0,
        'bonus_attack': 0,
        'bonus_defense': 0,
        'bonus_speed': 0,
        'bonus_crit_chance': 0,
        'bonus_stun_chance': 0,
        'bonus_vampirism': 0,
        'bonus_health_regen': 0,
        'bonus_mana_regen': 0,
        'on_consume': None,
        'features': [],
    },

    # COMMON
    'Sword': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['sword'],
        'description': ['+2 attack'],
        'bonus_attack': 2,
    },
    'Ring of Life': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['ring_of_life'],
        'description': ['+3 health'],
        'bonus_health': 3,
    },
    'Axe': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['axe'],
        'description': ['+1 attack', '+10% crit chance'],
        'bonus_attack': 1,
        'bonus_crit_chance': 10,
    },
    'Boots': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['boots'],
        'description': ['+1 speed'],
        'bonus_speed': 1,
    },
    'Shield': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['shield'],
        'description': ['+1 defense'],
        'bonus_defense': 1,
    },
    'Mana Diamond': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['mana_diamond'],
        'description': ['+2 mana'],
        'bonus_mana': 2,
    },

    # CONSUMABLES
    'Health Potion': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['health_potion'],
        'description': ['restores 5 health'],
        'on_consume': {
            'name': 'restore health',
            'points': 5,
        },
    },
    'Mana Potion': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['mana_potion'],
        'description': ['restores 3 mana'],
        'on_consume': {
            'name': 'restore mana',
            'points': 3,
        },
    },

    # RARE
    'Flail': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['flail'],
        'description': ['+2 attack', '+20% chance to stun'],
        'bonus_attack': 2,
        'bonus_stun_chance': 20,
    },
    'Mask of Vampirism': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['mask_of_vampirism'],
        'description': ['heals 50% of damage given'],
        'bonus_vampirism': 50,
    },
    'Desolator': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['desolator'],
        'description': ['+2 attack', 'ignores defense'],
        'bonus_attack': 2,
        'features': ['ignore defense'],
    },
    'Cross': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['cross'],
        'description': ['wearing this will always start turns first'],
        'features': ['first turn'],
    },
    'Ring of Regeneration': {
        'prototype': 'Base',
        'image': prepare.GFX['items']['ring_of_regeneration'],
        'description': [
            'restores 2 HP and 1 MP at the beginning of each turn'],
        'bonus_health_regen': 2,
        'bonus_mana_regen': 1,
    },
}


TURN_IMAGE = pg.Surface((ICON_SIZE, ICON_SIZE)).convert()
TURN_IMAGE.fill(pg.Color('#FFBD74'))


EFFECTS = {
    'Base': {
        'remove_on': 'START',
        'damage': None,
        'bonus_attack': 0,
        'bonus_crit_chance': 0,
    },
    'STUN': {
        'prototype': 'Base',
        'image': prepare.GFX['ui']['effect_stun'],
        'description': "Can't do anything the next turn.",
        'turns': 1,
    },
    'POISON': {
        'prototype': 'Base',
        'image': prepare.GFX['ui']['effect_poison'],
        'description': 'Gets 2 damage each turn.',
        'turns': 2,
        'damage': 2,
    },
    'STRONG POISON': {
        'prototype': 'Base',
        'image': prepare.GFX['ui']['effect_poison'],
        'description': 'Gets 4 damage each turn.',
        'turns': 2,
        'damage': 4,
    },
    'BLESSING': {
        'prototype': 'Base',
        'image': prepare.GFX['ui']['effect_blessing'],
        'description': '+4 attack, +20% crit chance.',
        'remove_on': 'FINISH',
        'turns': 1,
        'bonus_attack': 4,
        'bonus_crit_chance': 20,
    },
    'BLESSY BLESSING': {
        'prototype': 'Base',
        'image': prepare.GFX['ui']['effect_blessing'],
        'description': '+8 attack, +40% crit chance.',
        'remove_on': 'FINISH',
        'turns': 1,
        'bonus_attack': 8,
        'bonus_crit_chance': 40,
    },
}


SPELLS = {
    'Base': {
        'description': [],
        'target': None,
        'points': None,
        'duration': 0,
        'range': None,
        'manacost': 0,
        'fatigue': True,
        'level_required': 1,
    },
    'Heal': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['heal'],
        'description': ['Restores 4 health.'],
        'target': 'GOOD',
        'points': 4,
        'range': 2,
        'manacost': 1,
    },
    'Mass Heal': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['mass_heal'],
        'description': ['Restores 3 health to every one of your characters.'],
        'points': 3,
        'manacost': 2,
        'level_required': 2,
    },
    'Fireball': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['fireball'],
        'description': ['Deals 5 damage.'],
        'target': 'BAD',
        'points': 5,
        'range': 4,
        'manacost': 2,
    },
    'Huge Fireball': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['huge_fireball'],
        'description': ['Deals 8 damage.'],
        'target': 'BAD',
        'points': 8,
        'range': 5,
        'manacost': 3,
        'level_required': 2,
    },
    'Storm Bolt': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['storm_bolt'],
        'description': ['Deals 2 damage and stuns the target.'],
        'target': 'BAD',
        'points': 2,
        'range': 2,
        'manacost': 1,
    },
    'Thunderclap': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['thunderclap'],
        'description': ['Deals 2 damage and stuns all enemies around.'],
        'points': 2,
        'manacost': 2,
        'level_required': 2,
    },
    'Poison': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['poison'],
        'description': ['Deals 2 damage per turn.', 'Duration: 2 turns.'],
        'target': 'BAD',
        'range': 3,
        'manacost': 1,
    },
    'Strong Poison': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['strong_poison'],
        'description': ['Deals 4 damage per turn.', 'Duration: 2 turns.'],
        'target': 'BAD',
        'range': 4,
        'manacost': 2,
        'level_required': 2,
    },
    'Blessing': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['blessing'],
        'description': ['Empowers target for the next turn:',
                        '+4 attack',
                        '+20% crit chance'],
        'target': 'GOOD',
        'range': 2,
        'manacost': 1,
    },
    'Blessy Blessing': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['blessy_blessing'],
        'description': ['Empowers target for the next turn:',
                        '+8 attack',
                        '+40% crit chance'],
        'target': 'GOOD',
        'range': 3,
        'manacost': 2,
        'level_required': 2,
    },
    'Teleport': {
        'prototype': 'Base',
        'image': prepare.GFX['spells']['teleport'],
        'description': ['Teleports to the chosen location.',
                        'You can still do stuff after casting this spell.'],
        'target': 'SQUARE',
        'range': 15,
        'manacost': 1,
        'fatigue': False,
    },
}
