import pygame as pg
import random

from .. import state_machine
from ..components import data
from ..components.board import Board
from ..components.effect import Effect
from ..components.flying_label import FlyingLabel
from ..components.task import Task
from ..components.ui import UI


class Fight(state_machine._State):
    def first_start(self):
        self.events = []
        self.create_everything()
        self.turn = 0
        self.ui = UI(self.events)
        self.tasks = pg.sprite.Group()
        self.move_available = False
        self.phase = None
        self.active_body = None
        self.ai_turn = False
        self.flying_labels = pg.sprite.Group()
        self.start_new_turn()

    def create_everything(self):
        board_width = self.persist['dungeon_info']['width']
        board_height = self.persist['dungeon_info']['height']
        self.board = Board(board_width, board_height)

        squad = self.persist['squad']
        squad_bodies = [char.create_body(True, self.events) for char in squad]
        monsters = self.persist['dungeon_info']['monsters']
        monsters_bodies = [char.create_body(True, self.events)
                           for char in monsters]
        random.shuffle(squad_bodies)
        squares_for_squad = self.board.get_squares_on_side(
            'LEFT', len(squad_bodies))
        for body, square in zip(squad_bodies, squares_for_squad):
            square.get_obj(body)
        random.shuffle(monsters_bodies)
        squares_for_monsters = self.board.get_squares_on_side(
            'RIGHT', len(monsters_bodies))
        for body, square in zip(monsters_bodies, squares_for_monsters):
            square.get_obj(body)
        self.bodies = squad_bodies + monsters_bodies
        # for body in self.bodies:
        #     empty_squares = self.board.get_all_squares(
        #         key=lambda x: x.obj is None)
        #     square = random.choice(empty_squares)
        #     square.get_obj(body)

    def change_phase(self, new_phase):
        if self.phase == new_phase:
            return
        self.phase = new_phase
        if self.ai_turn:
            move = attack = spells = items = finish = 'BLOCKED'
        else:
            if self.phase == 'MOVE':
                move = 'ACTIVE'
            else:
                move = 'IDLE' if self.can_move() else 'BLOCKED'
            if self.phase == 'ATTACK':
                attack = 'ACTIVE'
            else:
                attack = 'IDLE' if self.can_attack() else 'BLOCKED'
            if self.phase == 'SPELLS' or self.phase == 'CASTING':
                spells = 'ACTIVE'
            else:
                spells = 'IDLE' if self.can_cast_spell() else 'BLOCKED'
            if self.phase == 'ITEMS':
                items = 'ACTIVE'
            else:
                items = 'IDLE' if self.can_do_action() else 'BLOCKED'
            finish = 'IDLE' if self.can_do_action() else 'BLOCKED'
        self.ui.create_phase_buttons(move, attack, spells, items, finish)

    def start_new_turn(self):
        cross_bearers = [body for body in self.bodies
                         if 'first turn' in body.features]
        others = [body for body in self.bodies
                  if body not in cross_bearers]
        random.shuffle(cross_bearers)
        random.shuffle(others)
        self.bodies_to_act = cross_bearers + others
        for body in self.bodies_to_act:
            body.event_new_global_turn()
        self.next_body_to_act()

    def next_body_to_act(self):
        self.change_phase('BETWEEN_BODIES')
        self.ui.take_down_card('LEFT')
        self.active_body = self.bodies_to_act.pop(0)
        self.active_body.event_new_turn()
        self.board.bring_hoop_over(self.active_body, self.start_turn)

    def start_turn(self):
        self.ui.new_body_for_card('LEFT', self.active_body)
        health = self.active_body.current_health
        self.active_body.regenerate()
        finish_turn = self.active_body.update_effects_on_start()
        health_delta = self.active_body.current_health - health
        self.create_flying_labels('START', self.active_body, health_delta)
        self.ui.update_cards()
        alive = self.active_body.check_alive()
        if finish_turn or not alive:
            self.finish_body_turn()
            return
        self.move_available = True
        if self.active_body.faction == 'GOOD':
            self.ai_turn = False
            self.change_phase('TURN')
        elif self.active_body.faction == 'BAD':
            self.ai_turn = True
            self.change_phase('TURN_AI')
            self.target_for_ai = None
            self.ai_turn_start()

    def move(self):
        self.change_phase('MOVE')
        squares = self.board.get_squares_to_move(self.active_body)
        self.board.mark_squares(*squares, mark_as='ACTION')

    def attack(self):
        self.change_phase('ATTACK')
        squares = self.board.get_squares_to_attack(self.active_body)
        self.board.mark_squares(*squares, mark_as='ACTION')

    def open_items(self):
        self.change_phase('ITEMS')
        self.ui.open_items(self.active_body)

    def open_spell_book(self):
        self.change_phase('SPELLS')
        self.ui.open_spell_book(self.active_body)

    def choose_target_for_spell(self, spell):
        squares = self.board.get_squares_for_spell(self.active_body, spell)
        if squares:
            self.change_phase('CASTING')
            self.spell_in_casting = spell
            self.board.mark_squares(*squares, mark_as='ACTION')

    def back_to_nothing(self):
        self.change_phase('TURN')
        self.clear_everything()

    def clear_everything(self):
        self.board.mark_squares()
        self.ui.close_items()
        self.ui.close_spell_book()

    def finish_body_turn(self):
        self.active_body.update_effects_on_finish()
        task = Task(self.next_body_turn, 1)
        self.tasks.add(task)

    def next_body_turn(self):
        self.clear_everything()
        if self.bodies_to_act:
            self.next_body_to_act()
        else:
            self.start_new_turn()

    def start_animation(self):
        self.change_phase('ANIMATION')
        self.board.mark_squares()

    def after_move(self):
        self.move_available = False
        if self.ai_turn:
            self.change_phase('TURN_AI')
            self.ai_turn_start()
        else:
            self.change_phase('TURN')

    def after_attack(self):
        self.finish_body_turn()

    def after_casting_spell(self):
        self.finish_body_turn()

    def try_action(self, name):
        if name == 'MOVE':
            if self.phase == 'MOVE':
                self.back_to_nothing()
            elif self.can_do_action():
                if self.can_move():
                    self.back_to_nothing()
                    self.move()
        elif name == 'ATTACK':
            if self.phase == 'ATTACK':
                self.back_to_nothing()
            elif self.can_do_action():
                if self.can_attack():
                    self.back_to_nothing()
                    self.attack()
        elif name == 'SPELLS':
            if self.phase == 'SPELLS' or self.phase == 'CASTING':
                self.back_to_nothing()
            elif self.can_do_action():
                if self.can_cast_spell():
                    self.back_to_nothing()
                    self.open_spell_book()
        elif name == 'ITEMS':
            if self.phase == 'ITEMS':
                self.back_to_nothing()
            elif self.can_do_action():
                self.back_to_nothing()
                self.open_items()
        elif name == 'FINISH TURN':
            if self.can_do_action():
                self.finish_body_turn()

    def move_on_square(self, square):
        self.start_animation()
        self.board.move_obj(
            self.active_body, square, self.after_move)

    def attack_on_square(self, square):
        target = square.obj
        self.coordinate_attack(self.active_body, target)
        if self.active_body.attack_range == 1:
            self.start_animation()
            self.board.move_to_and_back(
                self.active_body, square, self.after_attack)
        else:
            task = Task(self.after_attack, 1)
            self.tasks.add(task)

    def coordinate_attack(self, attacker, victim):
        damage = attacker.calculate_damage()
        crit = attacker.crit_proc()
        stun = attacker.stun_proc()
        if stun:
            damage += attacker.bonus_damage_on_stun
            victim.add_effect(Effect('STUN', self.active_body))
            effects = ['STUN']
        else:
            effects = []
        if crit:
            damage = int(damage * attacker.crit_multi)
        if 'ignore defense' not in attacker.features:
            defense = victim.defense
            damage = max(0, damage - defense)
            if damage == 0:
                crit = False
        victim.get_damage(damage, attacker, crit=crit)
        vampired_health = int(0.01 * attacker.vampirism * damage)
        if vampired_health > 0:
            attacker.restore_health(vampired_health)
        xp = 0
        self.create_flying_labels(
            'ATTACK', attacker, victim, damage, crit, xp, effects)

    def cast_spell(self, spell, target=None):
        info = {}
        for body in self.bodies:
            info[body] = {}
            info[body]['health'] = body.current_health
            info[body]['effects'] = body.get_effects()
        if spell.target == 'GOOD' or spell.target == 'BAD':
            target = target.obj
        self.active_body.remove_mana(spell.manacost)
        spell.cast(self.active_body, target, self.bodies, self.board)
        self.back_to_nothing()
        self.ui.update_cards()
        if spell.fatigue:
            self.tasks.add(Task(self.after_casting_spell, 1))
        for body in info.keys():
            health_delta = body.current_health - info[body]['health']
            new_effects = [
                effect for effect in body.get_effects()
                if effect not in info[body]['effects']]
            if health_delta < 0:
                damage = -health_delta
                heal = 0
            elif health_delta > 0:
                damage = 0
                heal = health_delta
            else:
                damage = 0
                heal = 0
            self.create_flying_labels(
                'SPELL', body, damage, heal, new_effects)

    def ai_turn_start(self):
        if self.can_move():
            targets = self.board.get_targets_for_ai(self.active_body)
            if not targets:
                self.target_for_ai = None
                squares = self.board.get_squares_to_move(self.active_body)
                square = random.choice(squares)
            else:
                self.target_for_ai = random.choice(targets)
                square = self.target_for_ai[0]
            self.move_on_square(square)
        elif self.target_for_ai:
            self.attack_on_square(self.target_for_ai[1])
        elif self.can_attack():
            targets = self.board.get_squares_to_attack(self.active_body)
            target = random.choice(targets)
            self.attack_on_square(target)
        else:
            self.finish_body_turn()

    def spell_hovered(self, spell):
        self.spell_unhovered()
        squares = self.board.get_all_squares_in_range(
            self.active_body, spell.range)
        for square in squares:
            square.highlight()

    def spell_unhovered(self):
        for square in self.board.get_all_squares():
            if square.state == 'HL':
                square.unhighlight()

    def can_do_action(self):
        if not self.active_body:
            return False
        return self.phase in ['TURN', 'MOVE', 'ATTACK', 'SPELLS', 'ITEMS',
                              'CASTING']

    def can_move(self):
        if not self.active_body:
            return False
        if not self.move_available:
            return False
        if not self.ai_turn:
            if not self.can_do_action():
                return False
        squares = self.board.get_squares_to_move(self.active_body)
        return True if squares else False

    def can_attack(self):
        if not self.active_body:
            return False
        if not self.ai_turn:
            if not self.can_do_action():
                return False
        squares = self.board.get_squares_to_attack(self.active_body)
        return True if squares else False

    def can_cast_spell(self):
        if not self.active_body or not self.can_do_action():
            return False
        return True if self.active_body.character.spells else False

    def after_damage_dealt_to_body(self, body):
        if body not in self.bodies:
            return
        alive = body.check_alive()
        if not alive:
            square = self.board.get_square_by_obj(body)
            square.remove_obj()
            self.bodies.remove(body)
            if body in self.bodies_to_act:
                self.bodies_to_act.remove(body)
            if self.ui.get_body_from_card('RIGHT') == body:
                self.ui.take_down_card('RIGHT')
            if self.check_if_game_finished():
                self.events.append(dict(name='GAME FINISHED'))

    def prepare_to_finish_game(self):
        task = Task(self.finish_game, 1000)
        self.tasks.add(task)

    def finish_game(self):
        squad = [body.character for body in self.bodies
                 if body.faction == 'GOOD']
        self.persist['squad'] = squad
        self.next = 'LOBBY'
        self.done = True

    def check_if_game_finished(self):
        factions = set([body.faction for body in self.bodies])
        return True if len(factions) < 2 else False

    def create_flying_labels(self, name, *args):
        if name == 'ATTACK':
            [attacker, victim, damage, crit, xp, effects] = args
            self.create_labels(
                victim, damage=damage, crit=crit, effects=effects)
            self.create_labels(attacker, xp=xp)
        elif name == 'SPELL':
            [target, damage, heal, effects] = args
            self.create_labels(
                target, damage=damage, heal=heal, effects=effects)
        elif name == 'START':
            [body, health_delta] = args
            if health_delta > 0:
                self.create_labels(body, heal=health_delta)
            elif health_delta < 0:
                self.create_labels(body, damage=(-health_delta))
        elif name == 'XP':
            [body, lvl_up] = args
            self.create_labels(body, xp=1, lvl_up=lvl_up)

    def create_labels(self, body, damage=None, crit=None, heal=None, xp=None,
                      lvl_up=None, effects=None):
        point = body.rect.center
        point_one = point[0] - 40, point[1]
        point_two = point[0] + 40, point[1]
        if damage:
            damage = '-{}'.format(damage)
        if crit:
            crit = 'CRIT!'
        if heal:
            heal = '+{}'.format(heal)
        if xp:
            xp = '+{} XP'.format(xp)
        if lvl_up:
            lvl_up = 'LVL UP!'
        if damage and not crit and not effects:
            self.create_labels_at_point(point, damage)
        elif damage and crit and not effects:
            self.create_labels_at_point(point, damage, crit)
        elif damage and not crit and effects:
            self.create_labels_at_point(point_one, damage)
            self.create_labels_at_point(point_two, *effects)
        elif damage and crit and effects:
            self.create_labels_at_point(point_one, damage, crit)
            self.create_labels_at_point(point_two, *effects)
        elif heal and xp:
            if lvl_up:
                self.create_labels_at_point(point_one, xp, lvl_up)
            else:
                self.create_labels_at_point(point_one, xp)
            self.create_labels_at_point(point_two, heal)
        elif heal:
            self.create_labels_at_point(point, heal)
        elif xp:
            if lvl_up:
                self.create_labels_at_point(point, xp, lvl_up)
            else:
                self.create_labels_at_point(point, xp)
        elif effects:
            self.create_labels_at_point(point, *effects)

    def create_labels_at_point(self, point, *args):
        if len(args) == 1:
            centers = [point]
        elif len(args) == 2:
            center_one = point[0], point[1] + data.FLYING_LABEL_GAP
            center_two = point[0], point[1] - data.FLYING_LABEL_GAP
            centers = [center_one, center_two]
        for text, center in zip(args, centers):
            label = FlyingLabel(text, center=center)
            self.flying_labels.add(label)

    def left_click(self):
        something_clicked = self.ui.click()
        if something_clicked:
            return
        if self.phase == 'MOVE':
            square = self.board.get_square_by_point(pg.mouse.get_pos())
            if square is not None and square.state == 'HOVER':
                self.move_on_square(square)
        elif self.phase == 'ATTACK':
            square = self.board.get_square_by_point(pg.mouse.get_pos())
            if square is not None and square.state == 'HOVER':
                self.attack_on_square(square)
        elif self.phase == 'CASTING':
            square = self.board.get_square_by_point(pg.mouse.get_pos())
            if square is not None and square.state == 'HOVER':
                self.cast_spell(self.spell_in_casting, square)
        flag = False
        for body in self.bodies:
            if body.rect.collidepoint(pg.mouse.get_pos()):
                self.ui.new_body_for_card('RIGHT', body)
                flag = True
        if not flag:
            if self.phase in ['ITEMS', 'SPELLS', 'CASTING']:
                self.back_to_nothing()
                self.change_phase('TURN')

    def right_click(self):
        for body in self.bodies:
            if body.rect.collidepoint(pg.mouse.get_pos()):
                self.change_state('CHARACTER_VIEW', body=body)

    def check_events(self):
        for event in self.events:
            if event['name'] == 'GAME FINISHED':
                self.prepare_to_finish_game()
            elif event['name'] == 'PHASE BUTTON CLICKED':
                self.try_action(event['button'].name)
            elif event['name'] == 'DAMAGE DEALT':
                victim = event['victim']
                self.after_damage_dealt_to_body(victim)
                self.ui.update_cards()
            elif event['name'] == 'ITEM CONSUMED':
                event['item'].consume(self.active_body)
                self.active_body.character.load_items(
                    self.ui.armory.get_items())
                self.ui.update_cards()
            elif event['name'] == 'SPELL HOVERED':
                self.spell_hovered(event['spell'])
            elif event['name'] == 'SPELL UNHOVERED':
                self.spell_unhovered()
            elif event['name'] == 'SPELL CLICKED':
                spell = event['spell']
                for sp in self.ui.spell_book.spells:
                    if sp.name == spell.name:
                        sp.activate()
                if spell.can_be_casted(self.active_body, self.board):
                    if spell.target is None:
                        self.cast_spell(spell)
                    else:
                        self.choose_target_for_spell(spell)
            elif event['name'] == 'SPELL UNCLICKED':
                self.back_to_nothing()
                self.open_spell_book()
            elif event['name'] == 'XP GAINED':
                body = event['body']
                if body.xp == 0:
                    lvl_up = True
                else:
                    lvl_up = False
                self.create_flying_labels('XP', body, lvl_up)
        self.events[:] = []

    def change_state(self, new_state, **kwargs):
        if new_state == 'CHARACTER_VIEW':
            body = kwargs['body']
            self.persist['body_to_view'] = body
        self.next = new_state
        self.done = True

    def startup(self, persistant):
        self.persist = persistant
        if self.previous == 'LOBBY':
            self.first_start()

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.phase in ['ITEMS', 'SPELLS', 'CASTING']:
                    self.back_to_nothing()
                    self.change_phase('TURN')
                else:
                    self.change_state('PAUSE')
            elif event.key == pg.K_1:
                self.try_action('MOVE')
            elif event.key == pg.K_2:
                self.try_action('ATTACK')
            elif event.key == pg.K_3:
                self.try_action('SPELLS')
            elif event.key == pg.K_4:
                self.try_action('ITEMS')
            elif event.key == pg.K_5:
                self.try_action('FINISH TURN')
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click()
            elif event.button == 3:
                self.right_click()

    def draw(self, surface):
        surface.fill(data.BG_COLOR)
        self.board.draw(surface)
        for body in self.bodies:
            body.draw(surface)
        self.board.hoop.draw(surface)
        self.ui.draw(surface)
        for label in self.flying_labels:
            label.draw(surface)

    def update(self, surface, dt):
        self.check_events()
        self.tasks.update(dt * 1000)
        self.board.update(dt, self.phase, self.active_body)
        for body in self.bodies:
            body.update()
        self.ui.update(self.bodies)
        for label in self.flying_labels:
            label.update(dt)
        self.draw(surface)
