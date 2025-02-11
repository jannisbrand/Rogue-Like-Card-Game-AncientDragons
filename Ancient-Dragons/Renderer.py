import pygame


class Renderer():
    def __init__(self, application):
        self.__application_context = application
        self.__clear_color: tuple
        self.__frames_per_secound: int

    def initialise(self, clear_color: tuple, frames_per_secound) -> bool:
        self.__clear_color = clear_color
        self.__frames_per_secound = frames_per_secound
        return True

    def clear(self):
        self.__application_context.get_window().fill(self.__clear_color)

    def add_surface(self):
        pass

    def render(self):
        pygame.display.flip()
        self.__application_context.get_clock().tick(self.__frames_per_secound)
