import pygame

class Level():
    def __init__(self):
        self.environment = set()    # Set of Surfaces
        self.next_environment_id = 1

    def add_environmental(self, surface: pygame.Surface):
        self.environment.add(surface)

    def render(self, window: pygame.Surface):
        list_of_environment_surfaces = []
        for env in self.environment:
            iterator = (env, (env.get_width(), env.get_height()))
            list_of_environment_surfaces.append(iterator)
        window.blits(list_of_environment_surfaces)
