from math import sin
import pygame
from typing import Any

from GUI.Base import GUI
from Sprites.Base import Sprite


"""
    First implentation with simple surfaces..
    Sprite classes come late.. Maybe
"""


class Level():
    def __init__(self, id: int, sprites: dict[str, list[Any]] = {}):
        self.id = id
        # BACKGROUND1; BACKGROUND2; FOREGROUND; XXXX
        self.environment: dict[str, list[Sprite]] = {}  # A list of "any" renderable data sorted to categories
        self.guis = []

        # ### STATIC ENVIRONMENT ### #
        # ### BACKGROUND1 ### #
        if len(sprites.keys()) > 0:
            self.environment["BACKGROUND1"] = []
            self.environment["BACKGROUND1"].extend(sprites["BACKGROUND1"])

            # ### BACKGROUND2 ### #
            # Like clouds etc..
            self.environment["BACKGROUND2"] = []
            self.environment["BACKGROUND2"].extend(sprites["BACKGROUND2"])

            # ### FOREGROUND1 ### #
            # Like trees, buildings, etc..
            self.environment["FOREGROUND1"] = []
            self.environment["FOREGROUND1"].extend(sprites["FOREGROUND1"])

            # ### FOREGROUND2 ### #
            # Like ground etc..
            self.environment["FOREGROUND2"] = []
            self.environment["FOREGROUND2"].extend(sprites["FOREGROUND2"])
        # ### STATIC ENVIRONMENT ### #

            self.animation_key_positions: dict[str, list[int]] = {}

        # ### STATIC ANIMATION KEY POSITIONS ### #
            self.animation_frame = 1

            self.animation_key_positions["BACKGROUND2"] = [5, 0, -5]
            self.background2_last_key = 0

            self.animation_key_positions["FOREGROUND1"] = [2, 0, -2]
            self.foreground1_last_key = 0

    def add_gui(self, gui: GUI) -> None:
        self.guis.append(gui)

    def get_gui(self, name: str) -> GUI:
        try:
            for gui in self.guis:
                if gui.name == name:
                    return gui
            return None
        except KeyError as e:
            print("No gui found! ", e)
            return None

    def get_sprites(self) -> list:
        list_of_sprites = []
        for category in self.environment:
            sprites = self.environment[category]
            list_of_sprites.extend(sprites)

        for gui in self.guis:
            list_of_sprites.append(gui)
            list_of_sprites.extend(gui.get_interactibles())
        return list_of_sprites

    def animation_state(self) -> None:

        # ### CLOUDS ### #
        offset = sin(self.animation_frame / 5) * 5  
        sprites = self.environment["BACKGROUND2"]
        for sprite in sprites:
            sprite.rect.y += int(offset)

        # ### TREES ### #
        offset = sin(self.animation_frame / 3) * 2
        sprites = self.environment["FOREGROUND1"]
        for sprite in sprites:
            sprite.rect.x += int(offset)
        
        self.animation_frame += 1

    def get_environment_type(self, type: str) -> list[Sprite]:
        return self.environment[type]

    def update(self) -> None:
        self.animation_state()

        for gui in self.guis:
            gui.update()
