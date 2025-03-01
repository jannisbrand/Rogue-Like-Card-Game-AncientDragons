from typing import Any, cast
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
from Sprites.Base import Sprite


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
        # LEVEL
        environment = {}
        entity = self.ecso_context.add_entity()
        sprite = Sprite(entity, "LEVEL_BACKGROUND_1", pygame.Rect, "", (0, 0, 0), 1440, 900, "Levels/Data/cloud.png")
        environment["BACKGROUND1"] = [sprite]
        self.ecso_context.add_game_object(entity, sprite)

        entity = self.ecso_context.add_entity()
        level = MenuLevel(entity, "MAIN_MENU", pygame.Rect, "", (13, 50, 89), 1440, 900, environment)
        self.active_level = entity
        self.ecso_context.add_game_object(entity, level)

        # GUI
        entity = self.ecso_context.add_entity()
        main_gui = GUI(entity, "GUI_MAIN_MENU", level.rect, "", pygame.Color(25, 25, 25), 500, 700)
        main_gui.rect.x = 470
        main_gui.rect.y = 100
        main_gui.image.set_alpha(180)
        level.add_gui(entity)
        self.ecso_context.add_game_object(entity, main_gui)

        # BUTTON
        entity = self.ecso_context.add_entity()
        button = Button(entity, f"btn_main_menu_{entity}", main_gui.rect, pygame.Color(35, 35, 80), pygame.Color(45, 45, 90), "", "ENDLESS", 200, 50)
        button.rect.x += 50
        button.rect.y += 50
        main_gui.add_interactible(entity)
        self.ecso_context.add_game_object(entity, button)

        entity = self.ecso_context.add_entity()
        subscription = InputSubscribtion(SubscriptionType.CURSOR, button, button.on_hover, button.rect)
        button.subscribtion_on_hover = entity
        self.input_handler.subscribe_to_event(subscription)
        self.ecso_context.add_game_object(entity, subscription)

        entity = self.ecso_context.add_entity()
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, button, button.on_click, button.rect, mouse_buttons=(True, False, False))
        button.callback_on_click = self.stop_game_mode
        button.subscribtion_on_click = entity
        self.input_handler.subscribe_to_event(subscription)
        self.ecso_context.add_game_object(entity, subscription)
        # ### (Manual) MAIN MENU ### #

    def stop_game_mode(self, source: Button, mouse_buttons: tuple[bool]) -> None:
        self.is_finished = True
        self.next_gamemode = "ENDLESS"
        self.input_handler.set_wait(0.25)

    def update(self) -> None:
        # level = self.ecso_context.get_object("LEVELS", self.active_level)
        self.test = []
        for game_object_type, entity_game_objects in self.ecso_context.game_objects.items():
            print(game_object_type)
            print(entity_game_objects)
            self.handle_entity_update(game_object_type, entity_game_objects)

        cast(Renderer, self.renderer).add_sprites(self.test)
        # self.renderer.add_sprites(level.get_sprites())

    def handle_entity_update(self, game_object_type: Any, entity_game_objects: dict[int, Any]):
        for entity, game_object in entity_game_objects.items():
            print(entity, game_object)
            if game_object_type is InputSubscribtion:
                continue
            if game_object_type is Sprite:
                self.test.append(game_object)
                continue
            if game_object_type is GUI:
                game_object.update()
                self.test.append(game_object)
                continue
            if game_object_type is Button:
                game_object.update()
                self.test.append(game_object)
                continue
            
            self.test.extend(game_object.get_sprites())
            game_object.update()
