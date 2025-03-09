import pygame
from Characters.Base import Character


class Passive_Stats(Character):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.passive_effects: set[int]  # Entities representing effects
