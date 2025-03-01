import pygame
from GUI.GUI import GUI
from GUI.Interactibles.Button import Button
from Levels.Base import Level
from Sprites.Base import Sprite


class MenuLevel(Level):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, sprites=..., image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, sprites, image_path)

    # def set_image(self, image: pygame.Surface):
    #     width = self.base_surface.get_rect().width
    #     height = self.base_surface.get_rect().height
    #     self.base_surface = image
    #     self.base_surface = pygame.transform.scale(self.base_surface, (width, height))
