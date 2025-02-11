from hmac import new
from math import cos, sin
from typing import Type
import pygame
from components import color_surface, position
from Systems import Systems


class ENTLevelManager():
    def __init__(self):
        self.level_entities: set[int] = set()
        self.level_components: dict[Type, dict[int, any]] = dict()
        self.next_level_id = 1
        self.active_level: int

    def create_entity(self) -> int:
        entity = self.next_level_id
        self.level_entities.add(self.next_level_id)
        self.next_level_id += 1
        return entity

    def add_component(self, entity: int, component: any) -> bool:
        component_type = type(component)
        if component_type not in self.level_components:
            self.level_components[component_type] = {}
            self.level_components[component_type][entity] = component
            return True
        else:
            self.level_components[component_type][entity] = component
        return False

    def update(self, window: pygame.Surface):
        list_of_drawable_surfaces = []
        if color_surface in self.level_components and position in self.level_components:
            for entity in self.level_entities:
                surface_component = self.level_components[color_surface][entity]
                position_component = self.level_components[position][entity]

                
                surface_component = surface_component
                pos_x = position_component.x
                pos_y = position_component.y
                pos_z = position_component.z
                systems = Systems()
                # systems.translation_system((pos_x, pos_y, pos_z), (0.001, 0.000, 0.000), position_component)
                clk = pygame.time.Clock()
                new_x = sin(entity / 10) * 100 + 50
                new_y = cos(entity / 10) * 100 + 50
                print("\033[2J\033[H")
                print(new_x, end="")
                print(new_y)
                Systems.translation_system((pos_x, pos_y, pos_z), (0, 0, 0), position_component)

                list_of_drawable_surfaces.append((surface_component.surface, (new_x, new_y)))
    
        window.blits(list_of_drawable_surfaces)
