from typing import Any
import pygame

from GUI.GUISprite import GUISprite
from Sprites.Base import Sprite


class GUI(GUISprite):
    """
    NOTE: If a text or title gets added it gets blit to the Surface() of the background.
    That means the text stays at the same position relative to the gui's position.
    """
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)

    def update(self) -> None:
        pass
