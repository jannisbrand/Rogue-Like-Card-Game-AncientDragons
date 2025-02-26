import os
import pygame
import pygame.display
from GUI.Base import GUI
from GUI.Interactibles.Button import Button
from Game.Gamemode_Handler import GamemodeHandler
from Game.Endless import Endless
from Game.Main_Menu import MainMenu
from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Event_Handler import Event_Handler
from Handlers.Subscriptions.Types import InputSubscribtion
from Renderer import Renderer
"""
Application # CONTEXT: Pygame / Window / Key mappings / Application state / etc.
    GameMode # STATEMACHINE: Game rules / Game state
        Level # INSTANCE: Active instance.
            NPC
        Character # INSTANCE: Active instance.
"""


class Application():
    def __init__(self, width: int, height: int, pos_x: int, pos_y: int, flags: int, icon_path: str):
        # Private
        self.__initialised = False
        self.__window: pygame.Surface
        self.__clock: pygame.time.Clock

        self.__icon_path = icon_path
        # self.__game_mode: None # Reference to the current game statemachine
        pygame.init()
        self.__clock = pygame.time.Clock()

        # Public
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._change_window(flags)

        self.active_game_mode: str
        self.window_should_close: bool

    def initialise(self) -> bool:
        self.window_should_close = False
        self.__initialised = True
        return True
    
    def get_window(self) -> pygame.Surface:
        return self.__window
    
    def get_clock(self) -> pygame.time.Clock:
        return self.__clock
    
    def set_window_caption(self, caption: str) -> bool:
        pygame.display.set_caption(caption, "")
        return True

    def _change_window(
            self,
            flags: int) -> bool:       
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (self.pos_x, self.pos_y)
        self.__window = pygame.display.set_mode((self.width, self.height), flags, 0, 0, 1)

        if self.__icon_path != "":
            icon = pygame.image.load(self.__icon_path)
            pygame.display.set_icon(icon)
        return True


if __name__ == "__main__":
    application = Application(1440, 900, (1440 - 720) - 450, 100, pygame.RESIZABLE, "")
    application.initialise()
    application.set_window_caption("Ancient Dragons - Ver: 0.001")
    
    event_handler = Event_Handler(application)
    input_handler = InputHandler(application)
    
    renderer = Renderer(application)
    renderer.initialise((100, 35, 55), 60)

    print("\n\n\n")

    gm_handler = GamemodeHandler()
    gm_handler.initialise()

    gm_menu = MainMenu(0, "START", input_handler, renderer)
    gm_menu.initialise()
    gm_handler.add_gamemode(gm_menu)

    gm_endless = Endless(1, "ENDLESS", input_handler, renderer)
    gm_handler.add_gamemode(gm_endless)

    while not application.window_should_close:
        # event_handler.handle_events()
        input_handler.update(pygame.event.get())

        # Do something with the event information
        gm_handler.update()

        renderer.render()
