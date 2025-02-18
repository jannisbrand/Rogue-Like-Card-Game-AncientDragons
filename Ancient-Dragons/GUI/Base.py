from tkinter import font
from typing import Any
import pygame


class GUI(pygame.sprite.Sprite):
    """
    NOTE: If a text or title gets added it gets blit to the Surface() of the background.
    That means the text stays at the same position relative to the gui's position. 
    """
    def __init__(self, id: int, color: pygame.Color, name: str = "DEFAULT_NAME", width: int = 50, height: int = 50, pos_x: int = 0, pos_y: int = 0):
        super().__init__()
        self.id = id
        self.name = name
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.image.get_rect().width = width
        self.image.get_rect().height = height
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.__font_title = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 16)
        self.__font_text = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 11)
        self.titel: str
        self.text: str
        self.is_active = False

        self.interactibles: list[pygame.sprite.Sprite] = [] # Collection of all interactible buttons, etc.

    def get_surface(self) -> pygame.Surface:
        return self.image

    def get_rect(self) -> pygame.Rect:
        return self.rect

    def set_size(self, width, height) -> None:
        self.image.get_rect().width = width
        self.image.get_rect().height = height

    def set_pos(self, pos_x: int, pos_y: int) -> None:
        self.rect.x = pos_x
        self.rect.y = pos_y

    def get_pos(self) -> tuple[int, int]:
        return (self.image.get_rect().x, self.image.get_rect().y)

    def set_title(self, title: str = "") -> None:
        surface = self.__font_title.render(title, True, (255, 255, 255))
        self.__correct_text_pos("TITLE", surface)
        self.image.blit(surface, (self.image.get_rect().x, self.image.get_rect().y))
    
    def set_image(self, image: pygame.Surface) -> None:
        self.image = image
        self.image.get_rect().width = self.width
        self.image.get_rect().height = self.height

    def __correct_text_pos(self, type: str, surface: pygame.Surface) -> None:
        gui_middle_x = self.image.get_rect().x + (self.image.get_rect().width / 2)
        if type == "TITLE":
            surface.get_rect().x = gui_middle_x - int((surface.get_rect().width / 2))
            surface.get_rect().y = self.image.get_rect().y + 20
        elif type == "TEXT":
            surface.get_rect().x = gui_middle_x - int((surface.get_rect().width / 2))
            surface.get_rect().y = self.image.get_rect().y + 80
        # self.background.blit(surface)

    def add_interactible(self, interactible: pygame.sprite.Sprite) -> None:
        """Just to keep the reference. If surface get blit to the GUI on_hover dow not work in this setup
        """
        self.interactibles.append(interactible)

    def update(self) -> None:
        # self.__correct_text_pos()  # Only needed if the text change during objects life time
        pass
