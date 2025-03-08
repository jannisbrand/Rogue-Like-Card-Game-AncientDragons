from email.mime import base
from itertools import tee
import os
import pygame
from random import randint
from re import S
from typing import Any, cast
from Characters.Base import Character
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from Components.Components import C_CARD_COSTS, C_DISPLAY_NAME, C_DISPLAY_TEXT
from ECSO_Context import ECSO_Context
from Factories.Card_Factory import CardFactory
from Factories.Character_Factory import CharacterFactory
from Factories.GUI_Factory import GUIFactory
from Factories.Level_Factory import LevelFactory
from GUI.GUI import GUI
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Interactibles.Sprite_List import SpriteList
from GUI.Interactibles.Slider import ProgressBar
from Game.Gamemode import Gamemode
from Handlers import Input_Handler
from Handlers.Flags import SubscriptionType
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Levels.Menu import MenuLevel
from Renderer.Group_Types import SpriteGroupTypes
from Renderer.Renderer import Renderer
from Sprites.Base import Sprite
from Systems.Stacks.Hand import Hand
from Systems.Stacks.Play import Play


# ### GLOBAL GAMERULES ### #
AMOUNT_PLAYER_CHARACTERS_MAX = 1
AMOUNT_CARDS_MAX = 9999
AMOUNT_CARDS_MIN = 0
AMOUNT_CARDS_ON_DECK_MAX = 5
AMOUNT_CARDS_ON_DECK_MIN = 0
AMOUNT_STACK_SHUFFLE = 10
AMOUNT_LEVELS_MAX = 9999
AMOUNT_OPPONENTS_CONCURRENT = 1
AMOUNT_ACTORS_MAX = 9999
# ACTOR FLAGS
LOADING_LEVEL_CONTINIOUS = True

# ### LOCAL GAMERULES ### #
# ACTOR FLAGS
CARDS_ALL = 0b1
CARDS_ONLY_TYPE_ATTACK = 0b10
CARDS_ONLY_TYPE_DEFENSE = 0b100
# ...
CHARACTERS_ALL = 0b1000
CHARACTERS_ONLY_WARRIOR = 0b10000
# ...


class Endless(Gamemode):
    def __init__(self, id: int, name: str, application, input_handler: Input_Handler, renderer: "Renderer") -> None:
        super().__init__(id, name, application, input_handler, renderer)
        # ### STAGES ### #
        # PLAYER MOVE #
        self.selected_target: int
        self.selected_card: int

    def initialise(self) -> bool:
        self.ecso_context = ECSO_Context()
        self.create_factories()
        self.card_stacks = {}
        self.is_finished = False
        self.is_initialised = False
        self.current_stage = 0
        self.active_level = -1  # No level active
        self.selected_type = ""
        self.selected_target = -1
        self.selected_card = -1
        self.active_player_character = -1
        self.active_enemy_character = -1

        self.is_creating_gui = False
        self.is_generating_level = False
        self.is_generating_stacks = False

        self.is_initialised = True

        # ### Generate all character classes and at selected
        cast(CharacterFactory, self.factories["CHARACTERS"]).fabricate_player_characters()

        # ### Generate all card entities ### #
        cast(CardFactory, self.factories["CARDS"]).fabricate_all()
        return True

    def __show_selection_menu(self) -> None:
        self.input_handler.reset()  # TODO: NEEDS TO STAY! Application context has to be referenced first. (To get access to App clock)

        # ### CHARACTER SELECTION MENU ### #
        entity = self.ecso_context.add_entity()
        rect = pygame.Rect(0, 0, 0, 0)
        character_selection = MenuLevel(entity, "CHARACTER_SELECTION", rect, "", (0, 0, 0), 1440, 900, {}, "Levels/Data/selection-menu_background_test.png")
        self.ecso_context.add_game_object(entity, character_selection)
        self.renderer.add_sprite(SpriteGroupTypes.LEVELS, character_selection)
        self.active_level = entity

        entity = self.ecso_context.add_entity()
        selection_menu = GUI(entity, "GUI_MAIN_MENU", character_selection.rect, "", (25, 25, 25), 300, 900)
        selection_menu.relative_x = 0
        selection_menu.relative_y = 0
        selection_menu.image.set_alpha(100)
        self.ecso_context.add_game_object(entity, selection_menu)
        character_selection.add_gui(entity)  # Adds context id of the gui to the parent level
        self.renderer.add_sprite(SpriteGroupTypes.GUIS, selection_menu)

        index = 0
        button_offset_y = 75
        for _, character in self.ecso_context.get_game_objects_of_type(PlayerCharacter):
            character = cast(PlayerCharacter, character)

            entity = self.ecso_context.add_entity()
            button = Button(entity, "SELECTION_BUTTON", selection_menu.rect, pygame.Color(200, 0, 0), pygame.Color(240, 10, 10), f"btn_select_character_{character.id}", character.get_name(), 200, 50)
            button.relative_x = 50
            button.relative_y = 50 + button_offset_y * index
            self.ecso_context.add_game_object(entity, button)
            selection_menu.add_interactible(entity)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, button)

            entity = self.ecso_context.add_entity()
            subscription = InputSubscribtion(SubscriptionType.CURSOR, button, button.on_hover, button.rect)
            button.subscribtion_on_hover = entity
            self.ecso_context.add_game_object(entity, subscription)
            self.input_handler.subscribe_to_event(subscription)
            
            entity = self.ecso_context.add_entity()
            button.callback_on_click = self.select_character
            subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, button, button.on_click, button.rect, mouse_buttons=(True, False, False))
            button.subscribtion_on_click = entity
            self.ecso_context.add_game_object(entity, subscription)
            self.input_handler.subscribe_to_event(subscription)
            index += 1

    def select_character(self, source: Any, mouse_buttons: tuple[bool, bool, bool]) -> None:
        selected_character = int(source.get_name().split("_")[3])

        for _, character in self.ecso_context.get_game_objects_of_type(PlayerCharacter):
            character = cast(PlayerCharacter, character)
            if character.id == selected_character:
                self.active_player_character = selected_character
                break
        # TODO: TEST IF SUBSCRIPTIONS GET DELETED self.input_handler.reset()

    def __create_stacks(self) -> None:
        # ### DRAW STACK ### #
        # Stack where cards are drawn from after each round
        # TIER-0 IMPLEMENTATION: Stack composition with cards only listed in chararcter object
        player_character_data = cast(PlayerCharacter, self.ecso_context.get_game_object(self.active_player_character, PlayerCharacter))

        play_entity = self.ecso_context.add_entity()
        stack = Play(play_entity)
        self.ecso_context.add_game_object(play_entity, stack)

        stack_composition = player_character_data.get_stack_composition()
        temporary_index = 0
        for card_name in stack_composition:
            if temporary_index % 2 == 0:  # Skips the card amount (As long as the "stack_composition" stays like this)
                for _ in range(stack_composition[temporary_index + 1]):
                    # GETS CARD ENTITY WITH THE NAME IN CARD COMPOSITION
                    card_entity = self.ecso_context.get_entity(C_DISPLAY_NAME, card_name)
                    # COPIES THE CARD TO BE USED. (LIKE BETHESDA DOES IT :))
                    copied_card = cast(CardFactory, self.factories["CARDS"]).copy_entity(card_entity)
                    stack.add_card(copied_card)
                    print("[GAMEMODE] Added card to play stack: ", copied_card)

            temporary_index += 1

        stack.shuffle(10)
        self.active_play_stack = stack.context_id  # Does what its says
        # ### DRAW STACK ### #

        # ### HAND STACK ### #
        play_stack = cast(Play, self.ecso_context.get_game_object(self.active_play_stack, Play))

        hand_entity = self.ecso_context.add_entity()
        stack = Hand(hand_entity)
        self.ecso_context.add_game_object(hand_entity, stack)

        # Add top cards to the hand stack of the character
        draw_amount = 5
        for _ in range(draw_amount):
            stack.add_card(play_stack.take_card())
        print("[GAMEMODE] Cards drawn from character: ", 0)

        player_character_data.set_stack(stack.context_id)
        # ### HAND STACK ### #

    def __stage_select_targets(self, source: Sprite, mouse_buttons: tuple[bool]) -> None:
        print("Target ID:", source.context_id)
        print("Target TYPE:", source.type_id)
        print("Target NAME:", source.name)
        try:
            match source.type_id:
                case "INTERACTIBLE_CARD_SPRITE":
                    self.selected_card = source.card_context_id  # Saves the entity id of selected card
                case "INTERACTIBLE_PLAYER_CHARACTER_SPRITE":
                    if self.selected_card != -1:
                        self.selected_target = source.character_context_id  # Saves object id of selected character
                        self.selected_type = PlayerCharacter
                case "INTERACTIBLE_ENEMY_CHARACTER_SPRITE":
                    if self.selected_card != -1:
                        self.selected_target = source.character_context_id
                        self.selected_type = StandardEnemy
        except AttributeError as e:
            print("[GAMEMODE][SELECTION] ", e)

    def __handle_move(self) -> None:
        try:
            result = self.ecso_context.card_system(self.selected_card, self.selected_type, self.selected_target)
            if not result:
                exit()

            # TEST TEST TEST TEST TEST TEST TEST TEST TEST
            # h = player_character_data = cast(Character, self.ecso_context.get_object("PLAYER_CHARACTERS", self.active_player_character)).get_health()
            # player_character_data = cast(Character, self.ecso_context.get_object("PLAYER_CHARACTERS", self.active_player_character)).set_health(h - 40)
            # TEST TEST TEST TEST TEST TEST TEST TEST TEST

            # Necessary reset
            self.selected_card = -1
            self.selected_target = -1
            self.selected_type = ""
        except AttributeError as e:
            print("[GAMEMODE][MOVEHANDLING] Cardsystem not defined:", e)
            # Necessary reset
            self.selected_card = -1
            self.selected_target = -1
            self.selected_type = ""


    def update(self) -> None:
        try:
            if self.current_stage == 0:
                level = cast(MenuLevel, self.ecso_context.get_game_object(self.active_level, MenuLevel))
            else:
                level = cast(Level, self.ecso_context.get_game_object(self.active_level, Level))

            player_character_data = cast(Character, self.ecso_context.get_game_object(self.active_player_character, PlayerCharacter))
            enemy_character_data = cast(StandardEnemy, self.ecso_context.get_game_object(self.active_enemy_character, StandardEnemy))

            match self.current_stage:
                case 0:
                    # Character selection menu
                    if self.active_level == -1:
                        self.__show_selection_menu()

                    if self.active_player_character != -1:
                        try:
                            cast(MenuLevel, self.ecso_context.get_game_object(self.active_level, MenuLevel)).destroy = True
                        except AttributeError as e:
                            print("[GAMEMODE][ENDLESS] Menu level class not found:", e)
                        self.current_stage = 1
                case 1:
                    # STACK AND HAND
                    self.is_generating_stacks = True
                    self.__create_stacks()
                    self.is_generating_stacks = False
                    self.current_stage = 2
                case 2:
                    if level is None:
                        generated_entity = cast(LevelFactory, self.factories["LEVELS"]).generate_level()
                        generated_level = cast(Level, self.ecso_context.get_game_object(generated_entity, Level))
                        self.ecso_context.add_game_object(generated_entity, generated_level)  #TODO: generate_level already adds the entity to the context
                        self.active_level = generated_entity
                        self.is_generating_level = False
                    self.current_stage = 3
                case 3:
                    if self.active_enemy_character == -1:
                        new_enemy = cast(CharacterFactory, self.factories["CHARACTERS"]).fabricate_enemy()
                        if new_enemy is not None:
                            self.active_enemy_character = new_enemy
                            self.current_stage = 4
                case 4:
                    # The player & enemy characters are assingned to the same gui
                    if not self.is_creating_gui:
                        self.is_creating_gui = True
                        # self.__create_character_gui()
                        cast(GUIFactory, self.factories["GUIS"]).generate_character_gui(self.active_level, self.active_player_character, self.active_enemy_character, self.__stage_select_targets)

                    gui_entities = level.get_guis()
                    for gui_entity in gui_entities:
                        gui_object = cast(GUI, self.ecso_context.get_game_object(gui_entity, GUI))
                        if gui_object.type_id == "GUI_CHARACTERS":
                            self.is_creating_gui = False
                            self.current_stage = 5
                case 5:
                    if not self.is_creating_gui:
                        self.is_creating_gui = True
                        cast(GUIFactory, self.factories["GUIS"]).generate_card_gui(self.active_level, self.active_play_stack, player_character_data.get_stack(), self.__stage_select_targets)

                    gui_entities = level.get_guis()
                    for gui_entity in gui_entities:
                        gui_object = cast(GUI, self.ecso_context.get_game_object(gui_entity, GUI))
                        if gui_object.type_id == "GUI_CARDS":
                            self.is_creating_gui = False
                            self.current_stage = 10
                case 10:
                    """GAME LOGIC"""
                    """ TARGET - ACTION SELECTION """
                    try:
                        if self.on_round_start is not None:
                            self.on_round_start()
                    except TypeError as e:
                        print("[GAMEMODE][ENDLESS] Callback 'on_round_start' is not callable:", e)

                    # Pre move selection
                    if self.selected_card != -1 and self.selected_target != -1:
                        print("[GAMEMODE][SELECTION] Selected card: ", self.selected_card)
                        print("[GAMEMODE][SELECTION] Selected character: ", self.selected_target)
                        self.current_stage = 11
                case 11:
                    """ MOVE HANDLING """
                    # Calls system /systems that handle the start of a move
                    # Sets next stage
                    self.move_running = True
                    self.__handle_move()
                    self.current_stage = 10
                    if not self.move_running:
                        self.current_stage = 12
                case 12:
                    """ ENEMY MOVES"""
                    # The enemy does its thing
                    self.current_stage = 13
                case 13:
                    # ### RESTART LOOP ### #
                    try:
                        if self.on_round_end is not None:
                            self.on_round_end()
                    except TypeError as e:
                        print("[GAMEMODE][ENDLESS] Callback 'on_round_end' is not callable:", e)
                    self.current_stage = 1  # Starts from the beginning
                case 999:
                    # Error GUI popup
                    # Return to main menu or restart
                    pass
                case 9:
                    self.is_finished = True
                    self.next_gamemode = "START"

            # ### ### #
            # level.update()
            if self.active_player_character != -1:
                self.__sync_character(self.ecso_context.get_game_object(player_character_data.get_sprite(), InteractibleCharacter), player_character_data)
            if self.active_enemy_character != -1:
                self.__sync_character(self.ecso_context.get_game_object(enemy_character_data.get_sprite(), InteractibleCharacter), enemy_character_data)
            # self.renderer.add_sprites(level.get_sprites())  # Adds all sprites from the active level to the renderers sprite group
        except ValueError as e:
            print("Flupp", e)
        except AttributeError as e:
            print(f"[GAMEMODE] No level found: {e}")

    def __sync_character(self, sprite, data: Character):
        # sprite.set_display_name(data.get_name())
        # sprite.set_health(data.get_health())
        # Maybe update image?
        # TODO: Do we even need that?? The systems update the character class and card entities.
        #       The character classes update elements like the health bar on a change.. :think:
        if data.health_changed:
            pb = cast(ProgressBar, self.ecso_context.get_game_object(153, ProgressBar))
            pb.set_value(data.get_health())
        
        if sprite is not None and not data.is_alive:
            sprite.destroy = True
