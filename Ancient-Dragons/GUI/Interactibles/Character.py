

from typing import Any

import pygame
from Sprites.Base import Sprite


class InteractibleCharacter(Sprite):
    def __init__(self, context_id: int, type_id: str, name: str, color: pygame.Color, width: int, height: int, image_path=""):
        super().__init__(context_id, type_id, name, color, width, height, image_path)
        self.display_name = name
        self.show_name = False

    def set_display_name(self, value: str):
        self.display_name = value

    def on_hover(self, source: Any, cursor: tuple[int]) -> None:
        try:
            self.is_hovered_over = True
            if self.callback_on_hover is not None:
                self.callback_on_hover(source, cursor)
        except AttributeError as e:
            print("Callback not callable or not registered: ", e)

    def on_click(self, source: Any, mouse_buttons: tuple[bool]) -> None:
        try:
            # Does noting with it self atm
            if self.callback_on_click is not None:
                self.callback_on_click(source, mouse_buttons)
        except AttributeError as e:
            print("Callback not callable or not registered: ", e)

    def update(self) -> None:
        self.is_hovered_over = False
