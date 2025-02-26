

from typing import Any

import pygame
from Sprites.Base import Sprite


class InteractibleCharacter(Sprite):
    def __init__(self, id: int, type: str, name: str, color: pygame.Color, width: int, height: int, image_path = ""):
        super().__init__(id, type, name, color, width, height, image_path)
        self.display_name = ""
        self.health = 0  # TODO: Make a slider interactible
        # TODO: MOVE TO ONW: self.active_effects: list[Sprite] = []  # Icons representing the effects/buffs/debuffs with its value in a corner

        self.show_name = False
        
        self.on_health_changed = None

    def set_display_name(self, name: str) -> None:
        self.display_name = name

    def set_health(self, value: int) -> None:
        self.health = value
        if self.on_health_changed is not None:
            self.on_health_changed(value)

    def on_hover(self, source: Any, cursor: tuple[int]) -> None:
        try:
            self.callback_on_hover(source, cursor)
        except AttributeError as e:
            print("Callback not callable or not registered: ", e)

    def on_click(self, source: Any, mouse_buttons: tuple[bool]) -> None:
        try:
            self.callback_on_click(source, mouse_buttons)
        except AttributeError as e:
            print("Callback not callable or not registered: ", e)

    def update(self) -> None:
        pass
