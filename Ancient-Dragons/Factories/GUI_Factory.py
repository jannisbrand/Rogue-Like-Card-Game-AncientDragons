import os
from random import randint
from typing import Any, cast
import pygame
from Characters.Base import Character
from Characters.Boss_Enemy import BossEnemy
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from Components.Components import C_CARD_COSTS, C_DISPLAY_NAME, C_DISPLAY_TEXT
from ECSO_Context import ECSO_Context
from Factories.Character_Factory import CharacterFactory
from GUI.BaseGUI import BaseGUI
from GUI.GUI import GUI
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Interactibles.Label import InteractibleLabel
from GUI.Interactibles.Slider import ProgressBar
from GUI.Level_GUI import LevelGUI
from GUI.Scene_GUI import SceneGUI
from Handlers import Input_Handler
from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Renderer import Renderer
from Renderer.Group_Types import SpriteGroupTypes
from Systems.Stacks.Hand import Hand

DEFAULT_CHARACTER_TYPE_ID = "GUI_CHARACTERS"
DEFAULT_STATUS_BAR_TYPE_ID = "GUI_STATUS_BAR"


class GUIFactory():
    def __init__(self, application, renderer, ecso_context: ECSO_Context, input_handler: InputHandler):
        self.application = application
        self.renderer = renderer
        self.ecso_context = ecso_context
        self.input_handler = input_handler

        self.card_callback_on_click = None
        self.card_callback_on_hover = None

    def generate_menu(self, pos_x: int, pos_y: int, button_pos_start: tuple[int, int], buttons: list[tuple[str, int, int, Any]]) -> int:
        """DONT USE IT!"""
        # buttons = [
        #     ("Endless", 200, 50, self.stop_game_mode)
        # ]
        # level = MenuLevel(self.ecso_context.next_object_id)
        # level.add_gui(self.factories["GUI"].generate_menu(710, 100, (150, 100), buttons))
        gui_entity = self.ecso_context.add_entity()
        gui = LevelGUI(gui_entity, pygame.Color(0, 0, 0), "MENU", 500, 700, pos_x, pos_y)

        button_index = 0
        for button in buttons:
            button_entity = self.ecso_context.add_entity()
            new_button = Button(button_entity, f"btn_menu_{button_entity}", gui.get_rect(), pygame.Color(10, 10, 10), pygame.Color(40, 40, 40), "", button[0], 11, button[1], button[2], button_pos_start[0], (button_pos_start[1] + 50 * button_index))
            new_button = Button(button_entity, f"btn_menu_{button_entity}", gui.rect, pygame.Color(10, 10, 10), pygame.Color(40, 40, 40), "", button[0], buttons[1], buttons[2], "")
            new_button.callback_on_click = buttons[3]
            subscription = InputSubscribtion(SubscriptionType.CURSOR, new_button.on_hover, new_button.get_rect(), [])
            self.input_handler.subscribe_to_event(subscription)
            gui.add_interactible(new_button)
        return gui_entity
    
    def generate_card_gui(self, level_id: int, play_stack_id: int, hand_stack_id: int):
        level = cast(Level, self.ecso_context.get_game_object(level_id, Level))

        color = pygame.Color(10, 10, 10)
        gui_entity = self.ecso_context.add_entity()
        gui_cards = LevelGUI(gui_entity, "GUI_CARDS", level.rect, "", color, 1240, 300)
        gui_cards.image.set_alpha(50)
        gui_cards.relative_x = (level.rect.x + level.rect.width / 2) - int(gui_cards.rect.width / 2)
        gui_cards.relative_y = (level.rect.x + level.rect.height) - gui_cards.rect.height
        self.ecso_context.add_game_object(gui_entity, gui_cards)
        self.renderer.add_sprite(SpriteGroupTypes.GUIS, gui_cards)
        level.add_gui(gui_entity)

        hand_stack = cast(Hand, self.ecso_context.get_game_object(hand_stack_id, Hand))

        self.draw_cards(gui_cards, hand_stack.get_cards())

        # x_offset = 215
        # index = 0
        # for entity_on_hand in hand_stack.get_cards():
        #     card_entity = self.ecso_context.add_entity()
        #     color = pygame.Color(80, 20, 60)
        #     card = Card(card_entity, entity_on_hand, "INTERACTIBLE_CARD_SPRITE", gui_cards.rect, "", color, 200, 300, "Levels/Data/card_background.png")  # It's possible to use an image as a base background!
        #     cost_resource = pygame.image.load("Levels/Data/card_cost_background.png")  # Background of the card costs area (Mana)
        #     try:
        #         # CARD PICTURE
        #         card.set_picture(pygame.image.load("Levels/Data/gangsta_tree.png"))
        #         # CARD TITLE
        #         card.set_title(cast(C_DISPLAY_NAME, self.ecso_context.get_component(entity_on_hand, C_DISPLAY_NAME)).value)
        #         # CARD COSTS
        #         card.set_cost(cast(C_CARD_COSTS, self.ecso_context.get_component(entity_on_hand, C_CARD_COSTS)).value, cost_resource)
        #         # CARD DESCRIBTION
        #         card.set_description(cast(C_DISPLAY_TEXT, self.ecso_context.get_component(entity_on_hand, C_DISPLAY_TEXT)).value)
        #     except Exception as e:
        #         print("FUCK!?", e)
        #     card.relative_x = 100 + (x_offset * index)
        #     card.relative_y = 20
        #     # card.animation_initial_y = card.rect.y  # TODO: Not a good  solution
        #     card.callback_on_click = card_callback_on_click
        #     self.ecso_context.add_game_object(card_entity, card)
        #     gui_cards.add_interactible(card_entity)

        #     subscribtion_entity = self.ecso_context.add_entity()
        #     subscribtion = InputSubscribtion(SubscriptionType.CURSOR, card, card.on_hover, card.rect)
        #     self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
        #     self.input_handler.subscribe_to_event(subscribtion)

        #     subscribtion_entity = self.ecso_context.add_entity()
        #     subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, card, card.on_click, card.rect, [], mouse_buttons=(True, False, False))
        #     self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
        #     self.input_handler.subscribe_to_event(subscription)
        #     index += 1

        # ### CARD PULL STACK ### # TODO: MOVE TO OWN DRAW METHOD
        color = pygame.Color(0, 0, 245)
        highlight = pygame.Color(0, 0, 255)
        entity = self.ecso_context.add_entity()
        pull_stack = Button(entity, "INTERACTIBLE_BUTTON_SPRITE", gui_cards.rect, color, highlight, "", "STACK", 50, 50, "Ressources/Pictures/pull_stack.png")
        pull_stack.relative_x = 25
        pull_stack.relative_y = (gui_cards.rect.height - pull_stack.rect.height) - 25
        pull_stack.set_text("STACK")
        pull_stack.font_size = 32
        self.ecso_context.add_game_object(entity, pull_stack)
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, pull_stack)
        gui_cards.add_interactible(entity)
        # ### END TURN BUTTON ### #
        # TODO: Implement Button wich represents the exhaustion stack
        # TODO: Implement Button wich calls a methond wich sets "self.move_running to false"

    def draw_cards(self, gui: GUI, cards: list[int]):
        gui.interactibles = []
        x_offset = 215
        index = 0
        for entity_on_hand in cards:
            card_entity = self.ecso_context.add_entity()
            color = pygame.Color(80, 20, 60)
            card = Card(card_entity, entity_on_hand, "INTERACTIBLE_CARD_SPRITE", gui.rect, "", color, 200, 300, "Ressources/Pictures/card_background.png")  # It's possible to use an image as a base background!
            try:
                # CARD PICTURE
                picture = pygame.image.load("Ressources/Pictures/gangsta_tree.png")
                picture.convert()
                picture.convert_alpha()
                card.set_picture(picture)
                # CARD TITLE
                card.set_title(cast(C_DISPLAY_NAME, self.ecso_context.get_component(entity_on_hand, C_DISPLAY_NAME)).value)
                # CARD COSTS
                cost_resource = pygame.image.load("Ressources/Pictures/card_cost_background.png")  # Background of the card costs area (Mana)
                cost_resource.convert()
                cost_resource.convert_alpha()
                card.set_cost(cast(C_CARD_COSTS, self.ecso_context.get_component(entity_on_hand, C_CARD_COSTS)).value, cost_resource)
                # CARD DESCRIBTION
                card.set_description(cast(C_DISPLAY_TEXT, self.ecso_context.get_component(entity_on_hand, C_DISPLAY_TEXT)).value)
            except Exception as e:
                print("FUCK!?", e)
            card.relative_x = 100 + (x_offset * index)
            card.relative_y = 20
            # card.animation_initial_y = card.rect.y  # TODO: Not a good  solution
            card.callback_on_hover = self.card_callback_on_hover
            card.callback_on_click = self.card_callback_on_click
            self.ecso_context.add_game_object(card_entity, card)
            self.renderer.add_sprite(SpriteGroupTypes.CARDS, card)
            gui.add_interactible(card_entity)

            subscribtion_entity = self.ecso_context.add_entity()
            subscribtion = InputSubscribtion(SubscriptionType.CURSOR, card, card.on_hover, card.rect)
            card.subscribtion_on_hover = subscribtion_entity
            self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
            self.input_handler.subscribe_to_event(subscribtion)

            subscribtion_entity = self.ecso_context.add_entity()
            subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, card, card.on_click, card.rect, [], mouse_buttons=(True, False, False))
            card.subscribtion_on_click = subscribtion_entity
            self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
            self.input_handler.subscribe_to_event(subscription)
            index += 1

    def redraw_cards(self, level_id: int, cards: list[int]):
        level = cast(Level, self.ecso_context.get_game_object(level_id, Level))
        card_gui = cast(LevelGUI, self.ecso_context.get_game_object(level.get_guis()[1], LevelGUI))

        try:
            for card_sprite_id in card_gui.get_interactibles():
                card_sprite = self.ecso_context.get_game_object(card_sprite_id, Card)
                if card_sprite is None:
                    card_sprite = self.ecso_context.get_game_object(card_sprite_id, Button)
                card_sprite.destroy = True
        except Exception as e:
            print("[GUIFACTORY][REDRAW] Found all card sprites", e)

        self.draw_cards(card_gui, cards)

    def generate_character_gui(self, level_id: int, player_character_id: int, enemy_character_id: int, round: int, character_callback_on_click: Any):
        level = cast(Level, self.ecso_context.get_game_object(level_id, Level))
        ressource_directory = "Ressources/Pictures"
        # ground_level = level.get_environment_type("FOREGROUND2")[0].rect.y  # ...

        color = pygame.Color(0, 0, 0)
        entity = self.ecso_context.add_entity()
        gui_characters = LevelGUI(entity, DEFAULT_CHARACTER_TYPE_ID, level.rect, "", color, 1440, 400)
        gui_characters.image.set_alpha(50)
        gui_characters.relative_x = 0
        gui_characters.relative_y = gui_characters.rect.height - 200
        self.ecso_context.add_game_object(entity, gui_characters)
        self.renderer.add_sprite(SpriteGroupTypes.GUIS, gui_characters)
        level.add_gui(entity)

        player_character_data = cast(Character, self.ecso_context.get_game_object(player_character_id, PlayerCharacter))
        if player_character_data is None:
            return

        # ### MAIN CHARACTER SPRITE ### #
        # BASE
        list_of_images = os.listdir(ressource_directory + "/Characters")
        base_color = pygame.Color(255, 255, 255)
        resource = ""
        for image_name in list_of_images:
            if image_name.split(".")[0] == player_character_data.get_name().lower():
                resource = image_name
        player_character_sprite_entity = self.ecso_context.add_entity()
        character_width = level.rect.height / 3
        charcter_height = level.rect.height / 3
        player_character_sprite = InteractibleCharacter(player_character_sprite_entity, player_character_id, "INTERACTIBLE_PLAYER_CHARACTER_SPRITE", gui_characters.rect, "", base_color, character_width, charcter_height, ressource_directory + "/Characters/" + resource)
        player_character_sprite.relative_x = 75
        player_character_sprite.relative_y = gui_characters.rect.height - player_character_sprite.rect.height
        player_character_sprite.callback_on_click = character_callback_on_click

        subscription_entity = self.ecso_context.add_entity()
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, player_character_sprite, player_character_sprite.on_click, player_character_sprite.rect, [], (True, False, False))
        player_character_sprite.subscribtion_on_click = subscription_entity
        self.ecso_context.add_game_object(subscription_entity, subscription)
        self.input_handler.subscribe_to_event(subscription)

        self.ecso_context.add_game_object(player_character_sprite_entity, player_character_sprite)
        self.renderer.add_sprite(SpriteGroupTypes.CHARACTERS, player_character_sprite)
        gui_characters.add_interactible(player_character_sprite_entity)
        player_character_data.set_sprite(player_character_sprite_entity)
        # ## SURROUNDING INDICATORS
        # PROGRESS BAR AS HEALTH TODO: 26.02.2025: Add everything to the dict and try categories of interactibles :)
        base_color = pygame.Color(50, 120, 90)
        value_color = pygame.Color(255, 0, 0)
        progressbar_entity = self.ecso_context.add_entity()
        progressbar = ProgressBar(progressbar_entity, "INTERACTIBLE_PLAYER_PROGRESSBAR_SPRITE", player_character_sprite.rect, "", base_color, value_color, player_character_sprite.rect.width, 20, player_character_data.get_health_max(), 0, "")
        progressbar.relative_x = 0
        progressbar.relative_y = -40

        self.ecso_context.add_game_object(progressbar_entity, progressbar)
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, progressbar)
        gui_characters.add_interactible(progressbar_entity)
        player_character_sprite.health_bar = progressbar_entity
        # SPRITE LIST AS EFFECT LIST
        # base_color = pygame.Color(50, 120, 90)
        # sprite_list = SpriteList(len(gui_characters.interactibles) - 1, "PLAYER_EFFECTS", "SPRITELIST", base_color, player_character_sprite.rect.width, 50)
        # sprite_list.rect.x = player_character_sprite.rect.x
        # sprite_list.rect.y = player_character_sprite.rect.y - player_character_sprite.rect.height - 70
        # player_character_data.on_effect_added = sprite_list.add_sprite
        # gui_characters.add_interactible(sprite_list)
        # ### MAIN PLAYER SPRITE ### #

        # TODO: TEST self.active_enemy_character = cast(CharacterFactory, self.factories["CHARACTERS"]).fabricate_enemy()
        if round % 10 == 0:
            enemy_character_data = cast(StandardEnemy, self.ecso_context.get_game_object(enemy_character_id, BossEnemy))
        else:
            enemy_character_data = cast(StandardEnemy, self.ecso_context.get_game_object(enemy_character_id, StandardEnemy))

        if enemy_character_data is None:
            return

        # ### MAIN ENEMY SPRITE ### #
        base_color = pygame.Color(255, 255, 255)
        if round % 10 == 0:
            ressources = os.listdir(ressource_directory + "/Dragons")
            resource = ressource_directory + "/Dragons/" + ressources[randint(0, len(ressources) - 1)]
        else:
            ressources = os.listdir(ressource_directory + "/Enemies")
            resource = ressource_directory + "/Enemies/" + ressources[randint(0, len(ressources) - 1)]
        enemy_character_sprite_entity = self.ecso_context.add_entity()
        character_width = level.rect.height / 3
        charcter_height = level.rect.height / 3
        enemy_character_sprite = InteractibleCharacter(enemy_character_sprite_entity, enemy_character_id, "INTERACTIBLE_ENEMY_CHARACTER_SPRITE", gui_characters.rect, "", base_color, character_width, charcter_height, resource)
        enemy_character_sprite.callback_on_click = character_callback_on_click
        enemy_character_sprite.relative_x = gui_characters.rect.width - character_width - 75
        enemy_character_sprite.relative_y = gui_characters.rect.height - enemy_character_sprite.rect.height

        subscription_entity = self.ecso_context.add_entity()
        subscription = InputSubscribtion(SubscriptionType.MOUSEBUTTON, enemy_character_sprite, enemy_character_sprite.on_click, enemy_character_sprite.rect, [], (True, False, False))
        enemy_character_sprite.subscribtion_on_click = subscription_entity
        self.ecso_context.add_game_object(subscription_entity, subscription)
        self.renderer.add_sprite(SpriteGroupTypes.CHARACTERS, enemy_character_sprite)
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

        self.ecso_context.add_game_object(progressbar_entity, progressbar)
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, progressbar)
        gui_characters.add_interactible(progressbar)
        enemy_character_sprite.health_bar = progressbar_entity

        # ### SICKK ### #
        # BIOLERPLATE!
        # EFFECT SPRITE FOR THE PLAYER
        selection_effect_player = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_GUI_CHARACTERS_SELECTION_EFFECT", gui_characters.rect, "", (0, 255, 0), 25, charcter_height, image_path="Ressources/Pictures/selection_highlight_v2.png")
        selection_effect_player.image.set_colorkey((255, 255, 255))
        selection_effect_player.image.set_alpha(150)
        selection_effect_player.is_visible = False
        selection_effect_player.relative_x = player_character_sprite.relative_x - 50
        selection_effect_player.relative_y = player_character_sprite.relative_y
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, selection_effect_player)
        self.ecso_context.add_game_object(selection_effect_player.context_id, selection_effect_player)
        gui_characters.add_interactible(selection_effect_player.context_id)

        # EFFECT SPRITE FOR THE ENEMY
        selection_effect_enemy = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_GUI_CHARACTERS_SELECTION_EFFECT", gui_characters.rect, "", (0, 255, 0), 25, charcter_height, image_path="Ressources/Pictures/selection_highlight_v2.png")
        selection_effect_enemy.image.set_colorkey((255, 255, 255))
        selection_effect_enemy.image.set_alpha(150)
        selection_effect_enemy.is_visible = False
        selection_effect_enemy.relative_x = enemy_character_sprite.relative_x + character_width + 25
        selection_effect_enemy.relative_y = enemy_character_sprite.relative_y
        self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, selection_effect_enemy)
        self.ecso_context.add_game_object(selection_effect_enemy.context_id, selection_effect_enemy)
        gui_characters.add_interactible(selection_effect_enemy.context_id)

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

    def update_character_selection_effect(self, desired_state: bool):
        """Sets the is_visible flag positive or negative
            The selection effect is currently an InteractibleLabel"""
        try:
            gui_entity = None
            gui_object = None
            for gui_items in self.check_for__guis(LevelGUI):
                if gui_items[1].type_id is DEFAULT_CHARACTER_TYPE_ID:
                    gui_entity = gui_items[0]
                    gui_object = gui_items[1]

            for interactible_entity in gui_object.get_interactibles():
                try:
                    label = cast(InteractibleLabel, self.ecso_context.get_game_object(interactible_entity, InteractibleLabel))
                    if label.type_id == "INTERACTIBLE_GUI_CHARACTERS_SELECTION_EFFECT":
                        label.is_visible = desired_state
                except AttributeError:
                    continue
        except TypeError as e:
            print("[GUIFactory][SELECTIONEFFECT]", e)

    def generate_status_bar(self, scene, player_character_id=-1, enemy_character_id=-1, round=-1) -> int:
        try:
            if scene is None:
                return -1
            entity = self.ecso_context.add_entity()
            window_rect = self.application.get_window().get_rect()
            height_percentage = 0.08
            status_bar = SceneGUI(entity, DEFAULT_STATUS_BAR_TYPE_ID, window_rect, "", (0, 0, 0), window_rect.width, window_rect.height * height_percentage, "Ressources/Pictures/gui.jpg")
            status_bar.relative_x = 0
            status_bar.relative_y = 0
            self.ecso_context.add_game_object(entity, status_bar)
            self.renderer.add_sprite(SpriteGroupTypes.GUIS, status_bar)
            # NOTE: THE LEVEL DOES NOT RECIEVE THE SCENE GUI ID!

            # From left to right
            label_developer = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_DEVELOPER", status_bar.rect, "", (255, 255, 0), 100, status_bar.rect.height, "MeJa", (255, 255, 255), "Ressources/Pictures/gui.jpg")
            label_developer.relative_x = 20
            label_developer.font_size = 20
            self.ecso_context.add_game_object(label_developer.context_id, label_developer)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_developer)
            status_bar.add_interactible(label_developer.context_id)

            label_enemy_name = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_ENEMY_NAME", status_bar.rect, "", (255, 255, 0), 100, status_bar.rect.height, "TESTIGER TEST", (255, 255, 255), "Ressources/Pictures/gui.jpg")
            label_enemy_name.relative_x = 140
            label_enemy_name.font_size = 20
            self.ecso_context.add_game_object(label_enemy_name.context_id, label_enemy_name)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_enemy_name)
            status_bar.add_interactible(label_enemy_name.context_id)

            player = cast(PlayerCharacter, self.ecso_context.get_game_object(scene.active_player_character, PlayerCharacter))
            label_player_health = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_PLAYER_HEALTH", status_bar.rect, "", (255, 255, 0), 100, status_bar.rect.height, str(player.get_health_max()) + "/" + str(player.get_health()), (255, 0, 0), "Ressources/Pictures/gui.jpg")
            label_player_health.relative_x = 260
            label_player_health.font_size = 20
            self.ecso_context.add_game_object(label_player_health.context_id, label_player_health)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_player_health)
            status_bar.add_interactible(label_player_health.context_id)

            label_player_currency = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_PLAYER_CURRENCY", status_bar.rect, "", (255, 255, 0), 100, status_bar.rect.height, str(player.get_gold()), (255, 255, 255), "Ressources/Pictures/gui.jpg")
            label_player_currency.relative_x = 380
            label_player_currency.font_size = 20
            self.ecso_context.add_game_object(label_player_currency.context_id, label_player_currency)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_player_currency)
            status_bar.add_interactible(label_player_currency.context_id)

            label_current_level = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_CURRENT_ROUND", status_bar.rect, "", (255, 255, 0), 100, status_bar.rect.height, "ROUND: " + str(scene.current_round), (255, 255, 255), "Ressources/Pictures/gui.jpg")
            label_current_level.relative_x = 500
            label_current_level.font_size = 20
            self.ecso_context.add_game_object(label_current_level.context_id, label_current_level)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_current_level)
            status_bar.add_interactible(label_current_level.context_id)

            label_player_deck = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_PLAYER_DECK", status_bar.rect, "", (255, 255, 0), status_bar.rect.height, status_bar.rect.height, "DECK", (255, 255, 255), "Ressources/Pictures/gui.jpg")
            label_player_deck.relative_x = window_rect.width - 160
            label_player_deck.font_size = 20
            self.ecso_context.add_game_object(label_player_deck.context_id, label_player_deck)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_player_deck)
            status_bar.add_interactible(label_player_deck.context_id)

            label_settings = InteractibleLabel(self.ecso_context.add_entity(), "INTERACTIBLE_STATUS_BAR_SETTINGS", status_bar.rect, "", (100, 100, 100), status_bar.rect.height, status_bar.rect.height, "COG", (255, 255, 255), "Ressources/Pictures/gui.jpg")
            label_settings.relative_x = window_rect.width - 70
            label_settings.font_size = 20
            label_settings.callback_on_click = scene.callback_level_end
            subscribtion_entity = self.ecso_context.add_entity()
            subscribtion = InputSubscribtion(SubscriptionType.MOUSEBUTTON, label_settings, label_settings.on_click, label_settings.rect, [], (True, False, False))
            self.input_handler.subscribe_to_event(subscribtion)
            label_settings.subscribtion_on_click = subscribtion_entity
            self.ecso_context.add_game_object(subscribtion_entity, subscribtion)
            self.ecso_context.add_game_object(label_settings.context_id, label_settings)
            self.renderer.add_sprite(SpriteGroupTypes.INTERACTIBLES, label_settings)
            status_bar.add_interactible(label_settings.context_id)
            
        except AttributeError as e:
            print("[GUIFactory]", e)

    def update_status_bar(self, scene: Any):
        try:
            gui_entity = None
            gui_object = None
            for gui_items in self.check_for__guis(SceneGUI):
                if gui_items[1].type_id is DEFAULT_STATUS_BAR_TYPE_ID:
                    gui_entity = gui_items[0]
                    gui_object = gui_items[1]

            for interactible_entity in gui_object.get_interactibles():
                interactible = cast(InteractibleLabel, self.ecso_context.get_game_object(interactible_entity, InteractibleLabel))
                match interactible.type_id:
                    case "INTERACTIBLE_STATUS_BAR_DEVELOPER":
                        interactible.font_size = 32
                        interactible.set_text("MEJA")
                    case "INTERACTIBLE_STATUS_BAR_ENEMY_NAME":
                        if scene.current_round % 10 == 0:
                            enenmy = cast(BossEnemy, self.ecso_context.get_game_object(scene.active_enemy_character, BossEnemy))
                        else:
                            enenmy = cast(StandardEnemy, self.ecso_context.get_game_object(scene.active_enemy_character, StandardEnemy))
                        if enenmy is not None:
                            interactible.set_text(enenmy.get_name())
                    case "INTERACTIBLE_STATUS_BAR_PLAYER_HEALTH":
                        player = cast(PlayerCharacter, self.ecso_context.get_game_object(scene.active_player_character, PlayerCharacter))
                        if player is not None:
                            styled_health = str(player.get_health()) + "/" + str(player.get_health_max())
                            interactible.font_size = 24
                            interactible.set_text(styled_health)
                    case "INTERACTIBLE_STATUS_BAR_PLAYER_CURRENCY":
                        player = cast(PlayerCharacter, self.ecso_context.get_game_object(scene.active_player_character, PlayerCharacter))
                        if player is not None:
                            interactible.color_text = (255, 255, 0)
                            interactible.font_size = 24
                            styled_currency = "GOLD: " + str(player.get_gold())
                            interactible.set_text(styled_currency)
                    case "INTERACTIBLE_STATUS_BAR_CURRENT_ROUND":
                        styled_round = "LEVEL: " + str(scene.current_round)
                        interactible.font_size = 24
                        interactible.set_text(styled_round)
                    case "INTERACTIBLE_STATUS_BAR_PLAYER_DECK":
                        continue
        except Exception:
            pass

    def destroy_scene_guis(self):
        try:
            for gui_items in self.check_for__guis(SceneGUI):
                gui_items[1].destroy = True
        except KeyError:
            print("[GUIFactory]", e)

    def check_for__guis(self, type: Any) -> set[int, Any]:
        """Persistent GUIs wont get deleted during a level change.
        It is possible to find them.

        Returns:
            set[int, GUISprite]: Entity with its gameobject
        """
        result = self.ecso_context.get_game_objects_of_type(type)
        return result

    def get_gui_by_type_id(self, type_id: str, gui_set: set[dict[int, Any]]) -> Any:
        try:
            for gui_items in gui_set:
                if gui_items[1].type_id == type_id:
                    return gui_items[1]
            return None
        except KeyError:
            return None
