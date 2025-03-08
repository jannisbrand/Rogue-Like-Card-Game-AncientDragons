from typing import Any, Callable, cast
from Characters.Player_Character import PlayerCharacter
from Characters.Standard_Enemy import StandardEnemy
from ECSO_Context import ECSO_Context
from Factories.Card_Factory import CardFactory
from Factories.Character_Factory import CharacterFactory
from Factories.GUI_Factory import GUIFactory
from Factories.Level_Factory import LevelFactory
from GUI.Base import GUISprite
from GUI.GUI import GUI
from GUI.Interactibles.Base import InteractibleSprite
from GUI.Interactibles.Button import Button
from GUI.Interactibles.Card import Card
from GUI.Interactibles.Character import InteractibleCharacter
from GUI.Interactibles.Environmental import InteractibleEnvironmental
from GUI.Interactibles.Slider import ProgressBar
from GUI.Interactibles.Sprite_List import SpriteList
from Handlers.Input_Handler import InputHandler
from Handlers.Subscriptions.Types import InputSubscribtion
from Levels.Base import Level
from Levels.Menu import MenuLevel
from Renderer.Renderer import Renderer
from Sprites.Base import Sprite
from Systems.Stacks.Base import CardStack


class Gamemode():
    def __init__(self, id: int, name: str, application, input_handler: InputHandler, renderer: "Renderer") -> None:
        # ### GAMEMODE RELATED ### #
        self.id = id
        self.name = name
        self.application = application
        self.ecso_context = ECSO_Context()
        self.input_handler = input_handler
        self.renderer = renderer

        self.is_initialised = False
        self.is_started = False
        self.is_finished = False
        self.next_gamemode: str

        self.is_generating_stacks: bool
        self.is_creating_gui: bool
        self.is_generating_level: bool
        self.is_shuffling: bool
        self.move_running: bool
        
        self.current_stage = 0
        self.active_level: int  # Id of the level in the context
        self.active_player_character: int  # Id of the character in the context
        self.active_enemy_character: int
        self.active_play_stack: int
        self.selected_type: str

        self.on_round_start = None
        self.on_round_end = None
        # ### GAMEMODE RELATED ### #

        self.create_factories()

        # ### STACKS ### #
        self.card_stacks: dict[str, list] = {}
        # ### STACKS ### #

    def create_factories(self) -> None:
        # ### FACTORIES ### #
        self.factories: dict[str, Any] = {}
        for type in ["CARDS", "CHARACTERS", "LEVELS", "GUIS"]:
            try:
                match type:
                    case "CARDS":
                        self.factories[type] = CardFactory(self.application, self.renderer, self.ecso_context)
                    case "CHARACTERS":
                        self.factories[type] = CharacterFactory(self.application, self.renderer, self.ecso_context)
                    case "LEVELS":
                        self.factories[type] = LevelFactory(self.application, self.renderer, self.ecso_context)
                    case "GUIS":
                        self.factories[type] = GUIFactory(self.application, self.renderer, self.ecso_context, self.input_handler)
            except IndexError as e:
                print(f"[GAMEMODE] Factorie: {e} not found")
        # ### FACTORIES ### #