import pygame
from Level import Level


class LevelManager():
    def __init__(self, window: pygame.Surface):
        self.app_window = window
        self.active_level = ""
        self.levels: dict[str, Level] = {}

    def add_level(self, level_name: str, level: Level):
        self.levels[level_name] = level

    def load_level(self, level_key: str):
        self.active_level = level_key

    def update(self):
        if self.active_level:
            self.levels[self.active_level].render(self.app_window)
