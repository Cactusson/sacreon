import pygame as pg

from . import data
from .animation import Animation
from .hoop import Hoop
from .square import Square


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=data.BOARD_CENTER)
        self.grid = self.create_grid()
        self.squares = self.get_all_squares()
        self.animations = pg.sprite.Group()
        self.hoop = None
        self.obj_animated = None

    def create_image(self):
        width = (data.SQUARE_SIZE * self.width +
                 data.SQUARE_GAP * (self.width + 1))
        height = (data.SQUARE_SIZE * self.height +
                  data.SQUARE_GAP * (self.height + 1))
        image = pg.Surface((width, height)).convert()
        image.fill(data.BOARD_COLOR)
        return image

    def create_grid(self):
        grid = []
        for row_num in range(self.height):
            row = []
            for col_num in range(self.width):
                square = Square(row_num, col_num)
                x = (self.rect.x + square.rect.width * col_num +
                     data.SQUARE_GAP * (col_num + 1))
                y = (self.rect.y + square.rect.height * row_num +
                     data.SQUARE_GAP * (row_num + 1))
                square.rect.topleft = (x, y)
                row.append(square)
            grid.append(row)
        return grid

    def get_all_squares(self, key=lambda x: x):
        squares = [square for row in self.grid for square in row
                   if key(square)]
        return squares

    def get_squares_on_side(self, side, amount):
        if side == 'LEFT':
            col = 0
            offset = 1
        elif side == 'RIGHT':
            col = len(self.grid[0]) - 1
            offset = -1
        row = 0
        squares = []
        while amount:
            amount -= 1
            square = self.grid[row][col]
            squares.append(square)
            row += 1
            if row >= len(self.grid):
                row = 0
                col += offset
        return squares

    def get_square_by_point(self, point):
        for square in self.squares:
            if square.rect.collidepoint(point):
                return square

    def get_square_by_obj(self, obj):
        for square in self.squares:
            if square.obj == obj:
                return square

    def get_neighbors(self, square):
        row, col = square.row_num, square.col_num
        neighbors = []
        if row > 0:
            neighbors.append(self.grid[row-1][col])
        if row < self.height - 1:
            neighbors.append(self.grid[row+1][col])
        if col > 0:
            neighbors.append(self.grid[row][col-1])
        if col < self.width - 1:
            neighbors.append(self.grid[row][col+1])
        return neighbors

    def get_squares_to_move(self, obj):
        """
        Returns all squares the given obj can move to.
        They should be in move range and empty.
        """
        move_range = obj.speed
        square = self.get_square_by_obj(obj)
        return self.get_reachable_squares(square, move_range, empty=True)

    def get_squares_to_attack(self, obj):
        """
        Same as get_squares_to_move but uses different range
        and squares are not empty but with objs of opposite faction.
        """
        square = self.get_square_by_obj(obj)
        faction = 'GOOD' if obj.faction == 'BAD' else 'BAD'
        return self.get_reachable_squares(
            square, obj.attack_range, faction=faction, ignore=True)

    def get_squares_for_spell(self, obj, spell):
        square = self.get_square_by_obj(obj)
        target = spell.target
        if target == 'GOOD' or target == 'BAD':
            squares = self.get_reachable_squares(
                square, spell.range, faction=target, ignore=True)
        elif target == 'SQUARE':
            squares = self.get_reachable_squares(
                square, spell.range, empty=True, ignore=True)
        return squares

    def get_all_squares_in_range(self, obj, given_range):
        square = self.get_square_by_obj(obj)
        squares = self.get_reachable_squares(square, given_range, ignore=True)
        return squares

    def get_targets_for_ai(self, obj):
        targets = []
        victims = []
        original_square = self.get_square_by_obj(obj)
        squares = self.get_squares_to_move(obj)
        if original_square not in squares:
            squares.append(original_square)
        original_square.remove_obj()
        for square in squares:
            square.get_obj(obj, False)
            to_attack = self.get_squares_to_attack(obj)
            for target in to_attack:
                if target not in victims:
                    victims.append(target)
                    targets.append([square, target])
            square.remove_obj()
        original_square.get_obj(obj, False)
        return targets

    def get_enemies_around(self, body):
        square = self.get_square_by_obj(body)
        squares = self.get_reachable_squares(square, 1, faction='BAD')
        return [sq.obj for sq in squares if sq.obj is not None]

    def get_reachable_squares(
            self, square, steps, empty=False, faction=None, ignore=False):
        """
        Returns a list of squares that are N steps away from the given square.
        """
        accepted = [square]
        to_check = [square]
        checked = []
        while steps:
            steps -= 1
            squares_to_add = []
            if ignore:
                squares = to_check
            else:
                squares = accepted
            for sq in [s for s in squares if s not in checked]:
                checked.append(sq)
                neighbors = self.get_neighbors(sq)
                for n in neighbors:
                    if n not in to_check:
                        to_check.append(n)
                    if n not in accepted:
                        to_add = self.check_square(n, empty, faction)
                        if to_add:
                            squares_to_add.append(n)
            accepted.extend(squares_to_add)
            accepted = list(set(accepted))
        if not self.check_square(square, empty, faction):
            accepted.remove(square)
        return accepted

    def check_square(self, square, empty, faction):
        if empty and square.obj is not None:
            return False
        if faction is not None:
            if square.obj is None:
                return False
            if square.obj.faction != faction:
                return False
        return True

    def get_path(self, start_square, finish_square, only_empty=True):
        """
        Returns the shortest path from start_square to finish_square,
        which looks like this:
        [first_square, second_square, ..., target_square]
        If only_empty is True, only empty squares can be in the path.
        If there is no way to reach finish_square, returns None.
        """
        stack = [(start_square, [], [])]
        if only_empty:
            squares = self.get_all_squares(key=lambda x: x.obj is None)
        else:
            squares = self.squares

        while stack:
            current_square, visited, path = stack.pop(0)
            if current_square == finish_square:
                return path
            neighbors = [s for s in self.get_neighbors(current_square)
                         if s in squares]
            for neighbor in neighbors:
                if neighbor not in visited:
                    new_visited = visited + [current_square]
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_visited, new_path))

    def mark_squares(self, *squares, mark_as='IDLE'):
        if not squares:
            squares = self.squares
        for square in squares:
            square.change_state(mark_as)

    def move_obj(self, obj, target_square, callback):
        """
        Creates a queue of animations.
        """
        self.obj_animated = obj
        self.after_animations_callback = callback
        start_square = self.get_square_by_obj(obj)
        self.path = self.get_path(start_square, target_square)
        self.get_square_by_obj(obj).remove_obj()
        target_square.get_obj(obj, change_position=False)
        self.next_animation_in_queue()

    def move_to_and_back(self, obj, target_square, callback):
        self.obj_animated = obj
        self.after_animations_callback = callback
        finish_square = self.get_square_by_obj(obj)
        self.path = [target_square, finish_square]
        self.next_animation_in_queue()

    def next_animation_in_queue(self):
        if not self.path:
            self.after_animations_callback()
            return
        square = self.path.pop(0)
        rect = self.obj_animated.rect.copy()
        rect.center = square.rect.center
        x, y = rect.topleft
        animation = Animation(x=x, y=y, duration=350, round_values=True)
        self.animations.add(animation)
        animation.callback = self.next_animation_in_queue
        animation.start(self.obj_animated.rect)

    def bring_hoop_over(self, body, after_hoop_callback):
        if self.hoop is None:
            self.hoop = Hoop()
            self.hoop.rect.center = body.rect.center
            after_hoop_callback()
            return
        rect = self.hoop.rect.copy()
        rect.center = body.rect.center
        x, y = rect.topleft
        distance = (abs(rect.center[0] - x) +
                    abs(rect.center[1] - y))
        speed = 0.1
        duration = distance // speed
        animation = Animation(x=x, y=y, duration=duration, round_values=True,
                              transition='out_back')
        self.animations.add(animation)
        animation.start(self.hoop.rect)
        animation.callback = after_hoop_callback

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for square in self.squares:
            square.draw(surface)

    def update(self, dt, phase, active_body):
        if phase == 'MOVE' or phase == 'ATTACK' or phase == 'CASTING':
            for square in self.squares:
                square.update()
        self.hoop.rect.center = active_body.rect.center
        self.animations.update(dt * 1000)
