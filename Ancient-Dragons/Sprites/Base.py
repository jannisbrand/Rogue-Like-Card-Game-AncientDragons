import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, name, color, width, height, image_path: str = ""):
        super().__init__()
        self.name = name
        if image_path == "":
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(image_path)

        # pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()
