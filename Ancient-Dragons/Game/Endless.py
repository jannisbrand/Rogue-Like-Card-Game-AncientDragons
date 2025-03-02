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
from Components.Components import C_CARD_COSTS, C_DISPLAY_NAME
from ECSO_Context import ECSO_Context
from Factories.Card_Factory import CardFactory
from Factories.Character_Factory import CharacterFactory
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

    def __show_main_menu(self) -> None:
        self.input_handler.reset()  # TODO: NEEDS TO STAY! Application context has to be referenced first. (To get access to App clock)

        # ### CHARACTER SELECTION MENU ### #
        entity = self.ecso_context.add_entity()
        rect = pygame.Rect(0, 0, 0, 0)
        character_selection = MenuLevel(entity, "CHARACTER_SELECTION", rect, "", (0, 0, 0), 1440, 900, {})
        self.ecso_context.add_game_object(entity, character_selection)
        self.active_level = entity

        entity = self.ecso_context.add_entity()
        selection_menu = GUI(entity, "GUI_MAIN_MENU", character_selection.rect, "", (25, 25, 25), 500, 700)
        selection_menu.rect.x = 470
        selection_menu.rect.y = 100
        selection_menu.image.set_alpha(180)
        self.ecso_context.add_game_object(entity, selection_menu)
        character_selection.add_gui(entity)  # Adds context id of the gui to the parent level

        index = 0
        button_offset_y = 50
        for _, character in self.ecso_context.get_game_objects_of_type(PlayerCharacter):
            character = cast(PlayerCharacter, character)

            entity = self.ecso_context.add_entity()
            button = Button(entity, "SELECTION_BUTTON", selection_menu.rect, pygame.Color(35, 35, 80), pygame.Color(45, 45, 90), f"btn_select_character_{character.id}", character.get_name(), 200, 50)
            button.relative_x = 50
            button.relative_y = 50 + button_offset_y * index
            self.ecso_context.add_game_object(entity, button)
            selection_menu.add_interactible(entity)

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

        stack_name = "DRAW"
        if stack_name not in self.card_stacks:
            self.card_stacks[stack_name] = []

        stack_composition = player_character_data.get_stack_composition()
        temporary_index = 0
        for card in stack_composition:
            if temporary_index % 2 == 0:  # Skips the card amount (As long as the "stack_composition" stays like this)
                for _ in range(stack_composition[temporary_index + 1]):
                    entity_id = self.ecso_context.get_entity(C_DISPLAY_NAME, card)
                    copied_card = cast(CardFactory, self.factories["CARDS"]).copy_entity(entity_id)
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
            player_character_data.add_card_to_hand(entity)
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
        level = cast(Level, self.ecso_context.get_game_object(self.active_level, Level))

        color = pygame.Color(10, 10, 10)
        gui_entity = self.ecso_context.add_entity()
        gui_cards = GUI(gui_entity, "GUI_CARDS", level.rect, "", color, 1040, 200)
        gui_cards.image.set_alpha(50)
        gui_cards.relative_x = (level.rect.x + level.rect.width / 2) - int(gui_cards.rect.width / 2)
        gui_cards.relative_y = (level.rect.x + level.rect.height) - gui_cards.rect.height
        self.ecso_context.add_game_object(gui_entity, gui_cards)
        level.add_gui(gui_entity)

        player_character_data = cast(PlayerCharacter, self.ecso_context.get_game_object(self.active_player_character, PlayerCharacter))

        x_offset = 175
        index = 0
        for entity in player_character_data.get_cards_on_hand():
            card_entity = self.ecso_context.add_entity()
            color = pygame.Color(80, 20, 60)
            card = Card(card_entity, "INTERACTIBLE_CARD_SPRITE", gui_cards.rect, "", color, 200, 300)  # It's possible to use an image as a base background!
            cost_resource = pygame.image.load("Levels/Data/gangsta_tree.png")  # Background of the card costs area (Mana)
            try:
                # CARD TITLE
                card.set_title(cast(C_DISPLAY_NAME, self.ecso_context.get_component(entity, C_DISPLAY_NAME)).value)
                # CARD COSTS
                card.set_cost(cast(C_CARD_COSTS, self.ecso_context.get_component(entity, C_CARD_COSTS)).value, cost_resource)
            except Exception:
                print("FUCK!?")
            card.relative_x = 200 + (x_offset * index)
            card.relative_y = 20
            # card.animation_initial_y = card.rect.y  # TODO: Not a good  solution
            card.callback_on_click = self.__stage_select_targets
            self.ecso_context.add_game_object(card_entity, card)
            gui_cards.add_interactible(card_entity)

            subscribtion_entity = self.ecso_context.add_entity()
            subscribtion = InputSubscribtion(SubscriptionType.CURSOR, card, card.on_hover, card.rect)
            self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
            self.input_handler.subscribe_to_event(subscribtion)

            subscribtion_entity = self.ecso_context.add_entity()
            subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, card, card.on_click, card.rect, [], mouse_buttons=(True, False, False))
            self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
            self.input_handler.subscribe_to_event(subscription)
            index += 1

        # ### CARD PULL STACK ### #
        color = pygame.Color(0, 0, 245)
        highlight = pygame.Color(0, 0, 255)
        entity = self.ecso_context.add_entity()
        pull_stack = Button(entity, "INTERACTIBLE_BUTTON_SPRITE", gui_cards.rect, color, highlight, "", "STACK", 100, 100)
        pull_stack.relative_x = 50
        pull_stack.relative_y = 50
        pull_stack.set_text("STACK")
        pull_stack.font_size = 32
        self.ecso_context.add_game_object(entity, pull_stack)
        gui_cards.add_interactible(entity)

        # ### END TURN BUTTON ### #
        # TODO: Implement Button wich calls a methond wich sets "self.move_running to false"

    def __create_character_gui(self) -> None:
        level = cast(Level, self.ecso_context.get_game_object(self.active_level, Level))
        ground_level = level.get_environment_type("FOREGROUND2")[0].rect.y  # ...
        
        color = pygame.Color(0, 0, 0)
        entity = self.ecso_context.add_entity()
        gui_characters = GUI(entity, "GUI_CHARACTERS", level.rect, "", color, 1440, 400)
        gui_characters.image.set_alpha(50)
        gui_characters.relative_x = 0
        gui_characters.relative_y = ground_level - gui_characters.rect.height
        self.ecso_context.add_game_object(entity, gui_characters)
        level.add_gui(entity)

        player_character_data = cast(Character, self.ecso_context.get_game_object(self.active_player_character, PlayerCharacter))
        
        self.active_enemy_character = cast(CharacterFactory, self.factories["CHARACTERS"]).fabricate_enemy()
        enemy_character_data = cast(StandardEnemy, self.ecso_context.get_game_object(self.active_enemy_character, StandardEnemy))

        # ### MAIN CHARACTER SPRITE ### #
        # BASE
        list_of_images = os.listdir("Levels/Data/Charakters")
        base_color = pygame.Color(255, 255, 255)
        resource = ""
        for image_name in list_of_images:
            if image_name.split(".")[0] == player_character_data.get_name().lower():
                resource = image_name
        player_character_sprite_entity = self.ecso_context.add_entity()
        player_character_sprite = InteractibleCharacter(entity, "INTERACTIBLE_PLAYER_CHARACTER_SPRITE", gui_characters.rect, "", base_color, 300, 300, f"Levels/Data/Charakters/{resource}")
        player_character_sprite.relative_x = 50
        player_character_sprite.relative_y = gui_characters.rect.height - player_character_sprite.rect.height
        player_character_sprite.callback_on_click = self.__stage_select_targets

        subscription_entity = self.ecso_context.add_entity()
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, player_character_sprite, player_character_sprite.on_click, player_character_sprite.rect, [], (True, False, False))
        self.ecso_context.add_game_object(subscription_entity, subscription)
        self.input_handler.subscribe_to_event(subscription)

        self.ecso_context.add_game_object(player_character_sprite_entity, player_character_sprite)
        gui_characters.add_interactible(player_character_sprite_entity)
        player_character_data.set_sprite(player_character_sprite_entity)
        # ## SURROUNDING INDICATORS
        # PROGRESS BAR AS HEALTH TODO: 26.02.2025: Add everything to the dict and try categories of interactibles :)
        base_color = pygame.Color(50, 120, 90)
        value_color = pygame.Color(255, 0, 0)
        progressbar_entity = self.ecso_context.add_entity()
        progressbar = ProgressBar(progressbar_entity, "INTERACTIBLE_PLAYER_PROGRESSBAR_SPRITE", player_character_sprite.rect, "", base_color, value_color, player_character_sprite.rect.width, 20, player_character_data.get_health(), 0, "")
        progressbar.relative_x = 0
        progressbar.relative_y = -40
        player_character_data.on_health_changed = progressbar.set_value

        self.ecso_context.add_game_object(progressbar_entity, progressbar)
        gui_characters.add_interactible(progressbar_entity)
        # SPRITE LIST AS EFFECT LIST
        # base_color = pygame.Color(50, 120, 90)
        # sprite_list = SpriteList(len(gui_characters.interactibles) - 1, "PLAYER_EFFECTS", "SPRITELIST", base_color, player_character_sprite.rect.width, 50)
        # sprite_list.rect.x = player_character_sprite.rect.x
        # sprite_list.rect.y = player_character_sprite.rect.y - player_character_sprite.rect.height - 70
        # player_character_data.on_effect_added = sprite_list.add_sprite
        # gui_characters.add_interactible(sprite_list)
        # ### MAIN PLAYER SPRITE ### #

        # ### MAIN ENEMY SPRITE ### #
        base_color = pygame.Color(255, 255, 255)
        list_of_enemy_images = os.listdir("Levels/Data/Enemies")
        resource = list_of_enemy_images[randint(0, len(list_of_enemy_images) - 1)]
        enemy_character_sprite_entity = self.ecso_context.add_entity()
        enemy_character_sprite = InteractibleCharacter(enemy_character_sprite_entity, "INTERACTIBLE_ENEMY_CHARACTER_SPRITE", gui_characters.rect, "", base_color, 300, 300, f"Levels/Data/Enemies/{resource}")
        enemy_character_sprite.callback_on_click = self.__stage_select_targets
        enemy_character_sprite.relative_x = 1000
        enemy_character_sprite.relative_y = gui_characters.rect.height - enemy_character_sprite.rect.height

        subscription_entity = self.ecso_context.add_entity()
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, enemy_character_sprite, enemy_character_sprite.on_click, enemy_character_sprite.rect, [], (True, False, False))
        self.ecso_context.add_game_object(subscription_entity, subscription)
        self.input_handler.subscribe_to_event(subscription)

        self.ecso_context.add_game_object(enemy_character_sprite_entity, enemy_character_sprite)
        gui_characters.add_interactible(enemy_character_sprite_entity)
        enemy_character_data.set_sprite(enemy_character_sprite_entity)
        # ## SURROUNDING INDICATORS
        # PROGRESS BAR AS HEALTH TODO: 26.02.2025: Add everything to the dict and try categories of interactibles :)
        base_color = pygame.Color(50, 120, 90)
        value_color = pygame.Color(255, 0, 0)
        progressbar_entity = self.ecso_context.add_entity()
        progressbar = ProgressBar(progressbar_entity, "INTERACTIBLE_ENEMY_PROGRESSBAR_SPRITE", enemy_character_sprite.rect, "", base_color, value_color, enemy_character_sprite.rect.width, 20, enemy_character_data.get_health(), 0)
        progressbar.relative_x = 0
        progressbar.relative_y = -40
        enemy_character_sprite.on_health_changed = progressbar.set_value

        self.ecso_context.add_game_object(progressbar_entity, progressbar)
        gui_characters.add_interactible(progressbar)
        # SPRITE LIST AS EFFECT LIST
        # base_color = pygame.Color(50, 120, 90)
        # sprite_list = SpriteList(len(gui_characters.interactibles) - 1, "ENEMY_EFFECTS", "SPRITELIST", base_color, enemy_character_sprite.rect.width, 50)
        # sprite_list.rect.x = enemy_character_sprite.rect.x
        # sprite_list.rect.y = enemy_character_sprite.rect.y - enemy_character_sprite.rect.height - 70
        # enemy_character_data.on_effect_added = sprite_list.add_sprite
        # gui_characters.add_interactible(sprite_list)

        # # SPRITE LIST TEST
        # for image in os.listdir("Levels/Data/Charakters"):
        #     sprite = Sprite(0, "EFFECT_SPRITE", "", (0, 0, 0), 20, 20)
        #     sprite.image = pygame.image.load(f"Levels/Data/Charakters/{image}")
        #     sprite_list.add_sprite(sprite)
        # ### MAIN ENEMY SPRITE ### #

    def __stage_select_targets(self, source: Sprite, mouse_buttons: tuple[bool]) -> None:
        print("Target ID:", source.context_id)
        print("Target TYPE:", source.type_id)
        print("Target NAME:", source.name)
        try:
            match source.type_id:
                case "INTERACTIBLE_CARD_SPRITE":
                    self.selected_card = source.context_id  # Saves the entity id of selected card
                case "INTERACTIBLE_PLAYER_CHARACTER_SPRITE":
                    if self.selected_card != -1:
                        self.selected_target = source.context_id  # Saves object id of selected character
                        self.selected_type = source.type_id
                case "INTERACTIBLE_ENEMY_CHARACTER_SPRITE":
                    if self.selected_card != -1:
                        self.selected_target = source.context_id
                        self.selected_type = source.type_id
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
                        self.__show_main_menu()

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
                    self.shuffle_stack(self.card_stacks["DRAW"], AMOUNT_STACK_SHUFFLE)
                    self.current_stage = 3
                case 3:
                    if level is None:
                        generated_entity = cast(LevelFactory, self.factories["LEVELS"]).generate_level()
                        generated_level = cast(Level, self.ecso_context.get_game_object(generated_entity, Level))
                        self.ecso_context.add_game_object(generated_entity, generated_level)
                        self.active_level = generated_entity
                        self.is_generating_level = False
                    self.current_stage = 4
                case 4:
                    # The player & enemy characters are assingned to the same gui
                    if not self.is_creating_gui:
                        self.is_creating_gui = True
                        self.__create_character_gui()

                    gui_entities = level.get_guis()
                    for gui_entity in gui_entities:
                        gui_object = cast(GUI, self.ecso_context.get_game_object(gui_entity, GUI))
                        if gui_object.type_id == "GUI_CHARACTERS":
                            self.is_creating_gui = False
                            self.current_stage = 5
                case 5:
                    if not self.is_creating_gui:
                        self.is_creating_gui = True
                        self.__create_card_gui()

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
                    
                    # ### RESTART LOOP ### #
                    try:
                        if self.on_round_end is not None:
                            self.on_round_end()
                    except TypeError as e:
                        print("[GAMEMODE][ENDLESS] Callback 'on_round_end' is not callable:", e)
                    self.current_stage = 10
                case 13:
                    # Unnecessary?
                    pass
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
                self.__sync_character(player_character_data.get_sprite(), player_character_data)
            if self.active_enemy_character != -1:
                self.__sync_character(enemy_character_data.get_sprite(), enemy_character_data)
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
        pass
