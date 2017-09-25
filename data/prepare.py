import os
import pygame as pg

from . import tools


SCREEN_SIZE = (1000, 600)
ORIGINAL_CAPTION = 'Sacreon'

# pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

_SUB_DIRECTORIES = ['characters', 'items', 'spells', 'ui']
GFX = tools.graphics_from_directories(_SUB_DIRECTORIES)

fonts_path = os.path.join('resources', 'fonts')
FONTS = tools.load_all_fonts(fonts_path)

# sfx_path = os.path.join('resources', 'sounds')
# SFX = tools.load_all_sfx(sfx_path)

# music_path = os.path.join('resources', 'music')
# MUSIC = tools.load_all_music(music_path)
