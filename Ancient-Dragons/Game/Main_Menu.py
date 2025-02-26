from typing import Any
import pygame
from ECSO_Context import ECSO_Context
from GUI.Base import GUI
from GUI.Interactibles.Button import Button
from Game.Gamemode import Gamemode
from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Levels.Static.Menu import MenuLevel
from Renderer import Renderer


class MainMenu(Gamemode):
    def __init__(self, id: int, name: str, input_handler: InputHandler, renderer: "Renderer") -> None:
        super().__init__(id, name, input_handler, renderer)
        pass

    def initialise(self) -> None:
        # buttons = [
        #     ("Endless", 200, 50, self.stop_game_mode)
        # ]
        # level = MenuLevel(self.ecso_context.next_object_id)
        # level.add_gui(self.factories["GUI"].generate_menu(710, 100, (150, 100), buttons))
        self.ecso_context = ECSO_Context()
        self.is_finished = False
        self.input_handler.reset()

        # ### (Manual) MAIN MENU ### #
        level = MenuLevel(0, "MAIN_MENU")
        level.set_image(pygame.image.load("Levels/Data/cloud.png"))
        self.active_level = self.ecso_context.add_object("LEVELS", level)
        main_gui = GUI(pygame.Color(25, 25, 25, 180), "MAIN_GUI", 500, 700, 470, 100)
        button = Button(main_gui.get_rect(), pygame.Color(35, 35, 80), pygame.Color(45, 45, 90), "btn_start_ENDLESS", "ENDLESS 8==D", 16, 200, 50, 50, 50)
        subscription = InputSubscribtion(SubscriptionType.CURSOR, button, button.on_hover, button.get_rect())
        self.input_handler.subscribe_to_event(subscription)
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, button, self.stop_game_mode, button.get_rect(), mouse_buttons=(True, False, False))
        self.input_handler.subscribe_to_event(subscription)
        main_gui.add_interactible(button)

        level.add_gui(main_gui)
        # ### (Manual) MAIN MENU ### #

    def stop_game_mode(self, source: Button, mouse_buttons: tuple[bool]) -> None:
        self.is_finished = True
        self.next_gamemode = "ENDLESS"
        self.input_handler.set_wait(0.25)

    def update(self) -> None:
        level = self.ecso_context.get_object("LEVELS", self.active_level)
        level.update()
        self.renderer.add_sprites(level.get_sprites())
