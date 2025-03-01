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
        self.guis = []  # Collection of guis as their context id's

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

    def add_gui(self, gui: int) -> None:
        try:
            self.guis.append(gui)
        except AttributeError as e:
            print("[LEVEL] GUI sequence could not be found:", e)
        except ValueError as e:
            print("[LEVEL] Context id could not be added:", e)

    def get_guis(self) -> list[int]:
        try:
            return self.guis
        except AttributeError as e:
            print("[LEVEL] GUI seqence could not be found:", e)
            return []

    def get_sprites(self) -> list:
        try:
            list_of_sprites = []
            for _, value in self.environment.items():
                list_of_sprites.extend(value)
            return list_of_sprites
        except Exception as e:
            print("[LEVEL] Something:", e)

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
