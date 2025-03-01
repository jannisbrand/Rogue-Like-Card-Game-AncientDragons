import pygame
from Sprites.Base import Sprite


class Renderer():
    def __init__(self, application):
        self.__application_context = application
        self.__clear_color: tuple
        self.__frames_per_secound: int
        self.queue: list
        self.sprite_list = pygame.sprite.Group()

    def initialise(self, clear_color: tuple, frames_per_secound) -> bool:
        self.__clear_color = clear_color
        self.__frames_per_secound = frames_per_secound
        return True

    def clear(self):
        self.__application_context.get_window().fill(self.__clear_color)

    def add_surface(self, surface: pygame.Surface):
        self.queue.append(surface)

    def add_sprites(self, sprites: list[Sprite]):
        print("[RENDERER] RECIEVED SPRITES:", sprites)
        for sprite in sprites:
            self.sprite_list.add(sprite)

    def render(self):
        self.clear()

        window = self.__application_context.get_window()
        self.sprite_list.draw(window)
        #self.sprite_list = pygame.sprite.Group()

        pygame.display.flip()
        self.__application_context.get_clock().tick(self.__frames_per_secound)
