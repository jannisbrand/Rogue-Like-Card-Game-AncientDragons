import os
import sqlite3
from typing import Any

import pygame
from Characters.Base import Character
from Characters.Boss_Enemy import BossEnemy
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from ECSO_Context import ECSO_Context
from Components import Components
from Renderer.Group_Types import SpriteGroupTypes

HEALTH_DEFAULT_START = 10
HEALTH_PLAYER_START = 10
HEALTH_ENEMY_START = 10
HEALTH_PRGRESSION = 1.15


class CharacterFactory():
    def __init__(self, application, renderer, ecso_context: "ECSO_Context", database_path: str = "Ancient-Dragons_Database.db"):
        # ### Database ### #
        self.application = application
        self.renderer = renderer
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

    def generate_player(self, round: int):
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
            created_character.set_health(self.calculate_health(round))
            created_character.set_mana(10)
            created_character.set_gold(1000)
            self.ecso_context.add_game_object(entity, created_character)
            print("[OFactory] Created character: " + str(created_character))

    def boss_enemy(self, round: int) -> int:
        BOSS_BASE_ATTACK = 5
        ENEMY_BASE_IDK = 0

        entity = self.ecso_context.add_entity()
        created_enemy = BossEnemy(entity, "LUGENE CRABSUS")
        created_enemy.set_health(self.calculate_health(round, 1.20))
        created_enemy.set_attack_damage(BOSS_BASE_ATTACK)
        self.ecso_context.add_game_object(entity, created_enemy)
        return entity

    def standard_enemy(self, round: int) -> int:
        ENEMY_BASE_ATTACK = 3
        ENEMY_BASE_IDK = 0
    
        entity = self.ecso_context.add_entity()
        created_enemy = StandardEnemy(entity, "LUGENE CRABS")
        created_enemy.set_health(self.calculate_health(round))
        created_enemy.set_attack_damage(ENEMY_BASE_ATTACK)
        self.ecso_context.add_game_object(entity, created_enemy)
        return entity

    def generate_enemy(self, round: int) -> int:
        if round % 10 == 0:
            created_enemy = self.boss_enemy(round)
        else:
            created_enemy = self.standard_enemy(round)

        return created_enemy
    
    def calculate_health(self, round: int, multiplier: float = 1.0):
        return int(HEALTH_DEFAULT_START * pow(HEALTH_PRGRESSION, round)) * multiplier
