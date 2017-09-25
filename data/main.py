from . import prepare, state_machine
from .states.armory_view import ArmoryView
from .states.character_view import CharacterView
from .states.fight import Fight
from .states.lobby import Lobby
from .states.lose_screen import LoseScreen
from .states.main_menu import MainMenu
from .states.pause import Pause
from .states.reward import Reward
from .states.sacreon import Sacreon
from .states.win_screen import WinScreen


def main():
    run_it = state_machine.StateMachine(prepare.ORIGINAL_CAPTION)
    state_dict = {'ARMORY_VIEW': ArmoryView(),
                  'CHARACTER_VIEW': CharacterView(),
                  'FIGHT': Fight(),
                  'LOBBY': Lobby(),
                  'LOSE_SCREEN': LoseScreen(),
                  'MAIN_MENU': MainMenu(),
                  'PAUSE': Pause(),
                  'REWARD': Reward(),
                  'SACREON': Sacreon(),
                  'WIN_SCREEN': WinScreen(),
                  }
    run_it.setup_states(state_dict, 'MAIN_MENU')
    run_it.main()
