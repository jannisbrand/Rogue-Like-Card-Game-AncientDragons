from math import sin
import pygame
from typing import Any

from Sprites.Base import Sprite


"""
    First implentation with simple surfaces..
    Sprite classes come late.. Maybe
"""


class Level():
    def __init__(self, id:int, surfaces: dict[str, list[Any]]):
        self.id = id
        # BACKGROUND1; BACKGROUND2; FOREGROUND; XXXX
        self.environment: dict[str, list[Any]] = {}  # A list of "any" renderable data sorted to categories

        # ### STATIC ENVIRONMENT ### #
        # ### BACKGROUND1 ### #
        self.environment["BACKGROUND1"] = []
        self.environment["BACKGROUND1"].extend(surfaces["BACKGROUND1"])

        # ### BACKGROUND2 ### #
        self.environment["BACKGROUND2"] = []
        self.environment["BACKGROUND2"].extend(surfaces["BACKGROUND2"])

        # ### FOREGROUND1 ### #
        self.environment["FOREGROUND1"] = []
        self.environment["FOREGROUND1"].extend(surfaces["FOREGROUND1"])

        # ### FOREGROUND2 ### #
        self.environment["FOREGROUND2"] = []
        self.environment["FOREGROUND2"].extend(surfaces["FOREGROUND2"])
        # ### STATIC ENVIRONMENT ### #

        self.animation_key_positions: dict[str, list[int]] = {}

        # ### STATIC ANIMATION KEY POSITIONS ### #
        self.animation_frame = 1

        self.animation_key_positions["BACKGROUND2"] = [5, 0, -5]
        self.background2_last_key = 0

        self.animation_key_positions["FOREGROUND1"] = [2, 0, -2]
        self.foreground1_last_key = 0

    def get_sprites(self) -> list:
        list_of_sprites = []
        for category in self.environment:
            sprites = self.environment[category]
            list_of_sprites.extend(sprites)
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

    def update(self) -> None:
        self.animation_state()
