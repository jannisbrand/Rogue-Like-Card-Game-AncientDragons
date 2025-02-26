from typing import Any
from ECSO_Context import ECSO_Context
from Factories.Card_Factory import CardFactory
from Factories.Character_Factory import CharacterFactory
from Factories.GUI_Factory import GUIFactory
from Factories.Level_Factory import LevelFactory
from GUI.Base import GUI
from Handlers.Input_Handler import InputHandler
from Renderer import Renderer


class Gamemode():
    def __init__(self, id: int, name: str, input_handler: InputHandler, renderer: "Renderer") -> None:
        # ### GAMEMODE RELATED ### #
        self.id = id
        self.name = name
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
        self.active_character: int  # Id of the character in the context
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
                        self.factories[type] = CardFactory(self.ecso_context)
                    case "CHARACTERS":
                        self.factories[type] = CharacterFactory(self.ecso_context)
                    case "LEVELS":
                        self.factories[type] = LevelFactory(self.ecso_context)
                    case "GUIS":
                        self.factories[type] = GUIFactory(self.ecso_context, self.input_handler)
            except IndexError as e:
                print(f"[GAMEMODE] Factorie: {e} not found")
        # ### FACTORIES ### #
