import sqlite3
from typing import Any

import pygame
from Characters.Base import Character
from ECSO_Context import ECSO_Context
from Components import Components


class CharacterFactory():
    def __init__(self, ecso_context: "ECSO_Context", database_path: str = "Ancient-Dragons_Database.db"):
        # ### Database ### #
        self.database_connection = sqlite3.connect(database_path)
        # ### Database ### #

        self.ecso_context = ecso_context

    def get_database_column_names(self, table: str) -> list[str]:
        table_info = self.database_connection.cursor().execute(f"PRAGMA table_info({table})")
        column_names = list()
        for column in table_info:
            column_name = column[1]
            column_names.append(column_name)
        return column_names

    def fabricate_all(self):
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
