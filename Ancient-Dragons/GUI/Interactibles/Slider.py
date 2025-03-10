from pygame import Color, Surface
import pygame
from GUI.Interactibles.Base import InteractibleSprite
from Sprites.Base import Sprite


class ProgressBar(InteractibleSprite):
    def __init__(self, context_id, type_id, reference_rect, name, color, value_color: Color, width, height, max_value: int, min_value: int, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        self.max_value = max_value
        self.min_value = min_value
        self.total_range = min_value + max_value
        self.current_value = max_value  # Initial state is 100%
        self.fragmentation = 10
        self.fragment_width = int(self.total_range / 10)
        self.value_color = value_color

        self.base_font = pygame.font.Font("Ressources/Fonts/Agency_Gothic_CT.otf", height - 2)

        self.offset_x = int((self.min_value + self.max_value) / 10)

    def generate_slider(self) -> None:
        background = Surface((self.rect.width, self.rect.height))
        background.fill(pygame.Color(20, 20, 20))

        try:
            value_part = self.current_value / self.max_value
            value_width = self.rect.width * value_part
            value_surface = Surface((value_width, self.rect.height))
            value_surface.fill(self.value_color)
            self.image.blit(value_surface, (0, 0))
        except ZeroDivisionError:
            pass
        self.generate_text()

    def decrement(self, amount: int = 1) -> None:
        if self.current_value - amount >= self.min_value:
            self.current_value -= amount

    def increment(self, amount: int = 1) -> None:
        if self.current_value + amount <= self.max_value:
            self.current_value += amount

    def set_value(self, value: int) -> None:
        if value <= self.max_value and value >= self.min_value:
            self.current_value = value

    def generate_text(self) -> None:
        surface_text = self.base_font.render(str(self.current_value), True, pygame.Color(255, 255, 255))
        x_position = int(((self.rect.width / 2)) - (surface_text.get_rect().width / 2))
        self.image.blit(surface_text, (x_position, 0))

    def update(self) -> None:
        self.image.fill(Color(0, 0, 0))
        self.generate_slider()
        self.relative_positioning()
        
