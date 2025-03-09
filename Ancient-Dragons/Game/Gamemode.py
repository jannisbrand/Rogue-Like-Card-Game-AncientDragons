from typing import Any, Callable, cast

import pygame
from Characters.Base import Character
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from ECSO_Context import ECSO_Context
from Factories.Card_Factory import CardFactory
from Factories.Character_Factory import CharacterFactory
from Factories.GUI_Factory import GUIFactory
from Factories.Level_Factory import LevelFactory
from GUI.Base import GUISprite
from GUI.GUI import GUI
from GUI.Interactibles.Base import InteractibleSprite
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Interactibles.Environmental import InteractibleEnvironmental
from GUI.Interactibles.Slider import ProgressBar
from GUI.Interactibles.Sprite_List import SpriteList
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Levels.Menu import MenuLevel
from Renderer.Group_Types import SpriteGroupTypes
from Renderer.Renderer import Renderer
from Sprites.Base import Sprite
from Systems.Stacks.Base import CardStack


class Gamemode():
    def __init__(self, id: int, name: str, application, input_handler: InputHandler, renderer: "Renderer") -> None:
        # ### GAMEMODE RELATED ### #
        self.id = id
        self.name = name
        self.application = application
        self.ecso_context = ECSO_Context()
        self.input_handler = input_handler
        self.renderer = renderer

        self.is_initialised = False
        self.is_started = False
        self.is_finished = False
        self.next_gamemode: str

        self.is_generating_stacks: bool
        self.is_creating_gui: bool
        self.is_generating_level: bool
        self.is_shuffling: bool
        self.move_running: bool
        
        self.current_stage = 0
        self.current_round = 10
        self.level_end = False
        self.active_level: int  # Id of the level in the context
        self.active_player_character: int  # Id of the character in the context
        self.active_enemy_character: int
        self.active_play_stack: int
        self.selected_type: str

        self.on_round_start = None
        self.on_round_end = None
        # ### GAMEMODE RELATED ### #

        self.create_factories()

        # ### STACKS ### #
        self.card_stacks: dict[str, list] = {}
        # ### STACKS ### #

    def create_factories(self) -> None:
        # ### FACTORIES ### #
        self.factories: dict[str, Any] = {}
        for type in ["CARDS", "CHARACTERS", "LEVELS", "GUIS"]:
            try:
                match type:
                    case "CARDS":
                        self.factories[type] = CardFactory(self.application, self.renderer, self.ecso_context)
                    case "CHARACTERS":
                        self.factories[type] = CharacterFactory(self.application, self.renderer, self.ecso_context)
                    case "LEVELS":
                        self.factories[type] = LevelFactory(self.application, self.renderer, self.ecso_context)
                    case "GUIS":
                        self.factories[type] = GUIFactory(self.application, self.renderer, self.ecso_context, self.input_handler)
            except IndexError as e:
                print(f"[GAMEMODE] Factorie: {e} not found")
        # ### FACTORIES ### #

    def update_entities(self):
        stage_deletions = []
        try:
            for game_object_type, game_objects in self.ecso_context.game_objects.items():
                for game_object_entity, game_object in self.ecso_context.game_objects[game_object_type].items():
                    try:
                        if issubclass(type(game_object), Character):
                            stage_deletions.extend(self.handle_data_class(game_object))
                            continue
                        if issubclass(type(game_object), Level):
                            stage_deletions.extend(self.handle_level(game_object))
                            continue
                        if issubclass(type(game_object), GUISprite):
                            stage_deletions.extend(self.handle_gui(game_object))
                            continue
                        if issubclass(type(game_object), InteractibleSprite):
                            stage_deletions.extend(self.handle_interactible(game_object))
                            continue
                        if issubclass(type(game_object), InputSubscribtion):
                            stage_deletions.extend(self.handle_subscribtion(game_object))
                    except TypeError:
                        continue
                    except AttributeError:
                        continue
        except AttributeError as e:
            print("[GAMEMODE][UPDATE]", e)
        finally:
            for entity in stage_deletions:
                self.ecso_context.remove_game_object(entity)

    def handle_data_class(self, data_class) -> list:
        """DATA CLASS SPECIFICS"""
        return []

    def handle_level(self, level: Level) -> list:
        """LEVEL SPECIFICS"""
        deletion = []
        if level.is_visible:
            if len(level.groups()) == 0:
                self.renderer.add_sprite(SpriteGroupTypes.LEVELS, level)
        else:
            level.kill()

        if level.is_active:
            level.update()

        if level.destroy:
            level.kill()
            for gui_id in level.get_guis():
                gui = cast(GUI, self.ecso_context.get_game_object(gui_id, GUI))
                gui.destroy = True
                for interactible_id in gui.get_interactibles():
                    try:
                        """IF THE INTERACTIBLE IS ALREADY REMOVED"""
                        interactible = cast(InteractibleSprite, self.ecso_context.get_game_objects(interactible_id)[0])
                        interactible.destroy = True
                    except IndexError:
                        pass
            deletion.append(level.context_id)

        return deletion

    def handle_gui(self, gui: GUISprite) -> list:
        deletion = []
        if gui.is_visible:
            if len(gui.groups()) == 0:
                print(len(gui.groups()))
                self.renderer.add_sprite(SpriteGroupTypes.GUIS, gui)
        else:
            gui.kill()

        if gui.is_active:
            gui.update()

        if gui.destroy:
            gui.kill()
            deletion.append(gui.context_id)

        return deletion

    def handle_subscribtion(self, subscribtion: Any) -> list:
        """COULD BE ANY SUBSCRIBTION TYPE IN THE FUTURE"""
        return []

    def handle_interactible(self, interactible: InteractibleSprite) -> list:
        deletion = []
        if interactible.is_visible:
            if len(interactible.groups()) == 0:
                self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, interactible)
        else:
            interactible.kill()

        if interactible.is_active:
            interactible.update()

        if interactible.destroy:
            interactible.kill()
            try:
                on_hover = interactible.subscribtion_on_hover
                self.input_handler.remove_subscribtion(self.ecso_context.get_game_object(on_hover, InputSubscribtion))
                deletion.append(interactible.subscribtion_on_hover)
            except AttributeError:
                pass
            try:
                on_click = interactible.subscribtion_on_click
                self.input_handler.remove_subscribtion(self.ecso_context.get_game_object(on_click, InputSubscribtion))
                deletion.append(interactible.subscribtion_on_click)
            except AttributeError:
                pass
            deletion.append(interactible.context_id)

        return deletion
