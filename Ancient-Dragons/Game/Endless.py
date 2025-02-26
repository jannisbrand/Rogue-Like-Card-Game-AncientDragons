from itertools import tee
import pygame
from random import randint
from re import S
from typing import Any
from Components.Components import C_CARD_COSTS, C_DISPLAY_NAME
from ECSO_Context import ECSO_Context
from GUI.Base import GUI
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Interactibles.Slider import ProgressBar
from Game.Gamemode import Gamemode
from Handlers import Input_Handler
from Handlers.Flags import SubscriptionType
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Static.Menu import MenuLevel
from Renderer import Renderer
from Sprites.Base import Sprite


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
    def __init__(self, id: int, name: str, input_handler: Input_Handler, renderer: "Renderer") -> None:
        super().__init__(id, name, input_handler, renderer)
        # ### STAGES ### #
        # PLAYER MOVE #
        self.selected_character: int
        self.selected_card: int

    def initialise(self) -> bool:
        self.ecso_context = ECSO_Context()
        self.create_factories()
        self.card_stacks = {}
        self.is_finished = False
        self.is_initialised = False
        self.current_stage = 0
        self.active_level = -1  # No level active
        self.active_character = -1

        # ### Generate all character classes and at selected
        self.factories["CHARACTERS"].fabricate_all()
        # TODO: self.active_character = selected_character

        # ### Generate all card entities ### #
        self.factories["CARDS"].fabricate_all()

        # ### Generate a level to start the game with
        # TODO:
        # self.factories["LEVELS"].generate_level()
        #self.active_level = self.ecso_context.get_object("LEVELS", 0)
   
        # self.__show_main_menu()

        # self.input_handler.clear_subscriptions()

        # # ### CHARACTER SELECTION MENU ### #
        # character_selection = MenuLevel(self.ecso_context.next_object_id)

        # ### STAGES ### #
        # PLAYER MOVE #
        self.selected_character = -1
        self.selected_card = -1
        # ### STAGES ### #
        
        self.is_initialised = True

        self.test = None
        return True
    
    def __show_main_menu(self) -> None:
        self.input_handler.reset()

        # ### CHARACTER SELECTION MENU ### #
        character_selection = MenuLevel(0, "CHARACTER_SELECTION")

        selection_menu = GUI(pygame.Color(25, 25, 25, 180), "CHARACTER_SELECTION", 500, 700, 470, 100)
        index = 0
        button_offset_y = 50
        for character in self.ecso_context.get_objects("CHARACTERS"):
            button = Button(selection_menu.get_rect(), pygame.Color(35, 35, 80), pygame.Color(45, 45, 90), f"btn_select_character_{character.get_name()}", character.get_name(), 16, 200, 50, 50, 50 + (button_offset_y * index))
            subscription = InputSubscribtion(SubscriptionType.CURSOR, button, button.on_hover, button.get_rect())
            self.input_handler.subscribe_to_event(subscription)
            button.callback_on_click = self.select_character
            subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, button, button.on_click, button.get_rect(), mouse_buttons=(True, False, False))
            self.input_handler.subscribe_to_event(subscription)
            selection_menu.add_interactible(button)
            index += 1

        character_selection.add_gui(selection_menu)
        self.active_level = self.ecso_context.add_object("LEVELS", character_selection)
    
    def select_character(self, source: Any, mouse_buttons: tuple[bool, bool, bool]) -> None:
        characters = self.ecso_context.get_objects("CHARACTERS")
        selected_name = source.get_name().split("_")[3]

        index = 0
        for character in characters:
            if character.get_name() == selected_name:
                self.active_character = index
                break
            else:
                self.active_character = -1
            index += 1
        
        # Remove Level
        # self.ecso_context.remove_object_by_id("LEVLES", self.active_level)
        self.ecso_context.get_object("LEVELS", self.active_level).deactivate()
        self.input_handler.reset()  # TODO: Remove just menu subs
        
    def __create_stacks(self) -> None:
        # ### DRAW STACK ### #
        # Stack where cards are drawn from after each round
        # TIER-0 IMPLEMENTATION: Stack composition with cards only listed in chararcter object
        character = self.ecso_context.get_object("CHARACTERS", self.active_character)

        stack_name = "DRAW"
        if stack_name not in self.card_stacks:
            self.card_stacks[stack_name] = []

        stack_composition = character.get_stack_composition()
        temporary_index = 0
        for card in stack_composition:
            if temporary_index % 2 == 0:  # Skips the card amount (As long as the "stack_composition" stays like this)
                for _ in range(stack_composition[temporary_index + 1]):
                    entity_id = self.ecso_context.get_entity(C_DISPLAY_NAME, card)
                    copied_card = self.factories["CARDS"].copy_entity(entity_id)
                    self.card_stacks["DRAW"].append(copied_card)
                    print("[GAMEMODE] Stack composition with id: ", entity_id)

            temporary_index += 1

        print(self.card_stacks["DRAW"])
        self.card_stacks["DRAW"] = self.shuffle_stack(self.card_stacks["DRAW"], 10)
        print(self.card_stacks["DRAW"])
        # ### DRAW STACK ### #

        # ### HAND STACK ### #
        stack_name = "HAND"
        if stack_name not in self.card_stacks:
            self.card_stacks[stack_name] = []

        # Add top cards to the hand stack of the character
        draw_amount = 5
        for _ in range(draw_amount):
            entity = self.card_stacks["DRAW"].pop()
            character.add_card_to_hand(entity)
            self.card_stacks["HAND"].append(entity)
        print("[GAMEMODE] Cards drawn from character: ", 0)
        # ### HAND STACK ### #

    def shuffle_stack(self, stack: list, times: int) -> list:
        for _ in range(times):
            random_index_1 = randint(0, len(stack) - 1)
            random_index_2 = randint(0, len(stack) - 1)
            temporary_id = stack[random_index_1]
            stack[random_index_1] = stack[random_index_2]
            stack[random_index_2] = temporary_id
        print("[GAMEMODE] Stack shuffled!")
        return stack

    def __create_card_gui(self) -> None:
        level = self.ecso_context.get_object("LEVELS", self.active_level)
        background_color = pygame.Color(10, 10, 10)
        gui_hand = GUI(background_color, "CARD_HAND", 1040, 200, 100, 700)
        gui_hand.image.set_alpha(50)
        level = self.ecso_context.get_object("LEVELS", self.active_level)
        level.add_gui(gui_hand)

        x_offset = 150
        index = 0
        for entity in self.ecso_context.get_object("CHARACTERS", self.active_character).get_hand():
            base_color = pygame.Color(80, 20, 60)
            name = self.ecso_context.get_component(entity, C_DISPLAY_NAME)
            card = Card(entity, "CARD", name, base_color, 200, 300, "")
            cost_resource = pygame.image.load("Levels/Data/gangsta_tree.png")
            card.set_cost(self.ecso_context.get_component(entity, C_CARD_COSTS).value, cost_resource)
            card.set_title(self.ecso_context.get_component(entity, C_DISPLAY_NAME).value)
            
            card.rect.x = (gui_hand.rect.x + 200) + (x_offset * index)
            card.rect.y = gui_hand.rect.y + 20
            card.animation_initial_y = card.rect.y  # TODO: Not a good  solution
            card.callback_on_click = self.__stage_select_targets
            subscription = InputSubscribtion(SubscriptionType.CURSOR, card, card.on_hover, card.rect)
            self.input_handler.subscribe_to_event(subscription)
            subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, card, card.on_click, card.rect, [], mouse_buttons=(True, False, False))
            self.input_handler.subscribe_to_event(subscription)
            gui_hand.add_interactible(card)
            index += 1

        # ### CARD STACK ### #
        color = pygame.Color(0, 0, 255)
        stack_icon = Button(gui_hand.rect, color, None, "STACK_ICON", "", 16, 100, 100, 20, 20)
        stack_icon.set_text("STACK", 26)
        gui_hand.add_interactible(stack_icon)

    def __create_character_gui(self) -> None:
        level = self.ecso_context.get_object("LEVELS", self.active_level)
        ground_level = level.get_environment_type("FOREGROUND2")[0].rect.y
        
        background_color = pygame.Color(0, 0, 0, 100)
        gui_characters = GUI(background_color, "CHARACTERS", 1440, 400, 0, ground_level - 400)
        gui_characters.image.set_alpha(0)
        level.add_gui(gui_characters)

        character = self.ecso_context.get_object("CHARACTERS", self.active_character)

        # ### MAIN CHARACTER SPRITE
        base_color = pygame.Color(255, 255, 255)
        # resource = pygame.image.load("Levels/Data/gangsta_tree.png")
        char = InteractibleCharacter(self.active_character, "CHARACTER", character.get_name(), base_color, 100, 100, "Levels/Data/gangsta_tree.png")
        char.callback_on_click = self.__stage_select_targets
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, char, char.on_click, char.rect, [], (True, False, False))
        self.input_handler.subscribe_to_event(subscription)
        char.rect.x = 50
        char.rect.y = ground_level - char.rect.height
        gui_characters.add_interactible(char)

        # ### CHARACTER HEALTH SPRITE TODO: Finish character display and events
        base_color = pygame.Color(50, 120, 90)
        value_color = pygame.Color(255, 0, 0)
        progressbar = ProgressBar(len(gui_characters.interactibles) -1, "PLAYER_HEALTH", "PROGRESSBAR", base_color, value_color, 100, 20, 50, 0, "")
        progressbar.rect.x = 50
        progressbar.rect.y = char.rect.y - progressbar.rect.height - 20
        char.on_health_changed = progressbar.set_current
        gui_characters.add_interactible(progressbar)

    def __stage_select_targets(self, source: Sprite, mouse_buttons: tuple[bool]) -> None:
        print("Target ID:", source.id)
        print("Target TYPE:", source.type)
        print("Target NAME:", source.name)
        try:
            match source.type:
                case "CARD":
                    self.selected_card = source.id  # Saves the entity id of selected card
                case "CHARACTER":
                    if self.selected_card != -1:
                        self.selected_character = source.id  # Saves object id of selected character
        except AttributeError as e:
            print("[GAMEMODE][SELECTION] ", e)

    def __handle_move(self) -> None:
        try:
            card_components = self.ecso_context.get_components(self.selected_card)
            for component in card_components:
                match component:
                    case "Skill":
                        print("SKILL")

            self.move_running = False  # TODO: Set its value to the result of the system
        except KeyError as e:
            print("[GAMEMODE][MOVE_HANDLING] Context returned no components: ", e)


    def update(self) -> None:
        try:
            level = self.ecso_context.get_object("LEVELS", self.active_level)

            match self.current_stage:
                case 0:
                    # Character selection menu
                    if self.active_level == -1:
                        self.__show_main_menu()

                    if self.active_character != -1:
                        self.current_stage = 1
                case 1:
                    # STACK AND HAND
                    self.is_generating_stacks = True
                    self.__create_stacks()
                    self.is_generating_stacks = False
                    self.current_stage = 2
                case 2:
                    self.shuffle_stack(self.card_stacks["DRAW"], AMOUNT_STACK_SHUFFLE)
                    self.current_stage = 3
                case 3:
                    self.is_generating_level = True
                    new_level = self.factories["LEVELS"].generate_level()
                    id = self.ecso_context.add_object("LEVELS", new_level)
                    self.active_level = id
                    self.is_generating_level = False
                    self.current_stage = 4
                case 4:
                    gui = level.get_gui("CHARACTERS")
                    if gui is None:
                        self.is_creating_gui = True
                        self.__create_character_gui()
                    if gui.is_active:
                        self.is_creating_gui = False
                        self.current_stage = 5
                case 5:
                    gui = level.get_gui("CARD_HAND")
                    if gui is None:
                        self.is_creating_gui = True
                        self.__create_card_gui()
                    if gui.is_active:
                        self.is_creating_gui = False
                        self.current_stage = 6
                case 6:
                    # Pre move selection
                    if self.selected_card != -1 and self.selected_character != -1:
                        print("[GAMEMODE][SELECTION] Selected card: ", self.selected_card)
                        print("[GAMEMODE][SELECTION] Selected character: ", self.selected_character)
                        self.current_stage = 7
                case 7:
                    # Calls system /systems that handle the start of a move
                    # Sets next stage
                    self.move_running = True
                    self.__handle_move()
                    if not self.move_running:
                        self.current_stage = 8
                case 8:
                    exit()
                case 999:
                    # Error GUI popup
                    # Return to main menu or restart
                    pass
                case 9:
                    self.is_finished = True
                    self.next_gamemode = "START"

            # ### ### #
            level.update()
            self.renderer.add_sprites(level.get_sprites())  # Adds all sprites from the active level to the renderers sprite group
        except ValueError as e:
            print("Flupp", e)
        except AttributeError as e:
            print(f"[GAMEMODE] No level found: {e}")
