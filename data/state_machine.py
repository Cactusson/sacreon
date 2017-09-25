import pygame as pg

from . import prepare


class StateMachine(object):
    """
    Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here.
    """
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.state_dict = {}
        self.state_name = None
        self.state = None
        self.fullscreen = False

    def setup_states(self, state_dict, start_state):
        """
        Given a dictionary of States and a State to start in,
        builds the self.state_dict.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup({})

    def update(self, dt):
        """
        Checks if a state is done or has called for a game quit.
        State is flipped if neccessary and State.update is called.
        """
        # you may want to pass self.keys to self.state.update
        state_flipped = False
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
            state_flipped = True
        if not state_flipped:
            self.state.update(self.screen, dt)

    def flip_state(self):
        """
        When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed.
        """
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(persist)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            pg.display.set_mode(prepare.SCREEN_SIZE, pg.FULLSCREEN)
        else:
            pg.display.set_mode(prepare.SCREEN_SIZE)

    def event_loop(self):
        """
        Process all events and pass them down to current State.  The f5 key
        globally turns on/off the display of FPS in the caption
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    if pg.key.get_pressed()[pg.K_LALT]:
                        self.done = True
                elif event.key == pg.K_f:
                    self.toggle_fullscreen()
            self.state.get_event(event)

    def main(self):
        """
        Main loop for entire program.
        """
        while not self.done:
            time_delta = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(time_delta)
            pg.display.update()
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pg.display.set_caption(with_fps)


class _State(object):
    """
    This is a prototype class for States.  All states should inherit from it.
    No direct instances of this class should be created. get_event and update
    must be overloaded in the childclass.  startup and cleanup need to be
    overloaded when there is data that must persist between States.
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        """
        Processes events that were passed from the main event loop.
        Must be overloaded in children.
        """
        pass

    def startup(self, persistant):
        """
        Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time.
        """
        self.persist = persistant

    def cleanup(self):
        """
        Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False.
        """
        self.done = False
        return self.persist

    def update(self, surface, dt):
        """
        Update function for state.  Must be overloaded in children.
        """
        pass
