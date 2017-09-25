import pygame as pg

from . import data


class Square:
    def __init__(self, row_num, col_num):
        self.row_num = row_num
        self.col_num = col_num
        self.create_images()
        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.obj = None
        self.state = 'IDLE'

    def create_images(self):
        width = height = data.SQUARE_SIZE
        image = pg.Surface((width, height)).convert()
        self.image_idle = image.copy()
        self.image_idle.fill(data.SQUARE_COLOR_IDLE)
        self.image_action = image.copy()
        self.image_action.fill(data.SQUARE_COLOR_ACTION)
        self.image_hover = image.copy()
        self.image_hover.fill(data.SQUARE_COLOR_HOVER)
        self.image_hl = image.copy()
        self.image_hl.fill(data.SQUARE_COLOR_HL)

    def get_obj(self, obj, change_position=True):
        self.obj = obj
        if change_position:
            self.obj.rect.center = self.rect.center

    def remove_obj(self):
        self.obj = None

    def change_state(self, new_state):
        self.state = new_state
        if self.state == 'IDLE':
            self.image = self.image_idle
        elif self.state == 'ACTION':
            self.image = self.image_action
        elif self.state == 'HOVER':
            self.image = self.image_hover
        elif self.state == 'HL':
            self.image = self.image_hl

    def highlight(self):
        self.change_state('HL')

    def unhighlight(self):
        self.change_state('IDLE')

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        hover = self.rect.collidepoint(pg.mouse.get_pos())
        if self.state == 'ACTION' and hover:
            self.change_state('HOVER')
        elif self.state == 'HOVER' and not hover:
            self.change_state('ACTION')
