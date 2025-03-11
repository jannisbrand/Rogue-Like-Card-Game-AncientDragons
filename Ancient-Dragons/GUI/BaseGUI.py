from typing import Any, Callable
import pygame


class BaseGUI(pygame.sprite.Sprite):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path=""):
        super().__init__()
        self.context_id = context_id  # Represents object or entity id
        self.type_id = type_id
        self.reference_rect = reference_rect
        self.name = name
        self.color = color

        if image_path != "":
            self.image = pygame.image.load(image_path)
            self.image.convert()
            self.image.convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(self.color)

        # ### POSITION & SIZE ### #
        self.rect = self.image.get_rect()
        self.relative_x = 0
        self.relative_y = 0
        self.rect.x = self.relative_x
        self.rect.y = self.relative_y
        self.rect.width = width
        self.rect.height = height
        # ### POSITION ### #

        # ### SUBSCRIBTION ### #
        self.is_hovered_over = False
        self.subscribtion_on_click: int  # Holds the entity id of the input subscribtion
        self.subscribtion_on_hover: int  # Holds the entity id of the input subscribtion
        self.callback_on_hover = None  # Optional: Holds the reference to an method &/ or function wich is called with the execution of an event
        self.callback_on_click = None  # Optional: Holds the reference to an method &/ or function wich is called with the execution of an event
        self.callback_on_drag_on = None  # TODO: Not implemented yet

        # ### STATE ### #
        self.is_visible = True
        self.is_active = True
        self.destroy = False
        # ### STATE ### #

        # ### CONTAINER ### #
        self.interactibles: list[int] = []  # Collection of all interactible buttons, etc. as their context id's
        # ### CONTAINER ### #

    def set_image(self, path: str) -> None:
        try:
            self.image = pygame.image.load(path)
            self.image.convert()
            self.image.convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        except FileNotFoundError as e:
            print("[GUI]", e)
        except pygame.error as e:
            print("[GUI]", e)

    def get_context_id(self) -> int:
        try:
            return self.context_id
        except AttributeError as e:
            print("[GUI] Context id could not be found:", e)

    def get_type_id(self) -> str:
        try:
            return self.type_id
        except AttributeError as e:
            print("[GUI] Type id could not be found:", e)

    def get_name(self) -> str:
        try:
            return self.name
        except AttributeError as e:
            print("[GUI] Name could not be found:", e)

    def relative_positioning(self):
        try:
            # ### INITIAL RELATIVE POSITIONING ### #
            self.rect.x = self.reference_rect.x + self.relative_x
            self.rect.y = self.reference_rect.y + self.relative_y
        except AttributeError as e:
            print("[GUI]", e)

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

    def update(self):
        # self.__correct_text_pos()  # TODO: NOT TESTED! Only needed if the text change during objects life time.
        self.relative_positioning()
