import os
import sqlite3
from typing import Any

import pygame
from Characters.Base import Character
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
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

    def fabricate_player_characters(self):
        character_collection = self.database_connection.cursor().execute("SELECT * FROM Charakters")
        column_names = self.get_database_column_names("Charakters")
        for character_data in character_collection.fetchall():
            # PATTERN
            # CHARACTER ID; CHARACTER NAME;
            if len(character_data) != len(column_names):
                print("[OFactory] Character data and Colum names do not match!")
                continue

            entity = self.ecso_context.add_entity()
            created_character = PlayerCharacter(entity, character_data[1])
            created_character.set_health(1000)
            created_character.set_mana(10)
            created_character.set_gold(1000)
            self.ecso_context.add_game_object(entity, created_character)
            print("[OFactory] Created character: " + str(created_character))

    def fabricate_enemy(self) -> int:
        ENEMY_BASE_ATTACK = 137
        ENEMY_BASE_IDK = 0
    
        entity = self.ecso_context.add_entity()
        created_enemy = StandardEnemy(entity, "LUGENE CRABS")
        created_enemy.set_health(1000)
        created_enemy.set_attack_damage(ENEMY_BASE_ATTACK)
        self.ecso_context.add_game_object(entity, created_enemy)
        return entity
