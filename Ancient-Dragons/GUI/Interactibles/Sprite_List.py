from typing import cast
from pygame import Surface
from Sprites.Base import Sprite


class SpriteList(Sprite):
    def __init__(self, context_id, type_id, reference_rect, name, color, width, height, image_path = ""):
        super().__init__(context_id, type_id, reference_rect, name, color, width, height, image_path)
        self.rect.x = self.reference_rect.x
        self.rect.y = self.reference_rect.y

        self.sprites: list[Sprite] = []

    def add_sprite(self, sprite: Sprite):
        try:
            self.sprites.append(sprite)
        except AttributeError as e:
            print("[INTERACTIBLE][SPITE_LIST]", e)
        except ValueError as e:
            print("[INTERACTIBLE][SPRITE_LIST]", e)

    def calculate_size(self):
        for sprite in self.sprites:
            sprite.rect.width = self.rect.height  # SQUARE
            sprite.rect.height = self.rect.height

    def calculate_position(self):
        index = 0
        for sprite in self.sprites:
            sprite.rect.x = self.rect.x + (sprite.rect.width * index)
            self.image.blit(sprite.image, (sprite.rect.width * index, 0))
            index += 1

    def get_sprites(self) -> list:
        try:
            return [self]
        except AttributeError as e:
            print("[INTERACTIBLE][SPITE_LIST]", e)
        except ValueError as e:
            print("[INTERACTIBLE][SPRITE_LIST]", e)

    def update(self):
        # Resize all of listed sprites to own size
        # Position all of listed sprites relative to it self
        self.calculate_size()
        self.calculate_position()
