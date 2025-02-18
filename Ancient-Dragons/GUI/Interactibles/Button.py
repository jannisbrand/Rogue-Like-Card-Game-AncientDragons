from email.mime import image
from typing import Any
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, id: int,  gui_rect: Any, normal_color: pygame.Color, highlight_color: pygame.Color = None, name: str = "DEFAULT_BUTTON", text: str = "DEFAULT_BUTTON", font_size: int = 11, width: int = 10, height: int = 10, pos_x: int = 0, pos_y: int = 0):
        super().__init__()
        self.normal_color = normal_color
        self.hightlight_color = highlight_color

        self.image = pygame.Surface((width, height))
        self.image.fill(normal_color)
        self.rect = self.image.get_rect()

        self.parent_rect = gui_rect

        # ### RELATIVE POSITIONING ### #
        self.rect.x = gui_rect.x + pos_x
        self.rect.y = gui_rect.y + pos_y

        font_text = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", font_size)
        surface_text = font_text.render(text, True, (255, 255, 255))
        text_x = self.rect.x + int((surface_text.get_width() / 2))
        text_y = self.rect.y + int((surface_text.get_height() / 2))
        self.image.blit(surface_text, (self.rect.x, self.rect.y))

        self.text: text
        self.is_active = False
        self.is_hovered_over = False

    def get_rect(self) -> pygame.Rect:
        return self.rect
    
    def set_text(self, text: str = "DEFAULT_BUTTON", font_size: int = 11) -> None:
        font_text = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", font_size)
        surface_text = font_text.render(text, True, (255, 255, 255))
        text_x = self.rect.x + int((surface_text.get_width() / 2))
        text_y = self.rect.y + int((surface_text.get_height() / 2))
        self.image.blit(surface_text, (self.rect.x, self.rect.y))

    def update(self) -> None:
        if self.is_hovered_over and self.hightlight_color:
            self.image.fill(self.hightlight_color)
            self.is_hovered_over = False
        else:
            self.image.fill(self.normal_color)
        pass

    def on_hover(self, keys: list):
        self.is_hovered_over = True