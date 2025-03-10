from typing import Callable
import pygame

from Sprites.Base import Sprite


class Character():
    def __init__(self, id: int, name: str):
        self.id = id    # ID
        self.name = name    # Name of the character
        self.health_max: int
        self.health: int  # Currency for life
        self.shield = 0

        self.is_alive = True
        self.sprite = int
        self.active_effects = {}

        self.health_changed = False
        self.effects_changed = False
        self.mana_changed = False

    def set_sprite(self, sprite_context_id: int) -> bool:
        try:
            self.sprite = sprite_context_id
            print("Added sprite:", sprite_context_id)
            return True
        except AttributeError as e:
            print("Could not at a Sprite object:", e)
            return False

    def get_sprite(self) -> Sprite:
        try:
            return self.sprite
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
            return None
        except ValueError as e:
            print("[CHARACTER][DATA]", e)
            return None

    def get_name(self) -> str:
        return self.name

    def get_health(self) -> int:
        return self.health
    
    def get_health_max(self) -> int:
        return self.health_max

    def set_health(self, value):
        try:
            self.health = value
            if self.health <= 0:
                self.health = 0
                self.is_alive = False
            self.health_changed = True
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
        except ValueError as e:
            print("[CHARACTER][DATA]", e)
        except TypeError as e:
            print("[CHARACTER][DATA]", e)

    def set_health_max(self, value):
        try:
            self.health_max = value
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
        except ValueError as e:
            print("[CHARACTER][DATA]", e)
        except TypeError as e:
            print("[CHARACTER][DATA]", e)

    def damage(self, value: int):
        try:
            if value > self.shield:
                after_shield = value - self.shield
                self.health -= after_shield
            else:
                self.shield -= value
            if self.health <= 0:
                self.health = 0
                self.is_alive = False
            self.health_changed = True
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
        except ValueError as e:
            print("[CHARACTER][DATA]", e)
        except TypeError as e:
            print("[CHARACTER][DATA]", e)

    def set_shield(self, value: int):
        try:
            self.shield = value
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
        except ValueError as e:
            print("[CHARACTER][DATA]", e)
        except TypeError as e:
            print("[CHARACTER][DATA]", e)

    def increase_shield(self, value: int):
        try:
            self.shield = self.shield + value
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
        except ValueError as e:
            print("[CHARACTER][DATA]", e)
        except TypeError as e:
            print("[CHARACTER][DATA]", e)

    def add_effect(self, effect: int, value: int):
        try:
            if effect not in self.active_effects:
                self.active_effects[effect]

            self.active_effects[effect] = value
            self.effects_changed = True
        except ValueError as e:
            print("[CHARACTER][DATA]", e)

    def get_effects(self) -> dict:
        try:
            return self.active_effects
        except AttributeError as e:
            print("[CHARACTER][DATA]", e)
            return []

    def get_effect(self, effect: int) -> int:
        try:
            return self.active_effects[effect]
        except KeyError as e:
            print(e)
            return 0
