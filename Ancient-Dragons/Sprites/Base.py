from typing import Any
import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, id, type, name, color, width, height, image_path: str = ""):
        super().__init__()
        self.id = id  # Represents object or entity id
        self.type = type
        self.name = name
        self.color = color
        if image_path == "":
            self.image = pygame.Surface((width, height))
            self.image.fill(self.color)
        else:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()

        self.callback_on_hover: None  # Callbacks for input handling
        self.callback_on_click: None
        self.callback_on_drag_on: None
        # pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
