import pygame
from Level import Level
from LevelManager import LevelManager

running = True

pygame.init()
pygame.font.init()
global_font = pygame.font.SysFont("Consolas", 72)

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
clock = pygame.time.Clock()

levelManager = LevelManager(window)

# Mini Level factories..
test_level = Level()
for coord in range(0, 600):
    surface = pygame.Surface((coord, coord * 1.5))
    surface.fill((coord * 0.4, 0, 0))
    surface.get_width()
    test_level.add_environmental(surface)
surface = pygame.Surface((500, 300))
surface = global_font.render("LEVEL: 1", False, (0, 0, 0))
test_level.add_environmental(surface)

test_level_2 = Level()
for coord in range(0, 600):
    surface = pygame.Surface((coord + 100, coord * 1.5))
    surface.fill((0, coord * 0.4, 0))
    surface.get_width()
    test_level_2.add_environmental(surface)
surface = pygame.Surface((500, 300))
surface = global_font.render("LEVEL: 2", False, (0, 0, 0))
test_level_2.add_environmental(surface)
# End of mini level factories..

levelManager.add_level("TEST1", test_level)
levelManager.add_level("TEST2", test_level_2)

while running:
    window.fill((25, 10, 50))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print("KEY")
            if event.key == pygame.K_ESCAPE:
                print("ESCAPE")
                running = False
            elif event.key == pygame.K_1:
                levelManager.load_level("TEST1")
            elif event.key == pygame.K_2:
                levelManager.load_level("TEST2")
            elif event.key == pygame.K_0:
                levelManager.load_level("")
        elif event.type == pygame.QUIT:
            running = False

    levelManager.update()

    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)

pygame.display.quit()
pygame.quit()
