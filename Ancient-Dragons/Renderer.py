import pygame

from Sprites.Base import Sprite


class Renderer():
    def __init__(self, application):
        self.__application_context = application
        self.__clear_color: tuple
        self.__frames_per_secound: int
        self.sprite_list = pygame.sprite.Group()

    def initialise(self, clear_color: tuple, frames_per_secound) -> bool:
        self.__clear_color = clear_color
        self.__frames_per_secound = frames_per_secound
        return True

    def clear(self):
        self.__application_context.get_window().fill(self.__clear_color)

    def add_sprites(self, sprites: list[Sprite]):
        for sprite in sprites:
            self.sprite_list.add(sprite)

    def render(self):
        self.sprite_list.draw(self.__application_context.get_window())

        pygame.display.flip()
        self.__application_context.get_clock().tick(self.__frames_per_secound)
