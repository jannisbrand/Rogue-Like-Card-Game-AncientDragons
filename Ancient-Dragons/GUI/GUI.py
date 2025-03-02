from tkinter import font
from typing import Any
import pygame

from GUI.Base import GUISprite
from Sprites.Base import Sprite


class GUI(GUISprite):
    """
    NOTE: If a text or title gets added it gets blit to the Surface() of the background.
    That means the text stays at the same position relative to the gui's position.
    """
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path=""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        self.name = name

        self.rect.x = self.reference_rect.x
        self.rect.y = self.reference_rect.y

        self.__font_title = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 16)
        self.__font_text = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 11)
        self.titel: str
        self.text: str
        self.is_active = True
        self.destroy = False

        self.interactibles: list[int] = []  # Collection of all interactible buttons, etc. as their context id's

    def set_title(self, title: str = "") -> None:
        surface = self.__font_title.render(title, True, (255, 255, 255))
        self.__correct_text_pos("TITLE", surface)
        self.image.blit(surface, (surface.get_rect().x, surface.get_rect().y))
    
    def set_image(self, image: pygame.Surface) -> None:
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def __correct_text_pos(self, type: str, surface: pygame.Surface) -> None:
        gui_middle_x = self.rect.x + (self.rect.width / 2)
        if type == "TITLE":
            surface.get_rect().x = int(gui_middle_x - (surface.get_rect().width / 2))
            surface.get_rect().y = self.rect.y + 20
        elif type == "TEXT":
            surface.get_rect().x = int(gui_middle_x - (surface.get_rect().width / 2))
            surface.get_rect().y = self.rect.y + 80
        # self.background.blit(surface)

    def add_interactible(self, interactible: int) -> None:
        """Just to keep the reference. If surface get blit to the GUI on_hover dow not work in this setup
        """
        self.interactibles.append(interactible)

    def remove_interactible(self, interactible: int):
        try:
            self.interactibles.remove(interactible)
        except ValueError as e:
            print("[GUI] Interactible context-id could not be removed:", e)

    def get_interactibles(self) -> list[int]:
        try:
            return self.interactibles
        except AttributeError as e:
            print("[GUI] Could not retrieve list of interactibles:", e)

    def update(self) -> None:
        # Only cares about it's own thing! Interactibles are stored just to keep a the references!
        # self.__correct_text_pos()  # Only needed if the text change during objects life time
        self.relative_positioning()
        pass
