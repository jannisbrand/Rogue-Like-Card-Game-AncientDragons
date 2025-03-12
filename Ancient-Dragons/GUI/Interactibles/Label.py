from ctypes import ArgumentError
from typing import Any, cast
import pygame
from GUI.Interactibles.Base import InteractibleSprite


class InteractibleLabel(InteractibleSprite):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, text="", color_text=(255, 255, 255), image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        self.text = text
        self.color_text = color_text
        self.font_size = 11  # Standard size
        self.text_changed = True

        self.enabled = True

    def apply_text(self):
        try:
            font = pygame.font.Font("Ressources/Fonts/Agency_Gothic_CT.otf", self.font_size)
            surface_text = font.render(self.text, True, self.color_text)
            middle_x = (self.rect.width / 2) - (surface_text.get_rect().width / 2)
            middle_y = (self.rect.height / 2) - (surface_text.get_rect().height / 2)
            cast(pygame.Surface, self.image).blit(surface_text, (middle_x, middle_y))
        except AttributeError as e:
            print("[INTERACTIBLE][LABEL]", e)

    def set_text(self, value: str):
        self.text = value
    
    def on_hover(self, source: Any, cursor: tuple[int]):
        if self.enabled:
            self.is_hovered_over = True
        try:
            if self.callback_on_hover is not None:
                self.callback_on_hover(source)
        except Exception as e:
            print(f"[Button] No on_hover callback is registered: {e}")

    def on_click(self, source: Any, mouse_buttons: tuple[bool]):
        try:
            if self.callback_on_click is not None:
                self.callback_on_click(source, mouse_buttons)
        except ArgumentError as e:
            print(f"[Button] No on_click callback is registered: {e}", self.callback_on_click)

    def update(self):
        if self.text_changed:
            self.apply_text()
            self.text_changed = False

        self.relative_positioning()
