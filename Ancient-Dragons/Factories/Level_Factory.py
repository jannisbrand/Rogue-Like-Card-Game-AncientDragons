import random
import sqlite3
from typing import Any

import pygame
from Characters.Base import Character
from ECSO_Context import ECSO_Context
from Components import Components
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

    def fabricate_all(self):
        """NOT IMPLEMENTED"""
        character_collection = self.database_connection.cursor().execute("SELECT * FROM Charakters")
        column_names = self.get_database_column_names("Charakters")
        for character_data in character_collection.fetchall():
            # PATTERN
            # CHARACTER ID; CHARACTER NAME;
            if len(character_data) != len(column_names):
                print("[OFactory] Character data and Colum names do not match!")
                continue

            created_character = Character(character_data[0], character_data[1], None)
            created_character.health_points = 100
            created_character.mana_points = 100
            created_character.gold_points = 100
            self.ecso_context.add_object("CHARACTERS", created_character)
            print("[OFactory] Created character: " + str(created_character))

    def generate_level(self) -> Any:
        # seed = 69
        # random.seed(seed)

        environment_categories = ["BACKGROUND1", "BACKGROUND2", "FOREGROUND"]
        
        sprites: dict[str, list[Any]] = {}
        for category in environment_categories:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = pygame.Color(r, g, b)
            sprite = Base.Sprite(color, 50, 50)
            sprite.rect.x += random.randint(0, 100)
            sprite.rect.y += random.randint(0, 100)

            if category not in sprites:
                sprites[category] = []

            sprites[category].append(sprite)

        created_level = Level(self.ecso_context.next_object_id, sprites)
        print("[OFactory] Level generated with id: ", self.ecso_context.next_object_id)
        self.ecso_context.add_object("LEVELS", created_level)
