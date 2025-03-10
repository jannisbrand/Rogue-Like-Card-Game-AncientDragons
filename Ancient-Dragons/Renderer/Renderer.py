from typing import Any, cast
import pygame
from Renderer.Group_Types import SpriteGroupTypes


class Renderer():
    def __init__(self, application):
        self.__application_context = application
        self.__clear_color: tuple
        self.__frames_per_secound: int
        self.queue: list
        self.sprite_groups: dict[SpriteGroupTypes, pygame.sprite.Group] = {
            SpriteGroupTypes.LEVELS: pygame.sprite.Group(),
            SpriteGroupTypes.GUIS: pygame.sprite.Group(),
            SpriteGroupTypes.CHARACTERS: pygame.sprite.Group(),
            SpriteGroupTypes.CARDS: pygame.sprite.Group(),
            SpriteGroupTypes.INTERACTIBLES: pygame.sprite.Group(),
            SpriteGroupTypes.POPUPS: pygame.sprite.Group(),
        }

    def initialise(self, clear_color: tuple, frames_per_secound) -> bool:
        self.__clear_color = clear_color
        self.__frames_per_secound = frames_per_secound
        return True

    def clear(self):
        self.__application_context.get_window().fill(self.__clear_color)

    def add_sprite(self, group: SpriteGroupTypes, sprite: Any):
        try:
            self.sprite_groups[group].add(sprite)
            print("[RENDERER]", sprite, "Added to", group.name)
        except AttributeError as e:
            print("[RENDERER]", e)

    def get_sprites_of_group(self, group: SpriteGroupTypes):
        try:
            return self.sprite_groups[group].copy()
        except AttributeError as e:
            print("[RENDERER]", e)

    def remove_sprite(self, group: SpriteGroupTypes, sprite: Any):
        try:
            self.sprite_groups[group].remove(sprite)
        except AttributeError as e:
            print("[RENDERER]", e)

    def render(self):
        self.clear()

        window = cast(pygame.Surface, self.__application_context.get_window())
        # for group_type, group in self.sprite_groups.items():
        #     cast(pygame.sprite.Group, group).draw(window)
        dirty_rects = []
        dirty_rects.extend(self.sprite_groups[SpriteGroupTypes.LEVELS].draw(window))
        dirty_rects.extend(self.sprite_groups[SpriteGroupTypes.GUIS].draw(window))
        dirty_rects.extend(self.sprite_groups[SpriteGroupTypes.CHARACTERS].draw(window))
        dirty_rects.extend(self.sprite_groups[SpriteGroupTypes.CARDS].draw(window))
        dirty_rects.extend(self.sprite_groups[SpriteGroupTypes.INTERACTIBLES].draw(window))
        dirty_rects.extend(self.sprite_groups[SpriteGroupTypes.POPUPS].draw(window))
        pygame.display.update(dirty_rects)

        pygame.display.flip()
        self.__application_context.get_clock().tick(self.__frames_per_secound)
