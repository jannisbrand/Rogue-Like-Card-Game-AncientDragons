from typing import Any, Callable, cast
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
from GUI.Interactibles.Slider import ProgressBar
from GUI.Interactibles.Sprite_List import SpriteList
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Levels.Menu import MenuLevel
from Renderer import Renderer
from Sprites.Base import Sprite


class Gamemode():
    def __init__(self, id: int, name: str, input_handler: InputHandler, renderer: "Renderer") -> None:
        # ### GAMEMODE RELATED ### #
        self.id = id
        self.name = name
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
        self.active_level: int  # Id of the level in the context
        self.active_player_character: int  # Id of the character in the context
        self.active_enemy_character: int
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
                        self.factories[type] = CardFactory(self.ecso_context)
                    case "CHARACTERS":
                        self.factories[type] = CharacterFactory(self.ecso_context)
                    case "LEVELS":
                        self.factories[type] = LevelFactory(self.ecso_context)
                    case "GUIS":
                        self.factories[type] = GUIFactory(self.ecso_context, self.input_handler)
            except IndexError as e:
                print(f"[GAMEMODE] Factorie: {e} not found")
        # ### FACTORIES ### #

    def entity_render(self):
        staged_sprites = []
        index = 0
        game_object_types = self.ecso_context.get_game_object_types()
        for game_object_type in game_object_types:
            for entity in self.ecso_context.get_game_object_entities():
                sprite_game_object = self.ecso_context.get_game_object(entity, game_object_types[index])
                if sprite_game_object is None:
                    continue
                if game_object_type is InputSubscribtion:
                    continue

                if len(sprite_game_object.groups()) < 1:
                    if not sprite_game_object.destroy and sprite_game_object.is_visible:
                        staged_sprites.append(sprite_game_object)
                        # cast(Renderer, self.renderer).add_sprite(sprite_game_object)
                        # TODO: Ich brauche eine Liste mit den Sprites und ein sprite das hinzugefügt werden soll.
                        # Dann eine fest definierte Reihenfolge der Types, damit die Sprites eingeordnet werden können.
                        # ODER!
                        # Sprite() bekommt eine z attribute, die das handelt. Z.b. B Buttons -> 0 ------ NAH Trotzdem braucht man die Typen Reihenfolge. :grimm:
            index += 1

        staged_sprites = self.apply_render_order(staged_sprites)
        cast(Renderer, self.renderer).add_sprites(staged_sprites)

        # for sprite in self.entity_update():
        #     if len(sprite.groups()) <= 0 and not sprite.destroy and sprite.is_visible:
        #         cast(Renderer, self.renderer).add_sprite(sprite)

    def apply_render_order(self, list_of_sprites):
        render_order = (Level, GUISprite, InteractibleSprite)

        ordered_list = []
        for order_type in render_order:
            for sprite in list_of_sprites:
                if issubclass(type(sprite), order_type):
                    ordered_list.append(sprite)

        return ordered_list

    def entity_update(self) -> list:
        list_of_sprites = []
        # ### Get game objects per type ### #
        for game_object_type, entity_game_objects in self.ecso_context.game_objects.items():
            self.handle_entity_states(game_object_type, entity_game_objects, list_of_sprites)
        # ### Get game object per type ### #

        return list_of_sprites

    def handle_entity_states(self, game_object_type: Any, entity_game_objects: dict[int, Any], list_of_sprites: list):
        for entity, game_object in entity_game_objects.items():
            if game_object_type is InputSubscribtion:
                # NOTHING
                continue

            if game_object_type is Sprite:
                # NOTING
                continue

            if game_object_type is Button:
                # ### INTERACTIBLE BUTTON ### #
                game_object = cast(Button, game_object)
                if game_object.destroy:
                    # Removes input subscribtions from being checked
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
                    game_object.kill()  # Removes the sprite from all groups
                    self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
                    continue
                elif not game_object.is_visible:
                    game_object.kill()  # Removes the sprite from all groups

                game_object.update()
                list_of_sprites.append(game_object)
                continue
                # ### INTERACTIBLE BUTTON ### #

            if game_object_type is InteractibleCharacter:
                # ### INTERACTIBLE CHARACTER ### #
                game_object = cast(InteractibleCharacter, game_object)
                if game_object.destroy:
                    # Removes input subscribtions from being checked
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
                    game_object.kill()  # Removes the sprite from all groups
                    self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
                    continue
                elif game_object.is_visible:
                    game_object.kill()  # Removes the sprite from all groups

                game_object.update()
                list_of_sprites.append(game_object)
                continue
                # ### INTERACTIBLE CHARACTER ### #

            if game_object_type is Card:
                # ### INTERACTIBLE CARD ### #
                game_object = cast(Card, game_object)
                if game_object.destroy:
                    # Removes input subscribtions from being checked
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
                    game_object.kill()  # Removes the sprite from all groups
                    self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
                    continue
                elif game_object.is_visible:
                    game_object.kill()  # Removes the sprite from all groups

                game_object.update()
                list_of_sprites.append(game_object)
                continue
                # ### INTERACTIBLE CARD ### #

            if game_object_type is ProgressBar:
                # ### INTERACTIBLE PROGRESSBAR ### #
                game_object = cast(ProgressBar, game_object)
                if game_object.destroy:
                    # Removes input subscribtions from being checked
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
                    game_object.kill()  # Removes the sprite from all groups
                    self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
                    continue
                elif game_object.is_visible:
                    game_object.kill()  # Removes the sprite from all groups

                game_object.update()
                list_of_sprites.append(game_object)
                continue
                # ### INTERACTIBLE PROGRESSBAR ### #

            if game_object_type is SpriteList:
                # ### INTERACTIBLE SPRITELIST ### #
                game_object = cast(SpriteList, game_object)
                if game_object.destroy:
                    # Removes input subscribtions from being checked
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_hover)
                    self.input_handler.remove_subscribtion(game_object.subscribtion_on_click)
                    game_object.kill()  # Removes the sprite from all groups
                    self.ecso_context.remove_game_object(entity)  # Removes that entity from existence
                    continue
                elif game_object.is_visible:
                    game_object.kill()  # Removes the sprite from all groups

                game_object.update()
                list_of_sprites.append(game_object)
                continue
                # ### INTERACTIBLE SPRITELIST ### #

            if issubclass(game_object_type, GUISprite):
                # ### GUI ### #
                game_object = cast(GUI, game_object)
                for interactible in game_object.get_interactibles():  # Removes id's of not existent entities
                    if not self.ecso_context.is_game_object_enity_existent(interactible):  # No entity -> No object -> No true :)
                        game_object.get_interactibles().remove(interactible)

                game_object.update()
                list_of_sprites.append(game_object)
                continue
                # ### GUI ### #

            if game_object_type is MenuLevel:
                # ### MENU LEVEL ### #
                game_object = cast(MenuLevel, game_object)
                if not game_object.is_active:
                    game_object.kill()  # Removes the sprite from all groups
                    continue
                elif game_object.destroy:
                    game_object.kill()  # Removes the sprite from all groups
                    # REMOVE ALL CHILDS #
                    # Starts with destroing the deepest childs first and works upwards
                    for gui in game_object.get_guis():
                        gui_id = cast(int, gui)
                        gui = cast(GUI, self.ecso_context.get_game_object(gui_id, game_object_type))
                        for interactible in gui.get_interactibles():
                            self.ecso_context.remove_game_object(interactible)
                        gui.kill()
                        self.ecso_context.remove_game_object(gui_id)

                    # TEMP until Level class has a better sprite storage..
                    for _, sprites in game_object.environment.items():
                        for sprite in sprites:
                            sprite.kill()
                            self.ecso_context.remove_game_object(sprite.context_id)
                    # TEMP
                    self.ecso_context.remove_game_object(game_object.context_id)  # Removes that entity from existence
                    continue

                # TEMP until Level class has a better sprite storage..
                all_sprites_including_self = []
                all_sprites_including_self.append(game_object)
                for _, sprites in game_object.environment.items():
                    for sprite in sprites:
                        all_sprites_including_self.append(sprite)
                # TEMP
                game_object.update()
                list_of_sprites.extend(all_sprites_including_self)
                continue
                # ### MENU LEVEL ### #

            list_of_sprites.extend(game_object.get_sprites())
            game_object.update()
