from typing import Any, Callable
import pygame


class GUISprite(pygame.sprite.Sprite):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path=""):
        super().__init__()
        self.context_id = context_id  # Represents object or entity id
        self.type_id = type_id
        self.name = name
        self.color = color
        self.reference_rect = reference_rect

        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(self.color)

        self.rect = self.image.get_rect()

        self.is_hovered_over = False

        self.subscribtion_on_click: int
        self.subscribtion_on_hover: int
        self.callback_on_hover = None  # Callbacks for input handling
        self.callback_on_click = None
        self.callback_on_drag_on = None

        self.is_visible = True
        self.destroy = False
        # pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))

    def get_context_id(self) -> int:
        try:
            return self.context_id
        except AttributeError as e:
            print("[SPRITE] Context id could not be found:", e)

    def get_type_id(self) -> str:
        try:
            return self.type_id
        except AttributeError as e:
            print("[SPRITE] Type id could not be found:", e)

    def get_name(self) -> str:
        try:
            return self.name
        except AttributeError as e:
            print("[SPRITE] Name could not be found:", e)

    
