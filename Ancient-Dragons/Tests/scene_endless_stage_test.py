from dataclasses import dataclass
import unittest

from pygame import Rect
from Characters.Boss_Enemy import BossEnemy
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Level_GUI import LevelGUI
from Game.Endless import Endless
from Handlers.Input_Handler import InputHandler
from Levels.Base import Level
from Levels.Menu import MenuLevel
from Renderer.Renderer import Renderer
from Systems.Stacks.Exhaust import Exhaust
from Systems.Stacks.Hand import Hand
from Systems.Stacks.Play import Play
from main import Application


class SceneEndlessStageTest(unittest.TestCase):

    def setUp(self):
        self.application = Application(0, 0, 0, 0, 0, "")
        self.input_handler = InputHandler(self.application)
        self.renderer = Renderer(self.application)
        self.scene = Endless(0, "ENDLESS", self.application, self.input_handler, self.renderer)
        self.scene.initialise()

    def test_initialisation(self):
        # Created instance of ecso context
        self.assertIsNotNone(self.scene.ecso_context)

        # Dictionary with available facories
        self.assertGreater(len(self.scene.factories), 0, "Factory dictionary is empty!")
        for key in self.scene.factories.keys():
            self.assertIsInstance(key, str, f"Key: {key} ist kein String")

        for value in self.scene.factories.values():
            self.assertIsInstance(value, object, f"Factory: {value} is not an object!")

        # Flags
        self.assertEqual(len(self.scene.card_stacks), 0, "Card stack is not empty!")
        self.assertFalse(self.scene.is_finished, "is_finished")
        self.assertTrue(self.scene.is_initialised, "is_initialised")
        self.assertEqual(self.scene.current_stage, 0, "Initial stage is not 0")
        self.assertGreaterEqual(self.scene.current_round, 0, "Initial round is not 0")
        self.assertFalse(self.scene.game_over, "game_over")
        self.assertEqual(self.scene.active_level, -1, "No active Level should equal -1")
        self.assertEqual(self.scene.selected_type, "", "No selected type should equal """)
        self.assertEqual(self.scene.selected_card, -1, "No selected card should equal -1")
        self.assertEqual(self.scene.active_player_character, -1, "No selected player should be -1")
        self.assertEqual(self.scene.active_enemy_character, -1, "No selected player should be -1")
        self.assertFalse(self.scene.is_creating_gui, "is_creating_gui")
        self.assertFalse(self.scene.is_generating_level, "is_generating_level")
        self.assertFalse(self.scene.is_generating_stacks, "is_generation_stacks")

    def test_selection_menu(self):
        self.scene.current_stage = 0
        self.scene.update()

        # Check active level
        result_level = self.scene.ecso_context.get_game_object(self.scene.active_level, MenuLevel)
        self.assertIsInstance(result_level, MenuLevel, "No menu level could be found!")

        # Check level guis
        for gui_ids in result_level.get_guis():
            result_gui = self.scene.ecso_context.get_game_object(gui_ids, LevelGUI)
            self.assertIsNotNone(result_gui, f"GUI {gui_ids} could not be found")

            # Check interactibles
            for interactibles_id in result_gui.get_interactibles():
                result_interactible = self.scene.ecso_context.get_game_object(interactibles_id, Button)
                self.assertIsNotNone(result_interactible, f"Interactible: {interactibles_id} could not be found!")

    def test_create_stacks(self):
        # Get the first player character
        result_character_set = self.scene.ecso_context.get_game_objects_of_type(PlayerCharacter)
        self.assertIsNotNone(result_character_set, f"No characters could be found!")
        for _, character in result_character_set:
            self.scene.active_player_character = character.id
            break

        self.scene.current_stage = 1
        self.scene.update()

        play_stack_id = self.scene.active_play_stack
        self.assertGreaterEqual(play_stack_id, 0, f"Scene does not have an play stack id!")
        result_play_stack = self.scene.ecso_context.get_game_object(play_stack_id, Play)
        self.assertIsNotNone(result_play_stack, f"Play stack could not be found!")
        self.assertGreater(len(result_play_stack.get_cards()), 0, f"No cards in play stack: {result_play_stack}")

        exhaust_stack_id = self.scene.active_exhaust_stack
        self.assertGreaterEqual(exhaust_stack_id, 0, f"Scene does not have an exhaust stack!")
        result_exhaust_stack = self.scene.ecso_context.get_game_object(exhaust_stack_id, Exhaust)
        self.assertIsNotNone(result_exhaust_stack, f"Exhaust stack could not be found!")
        # Exhaust stack is empty initially!
        self.assertEqual(len(result_exhaust_stack.get_cards()), 0, f"No cards in exhaust stack: {result_exhaust_stack}")

        result_character = self.scene.ecso_context.get_game_object(self.scene.active_player_character, PlayerCharacter)
        self.assertIsNotNone(result_character)
        hand_stack_id = result_character.get_stack()
        self.assertGreaterEqual(hand_stack_id, 0, f"Character does not have a hand stack id!")
        result_hand_stack = self.scene.ecso_context.get_game_object(hand_stack_id, Hand)
        self.assertIsNotNone(result_hand_stack, f"Hand stack could not be found!")
        self.assertGreater(len(result_hand_stack.get_cards()), 0, f"No cards in hand stack: {result_hand_stack}")

    def test_generate_level(self):
        self.scene.current_stage = 2
        self.scene.update()

        self.assertGreaterEqual(self.scene.active_level, 0, f"Scene does not have an active level!")
        result_level = self.scene.ecso_context.get_game_object(self.scene.active_level, Level)
        self.assertIsNotNone(result_level, f"No level could be found!")

    def test_generate_enemy(self):
        self.scene.current_stage = 3
        self.scene.update()

        self.assertGreaterEqual(self.scene.active_enemy_character, 0, f"Scene does not have an active enemy character!")
        if self.scene.current_round % 10 == 0:
            result_enemy_character = self.scene.ecso_context.get_game_object(self.scene.active_enemy_character, BossEnemy)
            self.assertIsNone(result_enemy_character, f"No enemy boss character could be found!")
        else:
            result_enemy_character = self.scene.ecso_context.get_game_object(self.scene.active_enemy_character, StandardEnemy)
            self.assertIsNotNone(result_enemy_character, f"No enemy standard enemy character could be found!")

    def test_generate_character_gui(self):
        self.scene.current_stage = 2
        self.scene.update()
        self.scene.current_stage = 4
        self.scene.update()

        self.assertGreaterEqual(self.scene.active_level, 0, f"Scene does not have an active level!")
        result_level = self.scene.ecso_context.get_game_object(self.scene.active_level, Level)
        self.assertIsNotNone(result_level, f"No level could be found!")
        result_gui_ids = result_level.get_guis()
        self.assertGreater(len(result_gui_ids), 0, f"Level have not recieved a GUI!")
        result_gui = self.scene.ecso_context.get_game_object(result_gui_ids[0], LevelGUI)
        self.assertIsNotNone(result_gui, f"No gui could be found!")
        self.assertIsInstance(result_gui, LevelGUI, f"Gui is not of expected type!")

    # def test_generate_card_gui(self):
    #     self.scene.current_stage = 1
    #     self.scene.update()
    #     self.scene.current_stage = 2
    #     self.scene.update()
    #     self.scene.current_stage = 5
    #     self.scene.update()

    #     self.assertGreaterEqual(self.scene.active_level, 0, f"Scene does not have an active level!")
    #     result_level = self.scene.ecso_context.get_game_object(self.scene.active_level, Level)
    #     self.assertIsNotNone(result_level, f"No level could be found!")
    #     result_gui_ids = result_level.get_guis()
    #     self.assertGreater(len(result_gui_ids), 0, f"Level have not recieved a GUI!")
    #     result_gui = self.scene.ecso_context.get_game_object(result_gui_ids[1], LevelGUI)
    #     self.assertIsNotNone(result_gui, f"No gui could be found!")
    #     self.assertIsInstance(result_gui, LevelGUI, f"Gui is not of expected type!")


    def test_select_target(self):
        @dataclass
        class TestComponent():
            name = ""

        target_types = [
            "INTERACTIBLE_CARD_SPRITE",
            "INTERACTIBLE_PLAYER_CHARACTER_SPRITE",
            "INTERACTIBLE_ENEMY_CHARACTER_SPRITE",
        ]

        test_card_entity = 0
        test_character_entity = 1
        
        for target_type in target_types:
            test_card_sprite = Card(0, test_card_entity, target_type, Rect(0, 0, 0, 0), "", (0, 0, 0), 0, 0)
            test_character_sprite = InteractibleCharacter(1, test_character_entity, target_type, Rect(0, 0, 0, 0), "", (0, 0, 0), 0, 0)

            if target_type == "INTERACTIBLE_CARD_SPRITE":
                self.scene.stage_select_targets(test_card_sprite, (True, False, False))
                self.assertEqual(self.scene.selected_card, test_card_sprite.card_context_id)
            elif target_type == "INTERACTIBLE_PLAYER_CHARACTER_SPRITE":
                self.scene.stage_select_targets(test_character_sprite, (True, False, False))
                self.assertEqual(self.scene.selected_target, test_character_sprite.character_context_id)
            elif target_type == "INTERACTIBLE_ENEMY_CHARACTER_SPRITE":
                self.scene.stage_select_targets(test_character_sprite, (True, False, False))
                self.assertEqual(self.scene.selected_target, test_character_sprite.character_context_id)
                if self.scene.current_round % 10 == 0:
                    self.assertIs(self.scene.selected_type, BossEnemy, f"Selected target is not from type: {BossEnemy}")
                else:
                    self.assertIs(self.scene.selected_type, StandardEnemy, f"Selected target is not from type: {StandardEnemy}")
