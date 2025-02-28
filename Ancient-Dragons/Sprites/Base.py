from typing import Any, Callable
import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, id, type, name, color, width, height, image_path: str = ""):
        super().__init__()
        self.id = id  # Represents object or entity id
        self.type = type
        self.name = name
        self.color = color

        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(self.color)

        self.rect = self.image.get_rect()

        self.callback_on_hover: Callable  # Callbacks for input handling
        self.callback_on_click: Callable
        self.callback_on_drag_on: Callable
        # pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
