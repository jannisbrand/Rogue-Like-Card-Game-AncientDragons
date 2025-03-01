import random
import sqlite3
from typing import Any

import pygame
from Characters.Base import Character
from ECSO_Context import ECSO_Context
from Components import Components
from GUI.Base import GUI
from GUI.Interactibles.Button import Button
from Handlers.Flags import SubscriptionType
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Static.Menu import MenuLevel
from Handlers import Input_Handler
from Levels.Base import Level
from Sprites import Base


class LevelFactory():
    def __init__(self, ecso_context: "ECSO_Context", database_path: str = "Ancient-Dragons_Database.db"):
        # ### Database ### #
        self.database_connection = sqlite3.connect(database_path)
        # ### Database ### #

        self.ecso_context = ecso_context

    def get_database_column_names(self, table: str) -> list[str]:
        """NOT IMPLEMENTED"""
        table_info = self.database_connection.cursor().execute(f"PRAGMA table_info({table})")
        column_names = list()
        for column in table_info:
            column_name = column[1]
            column_names.append(column_name)
        return column_names

    def generate_level(self) -> Any:
        # seed = 69
        # random.seed(seed)

        environment_categories = ["BACKGROUND1", "BACKGROUND2", "FOREGROUND1", "FOREGROUND2"]
        
        sprites: dict[str, list[Any]] = {}
        for category in environment_categories:
            if category not in sprites:
                sprites[category] = []

            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = pygame.Color(50, 50, 255)
            match category:
                case "BACKGROUND1":
                    sprite = Base.Sprite(-1, "---", "sky.color", color, 1440, 900)
                    sprite.rect.x = 0
                    sprite.rect.y = 0
                    sprites[category].append(sprite)
                case "BACKGROUND2":
                    # Clouds
                    for index in range(6):
                        sprite = Base.Sprite(-1, "---", "cloud.png", color, 200, 50, "Levels\Data\cloud.png")
                        sprite.rect.x += 250 * index
                        sprite.rect.y = 200
                        sprites[category].append(sprite)
                case "FOREGROUND1":
                    for index in range(4):
                        sprite = Base.Sprite(-1, "---", "tree.png", color, 200, 200, "Levels\Data\gangsta_tree.png")
                        sprite.rect.x = 350 * index + 100
                        sprite.rect.y = 500
                        sprites[category].append(sprite)
                case "FOREGROUND2":
                    sprite = Base.Sprite(-1, "---", "ground.color", (125, 80, 50), 1440, 500)
                    sprite.rect.x = 0
                    sprite.rect.y = 700
                    sprites[category].append(sprite)

        entity = self.ecso_context.add_entity()
        created_level = Level(entity, sprites)
        self.ecso_context.add_game_object(entity, created_level)
        print("[OFactory] Level generated with id: ", entity)
        return entity
