import pygame

from LevelManager import ENTLevelManager
from Systems import Systems
from components import color_surface, position

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
level_manager = ENTLevelManager()

for i in range(0, 20):
    new = level_manager.create_entity()
    new_surface = color_surface((i * 10, 90, 144))
    new_position = position(int(window.get_width() / 2) + (i * 15), int(window.get_height() / 2) + (i * 15), 1)
    level_manager.add_component(new, new_surface)
    level_manager.add_component(new, new_position)

running = True

while running:
    window.fill((50, 75, 125))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    level_manager.update(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()