from ctypes import ArgumentError
from email.mime import image
from sre_constants import ANY
from typing import Any
import pygame

from Handlers.Flags import SubscriptionType
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion


class Button(pygame.sprite.Sprite):
    def __init__(self, gui_rect: Any, normal_color: pygame.Color, highlight_color: pygame.Color = None, name: str = "DEFAULT_BUTTON", text: str = "DEFAULT_BUTTON", font_size: int = 11, width: int = 10, height: int = 10, pos_x: int = 0, pos_y: int = 0):
        super().__init__()
        self.name = name
        self.normal_color = normal_color
        self.hightlight_color = highlight_color

        self.image = pygame.Surface((width, height))
        #self.image.fill(normal_color)
        self.rect = self.image.get_rect()

        self.parent_rect = gui_rect

        # ### RELATIVE POSITIONING ### #
        self.rect.x = gui_rect.x + pos_x
        self.rect.y = gui_rect.y + pos_y

        self.font_text = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", font_size)
        self.set_text(text, font_size)
        # ### RELATIVE POSITIONING ### #

        # ### CALLBACKS ### #
        # Public
        self.callback_on_click = None
        self.callback_on_hover = None

        self.subscription_on_click = InputSubscribtion(SubscriptionType.MOUSEBUTTON, self, self.callback_on_click, self.rect, mouse_buttons=(True, False, False))
        self.subscription_on_hover = InputSubscribtion(SubscriptionType.CURSOR, self, self.on_hover, self.rect)
        self.text = text
        self.enabled = True
        self.is_hovered_over = False

    def get_name(self) -> str:
        return self.name

    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def set_text(self, text: str = "DEFAULT_BUTTON", font_size: int = 8) -> None:
        self.text = text
        surface_text = self.font_text.render(text, True, (255, 255, 255))
        rect_text = surface_text.get_rect()
        text_x = (self.image.get_width() - surface_text.get_width()) // 2
        text_y = (self.image.get_height() - surface_text.get_height()) // 2
        self.image.blit(surface_text, (text_x, text_y))

    def update(self) -> None:
        try:
            if self.is_hovered_over and self.hightlight_color:
                self.image.fill(self.hightlight_color)
                self.is_hovered_over = False
            else:
                self.image.fill(self.normal_color)
            
            self.set_text(self.text)
        except AttributeError as e:
            print(f"[BUTTON] No attribute: {e}")

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

