from email.mime import image
from typing import Any
import pygame
from GUI.Interactibles.Base import InteractibleSprite
from Sprites.Base import Sprite


class Card(InteractibleSprite):
    def __init__(self, context_id, card_context_id, type_id: str, reference_rect, name: str, color: pygame.Color, width: int, height: int, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        self.card_context_id = card_context_id
        self.rect.x = self.reference_rect.x
        self.rect.y = self.reference_rect.y
        
        self.cost_area = None
        self.title = None
        self.picture = None
        self.description = None

        self.base_font = pygame.font.Font("Ressources/Fonts/Agency_Gothic_CT.otf", 18)
        self.cost_font = pygame.font.Font("Ressources/Fonts/Agency_Gothic_CT.otf", 26)
        self.describtion_font = pygame.font.Font("Ressources/Fonts/Agency_Gothic_CT.otf", 18)

        # ### Animation ### #
        self.should_animate = False
        self.animation_increment_y = 10
        self.animation_range_max_y = 50
        self.animation_range_min_y = 50
        self.animation_initial_y = self.relative_y

        self.is_selected = False

    def set_cost(self, value: int, picture: pygame.Surface) -> None:
        square_measure = self.rect.width * 0.25
        background = pygame.Surface((square_measure, square_measure))  # ~25% smaller than the card
        if picture is None:
            background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        else:
            background = pygame.transform.scale(picture, (square_measure, square_measure))

        if value <= 0:
            text = "00"
        else:
            text = str(value)

        text_color = pygame.Color(255, 255, 0)
        cost_text = self.cost_font.render(text, True, text_color)

        middle_x = background.get_rect().width / 2 - cost_text.get_rect().width / 2
        middle_y = background.get_rect().height / 2 - cost_text.get_rect().height / 2

        background.blit(cost_text, (middle_x, middle_y))  # Placed centered
        self.cost_area = background
        self.image.blit(background, (0, 0))

    def set_title(self, value: str) -> None:
        background = pygame.Surface((self.rect.width * 0.90, self.rect.height * 0.10))
        background.fill((100, 240, 250))

        if value == "":
            text = "(O_o)"
        else:
            text = value

        text_color = pygame.Color(50, 50, 50)
        title_text = self.base_font.render(text, True, text_color)
        middle_x = background.get_rect().width / 2 - title_text.get_rect().width / 2
        middle_y = background.get_rect().height / 2 - title_text.get_rect().height / 2
        background.blit(title_text, (middle_x, middle_y))

        self.title = background
        self.image.blit(background, (self.rect.width / 2 - background.get_rect().width / 2, self.rect.y + self.rect.height / 10))

    def set_picture(self, picture: pygame.Surface) -> None:
        background = pygame.Surface((self.rect.width * 0.35, self.rect.height * 0.35))
        background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        background.blit(picture, (0, 0))
        self.picture = background

        picture = pygame.transform.scale(picture, (self.rect.width * 0.75, self.rect.width * 0.75))
        middle_x = self.rect.width / 2 - picture.get_rect().width / 2
        pos_y = int(self.rect.height / 12)

        self.picture = picture
        self.image.blit(picture, (middle_x, pos_y))

    def set_description(self, value: str) -> None:
        background = pygame.Surface((self.rect.width * 0.25, self.rect.height * 0.25))  # ~25% smaller than the card
        background.fill((int(self.color.r * 0.80), int(self.color.g * 0.80), int(self.color.b * 0.80)))
        if value == "":
            text = "- - -"
        else:
            text = str(value)

        text_color = pygame.Color(220, 220, 220)
        text = text.split(" ")

        font_size = 18
        word_spacing = 5
        line_spacing = 5
        line_pos_y = (self.rect.width / 1.0016)
        card_middle_x = self.rect.width / 2
        line_width_max = 150
        line_width = 0
        chars_in_line = 0
        lines = 0
        for word in text:
            chars_in_line += len(word)
            if chars_in_line >= 20:
                chars_in_line = 0
                line_pos_y += font_size + line_spacing
                line_width = 0
                lines += 1
            surface_word = self.describtion_font.render(word, True, text_color)
            pos_x = (card_middle_x - line_width_max / 2) + line_width
            self.image.blit(surface_word, (pos_x, line_pos_y))
            line_width += surface_word.get_rect().width + word_spacing

    def animation(self) -> None:
        if self.should_animate or self.is_selected:
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
            self.is_selected = True
            if self.callback_on_click is not None:
                self.callback_on_click(source, mouse_buttons)
        except AttributeError as e:
            print("Callback is not callable or registered: ", e)
