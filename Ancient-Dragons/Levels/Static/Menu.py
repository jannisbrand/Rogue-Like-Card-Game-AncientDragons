import pygame
from GUI.Base import GUI
from GUI.Interactibles.Button import Button
from Levels.Base import Level
from Sprites.Base import Sprite


class MenuLevel(Level):
    def __init__(self, id, name: str) -> None:
        self.name = name
        self.base_surface = Sprite(id, "MENU", name, pygame.Color(0, 0, 10), 1920, 1080, "")
        self.guis = []

        self.active = True

        # gui = GUI(0, pygame.Color(25, 25, 25, 150), "MAIN", 500, 700, 710, 200)
        # start_button = Button(0, gui.get_rect(), pygame.Color(25, 25, 40), pygame.Color(45, 45, 60), "btn_start", "START", 8, 200, 50, 150, 100)
        # gui.add_interactible(start_button)

        super().__init__(id)

    def set_image(self, image: pygame.Surface):
        width = self.base_surface.rect.width
        height = self.base_surface.rect.height
        self.base_surface.image = image
        self.base_surface.image = pygame.transform.scale(self.base_surface.image, (width, height))

    def add_gui(self, gui: GUI) -> None:
        # Id of the object in the context
        self.guis.append(gui)

    def get_sprites(self):
        list_of_sprites = []
        list_of_sprites.append(self.base_surface)
        for gui in self.guis:
            list_of_sprites.append(gui)

        for gui in self.guis:
            list_of_sprites.extend(gui.get_interactibles())
        return list_of_sprites
    
    def deactivate(self) -> None:
        self.active = False

    def update(self) -> None:
        for gui in self.guis:
            gui.update()
