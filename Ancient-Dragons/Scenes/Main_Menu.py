from encodings.punycode import T
from typing import Any, cast
import pygame
from Characters.Base import Character
from ECSO_Context import ECSO_Context
from GUI.Level_GUI import LevelGUI
from GUI.Level_GUI import LevelGUI
from GUI.Interactibles.Base import InteractibleSprite
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Interactibles.Environmental import InteractibleEnvironmental
from GUI.Interactibles.Slider import ProgressBar
from GUI.Interactibles.Sprite_List import SpriteList
from Scenes.Scene import Scene
from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Levels.Menu import MenuLevel
from Renderer.Group_Types import SpriteGroupTypes
from Renderer.Renderer import Renderer
from Sprites.Base import Sprite


class MainMenu(Scene):
    def __init__(self, id: int, name: str, application, input_handler: InputHandler, renderer: "Renderer") -> None:
        super().__init__(id, name, application, input_handler, renderer)
        pass

    def initialise(self) -> None:
        self.active_level = -1
        # buttons = [
        #     ("Endless", 200, 50, self.stop_game_mode)
        # ]
        # level = MenuLevel(self.ecso_context.next_object_id)
        # level.add_LevelGUI(self.factories["GUI"].generate_menu(710, 100, (150, 100), buttons))
        self.ecso_context = ECSO_Context()
        self.is_finished = False
        self.input_handler.reset()

        # ### (Manual) MAIN MENU ### #
        # LEVEL
        environment = {}
        entity = self.ecso_context.add_entity()
        rect = pygame.Rect(0, 0, 0, 0)
        rect.x = 0
        rect.y = 0

        entity = self.ecso_context.add_entity()
        level = MenuLevel(entity, "MAIN_MENU", rect, "", (13, 50, 89), 1440, 900, environment, "Ressources/Pictures/Levels/Menus/main-menu_background.png")
        self.active_level = entity
        self.ecso_context.add_game_object(entity, level)
        self.renderer.add_sprite(SpriteGroupTypes.GUIS, level)
        self.active_level = entity

        # GUI
        entity = self.ecso_context.add_entity()
        main_gui = LevelGUI(entity, "GUI_MAIN_MENU", level.rect, "", pygame.Color(25, 25, 25), 300, 900)
        main_gui.relative_x = 0
        main_gui.relative_y = 0
        main_gui.image.set_alpha(100)
        level.add_gui(entity)
        self.ecso_context.add_game_object(entity, main_gui)
        self.renderer.add_sprite(SpriteGroupTypes.GUIS, main_gui)

        # LOGO
        entity = self.ecso_context.add_entity()
        logo = InteractibleEnvironmental(entity, "INTERACTIBLE_ENVIRONMENTAL_SPRITE", main_gui.rect, "", (0, 0, 0), 300, 300, "Ressources/Pictures/Levels/Menus/main-menu_logo_final.png")
        logo.relative_x = 0
        logo.rect.y = 50
        self.ecso_context.add_game_object(entity, logo)
        main_gui.add_interactible(entity)
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, logo)

        # TITLE
        entity = self.ecso_context.add_entity()
        logo = InteractibleEnvironmental(entity, "INTERACTIBLE_ENVIRONMENTAL_SPRITE", main_gui.rect, "", (0, 0, 0), 1140, 120, "Ressources/Pictures/Levels/Menus/main-menu_title_test.png")
        logo.rect.x = (level.rect.width / 2 + main_gui.rect.width / 2) - logo.rect.width / 2
        logo.rect.y = level.rect.height / 2 - logo.rect.height / 2
        self.ecso_context.add_game_object(entity, logo)
        main_gui.add_interactible(entity)
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, logo)

        # BUTTON
        entity = self.ecso_context.add_entity()
        button = Button(entity, f"btn_main_menu_{entity}", main_gui.rect, pygame.Color(200, 0, 0), pygame.Color(240, 10, 10), "", "ENDLESS", 300, 50)
        button.relative_x = 0
        button.relative_y = 500
        main_gui.add_interactible(entity)
        self.ecso_context.add_game_object(entity, button)
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, button)

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

        try:
            cast(MenuLevel, self.ecso_context.get_game_object(self.active_level, MenuLevel)).destroy = True
        except AttributeError as e:
            print("[GAMEMODE][MENU] No active level could be found:", e)

    def update(self) -> None:
        # self.entity_update()
        pass

    # def entity_render(self):
    #     staged_sprites = []
    #     index = 0
    #     game_object_types = self.ecso_context.get_game_object_types()
    #     for game_object_type in game_object_types:
    #         for entity in self.ecso_context.get_game_object_entities():
    #             sprite_game_object = self.ecso_context.get_game_object(entity, game_object_types[index])
    #             if sprite_game_object is None:
    #                 continue
    #             if game_object_type is InputSubscribtion:
    #                 continue

    #             if len(sprite_game_object.groups()) < 1:
    #                 if not sprite_game_object.destroy and sprite_game_object.is_visible:
    #                     staged_sprites.append(sprite_game_object)
    #                     # cast(Renderer, self.renderer).add_sprite(sprite_game_object)
    #                     # TODO: Ich brauche eine Liste mit den Sprites und ein sprite das hinzugefügt werden soll.
    #                     # Dann eine fest definierte Reihenfolge der Types, damit die Sprites eingeordnet werden können.
    #                     # ODER!
    #                     # Sprite() bekommt eine z attribute, die das handelt. Z.b. B Buttons -> 0 ------ NAH Trotzdem braucht man die Typen Reihenfolge. :grimm:
    #         index += 1

    #     staged_sprites = self.apply_render_order(staged_sprites)
    #     cast(Renderer, self.renderer).add_sprites(staged_sprites)

    #     # for sprite in self.entity_update():
    #     #     if len(sprite.groups()) <= 0 and not sprite.destroy and sprite.is_visible:
    #     #         cast(Renderer, self.renderer).add_sprite(sprite)

    # def apply_render_order(self, list_of_sprites):
    #     render_order = (Level, GUISprite, InteractibleSprite)

    #     ordered_list = []
    #     for order_type in render_order:
    #         for sprite in list_of_sprites:
    #             if issubclass(type(sprite), order_type):
    #                 ordered_list.append(sprite)

    #     return ordered_list

    # def entity_update(self) -> list:
    #     list_of_sprites = []
    #     # ### Get game objects per type ### #
    #     for game_object_type, entity_game_objects in self.ecso_context.game_objects.items():
    #         self.handle_entity_states(game_object_type, entity_game_objects, list_of_sprites)
    #     # ### Get game object per type ### #

    #     return list_of_sprites

    # def handle_entity_states(self, game_object_type: Any, entity_game_objects: dict[int, Any], list_of_sprites: list):
    #     for entity, game_object in entity_game_objects.items():
    #         if game_object_type is InputSubscribtion:
    #             # NOTHING
    #             continue

    #         if game_object_type is Sprite:
    #             # NOTING
    #             continue

    #         if game_object_type is Button:
    #             # ### INTERACTIBLE BUTTON ### #
    #             game_object = cast(Button, game_object)
    #             if game_object.destroy:
    #                 # Removes input subscribtions from being checked
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
    #                 continue
    #             elif not game_object.is_visible:
    #                 game_object.kill()  # Removes the sprite from all groups

    #             game_object.update()
    #             list_of_sprites.append(game_object)
    #             continue
    #             # ### INTERACTIBLE BUTTON ### #

    #         if game_object_type is InteractibleCharacter:
    #             # ### INTERACTIBLE CHARACTER ### #
    #             game_object = cast(InteractibleCharacter, game_object)
    #             if game_object.destroy:
    #                 # Removes input subscribtions from being checked
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
    #                 continue
    #             elif game_object.is_visible:
    #                 game_object.kill()  # Removes the sprite from all groups

    #             game_object.update()
    #             list_of_sprites.append(game_object)
    #             continue
    #             # ### INTERACTIBLE CHARACTER ### #

    #         if game_object_type is Card:
    #             # ### INTERACTIBLE CARD ### #
    #             game_object = cast(Card, game_object)
    #             if game_object.destroy:
    #                 # Removes input subscribtions from being checked
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
    #                 continue
    #             elif game_object.is_visible:
    #                 game_object.kill()  # Removes the sprite from all groups

    #             game_object.update()
    #             list_of_sprites.append(game_object)
    #             continue
    #             # ### INTERACTIBLE CARD ### #

    #         if game_object_type is ProgressBar:
    #             # ### INTERACTIBLE PROGRESSBAR ### #
    #             game_object = cast(ProgressBar, game_object)
    #             if game_object.destroy:
    #                 # Removes input subscribtions from being checked
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
    #                 continue
    #             elif game_object.is_visible:
    #                 game_object.kill()  # Removes the sprite from all groups

    #             game_object.update()
    #             list_of_sprites.append(game_object)
    #             continue
    #             # ### INTERACTIBLE PROGRESSBAR ### #

    #         if game_object_type is SpriteList:
    #             # ### INTERACTIBLE SPRITELIST ### #
    #             game_object = cast(SpriteList, game_object)
    #             if game_object.destroy:
    #                 # Removes input subscribtions from being checked
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
    #                 self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
    #                 continue
    #             elif game_object.is_visible:
    #                 game_object.kill()  # Removes the sprite from all groups

    #             game_object.update()
    #             list_of_sprites.append(game_object)
    #             continue
    #             # ### INTERACTIBLE SPRITELIST ### #

    #         if issubclass(game_object_type, GUISprite):
    #             # ### GUI ### #
    #             game_object = cast(GUI, game_object)
    #             for interactible in game_object.get_interactibles():  # Removes id's of not existent entities
    #                 if not self.ecso_context.is_game_object_enity_existent(interactible):  # No entity -> No object -> No true :)
    #                     game_object.get_interactibles().remove(interactible)

    #             game_object.update()
    #             list_of_sprites.append(game_object)
    #             continue
    #             # ### GUI ### #

    #         if game_object_type is MenuLevel:
    #             # ### MENU LEVEL ### #
    #             game_object = cast(MenuLevel, game_object)
    #             if not game_object.is_active:
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 continue
    #             elif game_object.destroy:
    #                 game_object.kill()  # Removes the sprite from all groups
    #                 # REMOVE ALL CHILDS #
    #                 # Starts with destroing the deepest childs first and works upwards
    #                 for gui in game_object.get_guis():
    #                     gui_id = cast(int, gui)
    #                     gui = cast(GUI, self.ecso_context.get_game_object(gui_id, game_object_type))
    #                     for interactible in gui.get_interactibles():
    #                         self.ecso_context.remove_game_object(interactible)
    #                     gui.kill()
    #                     self.ecso_context.remove_game_object(gui_id)

    #                 # TEMP until Level class has a better sprite storage..
    #                 for _, sprites in game_object.environment.items():
    #                     for sprite in sprites:
    #                         sprite.kill()
    #                         self.ecso_context.remove_game_object(sprite.context_id)
    #                 # TEMP
    #                 self.ecso_context.remove_game_object(game_object.context_id)  # Removes that entity from existence
    #                 continue

    #             # TEMP until Level class has a better sprite storage..
    #             all_sprites_including_self = []
    #             all_sprites_including_self.append(game_object)
    #             for _, sprites in game_object.environment.items():
    #                 for sprite in sprites:
    #                     all_sprites_including_self.append(sprite)
    #             # TEMP
    #             game_object.update()
    #             list_of_sprites.extend(all_sprites_including_self)
    #             continue
    #             # ### MENU LEVEL ### #

    #         list_of_sprites.extend(game_object.get_sprites())
    #         game_object.update()
