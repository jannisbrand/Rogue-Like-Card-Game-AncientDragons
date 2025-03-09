from email.mime import application
import os
import random
import sqlite3
from typing import Any

import pygame
from Characters.Base import Character
from ECSO_Context import ECSO_Context
from Components import Components
from GUI.GUI import GUI
from GUI.Interactibles.Environmental import InteractibleEnvironmental
from GUI.Interactibles.Button import Button
from Handlers.Flags import SubscriptionType
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Menu import MenuLevel
from Handlers import Input_Handler
from Levels.Base import Level
from Renderer.Group_Types import SpriteGroupTypes
from Renderer.Renderer import Renderer
from Sprites import Base


class LevelFactory():
    def __init__(self, application, renderer: Renderer, ecso_context: "ECSO_Context", database_path: str = "Ancient-Dragons_Database.db"):
        # ### Database ### #
        self.application = application
        self.renderer = renderer
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
    
    def select_random_ressource(self, directory: str) -> str:
        ressources = os.listdir(directory)
        random_index = random.randint(0, len(ressources) - 1)
        return directory + "/" + ressources[random_index]
    
    def boss_level(self, round: int) -> int:
        application_rect = self.application.get_window().get_rect()

        ressource = self.select_random_ressource("Ressources/Pictures/Levels/Boss")

        entity = self.ecso_context.add_entity()
        created_level = Level(entity, "GAME_LEVEL", application_rect, "", (50, 50, 50), application_rect.width, application_rect.height, {}, ressource)
        self.ecso_context.add_game_object(entity, created_level)
        self.renderer.add_sprite(SpriteGroupTypes.LEVELS, created_level)
        print("[LEVELFACTORY][BOSS] Level generated with id: ", entity)
        return entity

    def standart_level(self, round: int) -> int:
        application_rect = self.application.get_window().get_rect()

        ressource = self.select_random_ressource("Ressources/Pictures/Levels/Standard")

        entity = self.ecso_context.add_entity()
        created_level = Level(entity, "GAME_LEVEL", application_rect, "", (50, 50, 50), application_rect.width, application_rect.height, {}, ressource)
        self.ecso_context.add_game_object(entity, created_level)
        self.renderer.add_sprite(SpriteGroupTypes.LEVELS, created_level)
        print("[OFactory] Level generated with id: ", entity)
        return entity

    def generate_level(self, round: int) -> int:
        # seed = 69
        # random.seed(seed)

        if round % 10 == 0:
            created_level = self.boss_level(round)
        else:
            created_level = self.standart_level(round)

        return created_level
