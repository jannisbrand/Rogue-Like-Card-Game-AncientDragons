import pygame


class color_surface():
    def __init__(self, color: tuple):
        self.surface = pygame.Surface((50, 50))
        self.surface.fill(color)

class position():
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class image_surface():
    def __init__(self, image_path):
        self.surface = pygame.image.load(image_path)
