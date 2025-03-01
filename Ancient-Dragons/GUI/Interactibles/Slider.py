from pygame import Color, Surface
import pygame
from Sprites.Base import Sprite


class ProgressBar(Sprite):
    def __init__(self, context_id, type_id, name, color, value_color: Color, width, height, max_value: int, min_value: int, image_path=""):
        super().__init__(context_id, type_id, name, color, width, height, image_path)
        self.max_value = max_value
        self.min_value = min_value
        self.total_range = min_value + max_value
        self.current_value = max_value  # Initial state is 100%
        self.fragmentation = 10
        self.fragment_width = int(self.total_range / 10)
        self.value_color = value_color

        self.base_font = pygame.font.Font("Fonts/Agency_Gothic_CT.otf", height - 2)

        self.offset_x = int((self.min_value + self.max_value) / 10)

    def generate_slider(self) -> None:
        background = Surface((self.rect.width, self.rect.height))
        background.fill(pygame.Color(20, 20, 20))

        # self.fragment_width = int(self.current_value / self.fragmentation)
        amount_of_fragments = int((self.current_value / self.total_range) * (self.total_range / self.fragment_width)) * 2
        for index in range(amount_of_fragments):
            fragment = Surface((self.fragment_width, self.rect.height))
            fragment.fill(self.value_color)
            x_placement_offset = self.fragment_width
            background.blit(fragment, (fragment.get_rect().x + (x_placement_offset * index), background.get_rect().y))
            index += 1
        self.image.blit(background, (0, 0))
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
        
