from typing import Any, cast
import pygame
from Components.Components import C_CARD_COSTS, C_DISPLAY_NAME, C_DISPLAY_TEXT
from ECSO_Context import ECSO_Context
from GUI.GUI import GUI
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from Handlers import Input_Handler
from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Renderer import Renderer
from Systems.Stacks.Hand import Hand


class GUIFactory():
    def __init__(self, ecso_context: ECSO_Context, input_handler: InputHandler):
        self.ecso_context = ecso_context
        self.input_handler = input_handler

    def generate_menu(self, pos_x: int, pos_y: int, button_pos_start: tuple[int, int], buttons: list[tuple[str, int, int, Any]]) -> int:
        """DONT USE IT!"""
        # buttons = [
        #     ("Endless", 200, 50, self.stop_game_mode)
        # ]
        # level = MenuLevel(self.ecso_context.next_object_id)
        # level.add_gui(self.factories["GUI"].generate_menu(710, 100, (150, 100), buttons))
        gui_entity = self.ecso_context.add_entity()
        gui = GUI(gui_entity, pygame.Color(0, 0, 0), "MENU", 500, 700, pos_x, pos_y)

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
    
    def generate_card_gui(self, level_id: int, play_stack_id: int, hand_stack_id: int, card_callback_on_click: Any):
        level = cast(Level, self.ecso_context.get_game_object(level_id, Level))

        color = pygame.Color(10, 10, 10)
        gui_entity = self.ecso_context.add_entity()
        gui_cards = GUI(gui_entity, "GUI_CARDS", level.rect, "", color, 1240, 300)
        gui_cards.image.set_alpha(50)
        gui_cards.relative_x = (level.rect.x + level.rect.width / 2) - int(gui_cards.rect.width / 2)
        gui_cards.relative_y = (level.rect.x + level.rect.height) - gui_cards.rect.height
        self.ecso_context.add_game_object(gui_entity, gui_cards)
        level.add_gui(gui_entity)

        hand_stack = cast(Hand, self.ecso_context.get_game_object(hand_stack_id, Hand))

        x_offset = 215
        index = 0
        for entity_on_hand in hand_stack.get_cards():
            card_entity = self.ecso_context.add_entity()
            color = pygame.Color(80, 20, 60)
            card = Card(card_entity, entity_on_hand, "INTERACTIBLE_CARD_SPRITE", gui_cards.rect, "", color, 200, 300, "Levels/Data/card_background.png")  # It's possible to use an image as a base background!
            cost_resource = pygame.image.load("Levels/Data/card_cost_background.png")  # Background of the card costs area (Mana)
            try:
                # CARD PICTURE
                card.set_picture(pygame.image.load("Levels/Data/gangsta_tree.png"))
                # CARD TITLE
                card.set_title(cast(C_DISPLAY_NAME, self.ecso_context.get_component(entity_on_hand, C_DISPLAY_NAME)).value)
                # CARD COSTS
                card.set_cost(cast(C_CARD_COSTS, self.ecso_context.get_component(entity_on_hand, C_CARD_COSTS)).value, cost_resource)
                # CARD DESCRIBTION
                card.set_description(cast(C_DISPLAY_TEXT, self.ecso_context.get_component(entity_on_hand, C_DISPLAY_TEXT)).value)
            except Exception as e:
                print("FUCK!?", e)
            card.relative_x = 100 + (x_offset * index)
            card.relative_y = 20
            # card.animation_initial_y = card.rect.y  # TODO: Not a good  solution
            card.callback_on_click = card_callback_on_click
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
        pull_stack = Button(entity, "INTERACTIBLE_BUTTON_SPRITE", gui_cards.rect, color, highlight, "", "STACK", 50, 50, "Levels/Data/pull_stack.png")
        pull_stack.relative_x = 25
        pull_stack.relative_y = (gui_cards.rect.height - pull_stack.rect.height) - 25
        pull_stack.set_text("STACK")
        pull_stack.font_size = 32
        self.ecso_context.add_game_object(entity, pull_stack)
        gui_cards.add_interactible(entity)

        # ### END TURN BUTTON ### #
        # TODO: Implement Button wich represents the exhaustion stack
        # TODO: Implement Button wich calls a methond wich sets "self.move_running to false"
