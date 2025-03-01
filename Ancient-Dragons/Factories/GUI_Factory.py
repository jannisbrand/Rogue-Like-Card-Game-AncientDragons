from typing import Any
import pygame
from ECSO_Context import ECSO_Context
from GUI.Base import GUI
from GUI.Interactibles.Button import Button
from Handlers import Input_Handler
from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Renderer import Renderer


class GUIFactory():
    def __init__(self, ecso_context: ECSO_Context, event_handler: InputHandler):
        self.ecso_context = ecso_context
        self.input_handler = event_handler

    def generate_menu(self, pos_x: int, pos_y: int, button_pos_start: tuple[int, int], buttons: list[tuple[str, int, int, Any]]) -> int:
        gui_entity = self.ecso_context.add_entity()
        gui = GUI(gui_entity, pygame.Color(0, 0, 0), "MENU", 500, 700, pos_x, pos_y)

        button_index = 0
        for button in buttons:
            button_entity = self.ecso_context.add_entity()
            new_button = Button(button_entity, f"btn_menu_{button_entity}", gui.get_rect(), pygame.Color(10, 10, 10), pygame.Color(40, 40, 40), "", button[0], 11, button[1], button[2], button_pos_start[0], (button_pos_start[1] + 50 * button_index))
            subscription = InputSubscribtion(SubscriptionType.CURSOR, new_button.on_hover, new_button.get_rect(), [])
            self.input_handler.subscribe_to_event(subscription)
            gui.add_interactible(new_button)
        return gui_entity
