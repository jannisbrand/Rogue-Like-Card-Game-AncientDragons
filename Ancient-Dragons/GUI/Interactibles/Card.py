from email.mime import image
from typing import Any
import pygame
from GUI.Interactibles.Base import InteractibleSprite
from Sprites.Base import Sprite


class Card(InteractibleSprite):
    def __init__(self, context_id, type_id: str, reference_rect, name: str, color: pygame.Color, width: int, height: int, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        self.rect.x = self.reference_rect.x
        self.rect.y = self.reference_rect.y
        
        self.cost_area = None
        self.title = None
        self.picture = None
        self.description = None

        self.base_font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 18)

        # ### Animation ### #
        self.should_animate = False
        self.animation_increment_y = 10
        self.animation_range_max_y = 50
        self.animation_range_min_y = 50
        self.animation_initial_y = self.relative_y


    def set_cost(self, value: int, resource: pygame.Surface) -> None:
        square_measure = self.rect.width * 0.25
        if resource is None:
            background = pygame.Surface((square_measure, square_measure))  # ~25% smaller than the card
            background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        else:
            background = pygame.transform.scale(resource, (square_measure, square_measure))
        if value <= 0:
            text = "00"
        else:
            text = str(value)
        text_color = pygame.Color(180, 180, 180)
        cost_text = self.base_font.render(text, True, text_color)
        background.blit(cost_text, (0, 0))  # Placed centered
        self.cost_area = background
        self.image.blit(background, (0, 0))

    def set_title(self, value: str) -> None:
        background = pygame.Surface((self.rect.width * 0.90, self.rect.height * 0.10))
        background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        if value == "":
            text = "(O_o)"
        else:
            text = value
        text_color = pygame.Color(180, 180, 180)
        title_text = self.base_font.render(text, True, text_color)
        background.blit(title_text, (0, 0))
        self.title = background
        self.image.blit(background, (self.rect.width / 2 - background.get_rect().width / 2, self.rect.y + self.rect.height * 0.50))

    def set_picture(self, picture: pygame.Surface) -> None:
        background = pygame.Surface((self.rect.width * 0.35, self.rect.height * 0.35))
        background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        background.blit(picture, (0, 0))
        self.picture = background
        self.image.blit(background)

    def set_description(self, value: str) -> None:
        background = pygame.Surface((self.rect.width * 0.25, self.rect.height * 0.25))  # ~25% smaller than the card
        background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        if value <= 0:
            text = "- - -"
        else:
            text = str(value)
        text_color = pygame.Color(10, 10, 10)
        cost_text = self.base_font.render(text, True, text_color)
        background.blit(cost_text, (0, 0))  # Placed centered
        self.description = background
        self.image.blit(background, (0, 0))

    def animation(self) -> None:
        if self.should_animate:
            if self.relative_y > self.animation_initial_y - self.animation_range_max_y:
                self.relative_y -= self.animation_increment_y
        else:
            # print(self.rect.y + self.animation_increment_y)
            if self.relative_y < self.animation_initial_y:
                self.relative_y += self.animation_increment_y

    def update(self) -> None:
        self.animation()
        self.should_animate = False
        self.relative_positioning()

    def on_hover(self, source: Any, cursor: tuple[int]) -> None:
        try:
            self.should_animate = True
            if self.callback_on_hover is not None:
                self.callback_on_hover(source, cursor)
        except AttributeError as e:
            print("Callback is not callable or registered: ", e)

    def on_click(self, source: Any, mouse_buttons: tuple[bool]) -> None:
        try:
            if self.callback_on_click is not None:
                self.callback_on_click(source, mouse_buttons)
        except AttributeError as e:
            print("Callback is not callable or registered: ", e)
