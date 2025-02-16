import pygame
from typing import Any


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

        # ### FOREGROUND ### #
        self.environment["FOREGROUND"] = []
        self.environment["FOREGROUND"].extend(surfaces["FOREGROUND"])
        # ### STATIC ENVIRONMENT ### #

    def get_sprites(self) -> list:
        list_of_sprites = []
        for category in self.environment:
            sprites = self.environment[category]
            list_of_sprites.extend(sprites)
        return list_of_sprites

    def update(self) -> None:
        pass
