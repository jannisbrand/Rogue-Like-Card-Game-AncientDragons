from random import randint
from re import S
from typing import Any

import pygame
from Components import Components
from Components.Components import C_DISPLAY_NAME
from ECSO_Context import ECSO_Context
from Factories.Character_Factory import CharacterFactory
from Factories.Card_Factory import CardFactory
from Factories.Level_Factory import LevelFactory
from Renderer import Renderer


# ### GLOBAL GAMERULES ### #
AMOUNT_PLAYER_CHARACTERS_MAX = 1
AMOUNT_CARDS_MAX = 9999
AMOUNT_CARDS_MIN = 0
AMOUNT_CARDS_ON_DECK_MAX = 5
AMOUNT_CARDS_ON_DECK_MIN = 0
AMOUNT_LEVELS_MAX = 9999
AMOUNT_OPPONENTS_CONCURRENT = 1
AMOUNT_ACTORS_MAX = 9999
# ACTOR FLAGS
LOADING_LEVEL_CONTINIOUS = True

# ### LOCAL GAMERULES ### #
# ACTOR FLAGS
CARDS_ALL = 0b1
CARDS_ONLY_TYPE_ATTACK = 0b10
CARDS_ONLY_TYPE_DEFENSE = 0b100
# ...
CHARACTERS_ALL = 0b1000
CHARACTERS_ONLY_WARRIOR = 0b10000
# ...


class gmEndless():
    def __init__(self, id: int, actor_types: list[str], renderer: "Renderer"):
        self.id = id
        self.name = "GAMEMODE-DEBUG"
        self.ecso_context = ECSO_Context()  # ECS_Context pro game mode
        self.renderer = renderer

        # ### FACTORIES ### #
        self.actor_factories: dict[str, Any] = {}
        for actor_type in actor_types:
            try:
                # Initialises the keys. Maybe unecessary
                match actor_type:
                    case "CARDS":
                        self.actor_factories[actor_type] = CardFactory(self.ecso_context)
                    case "CHARACTERS":
                        self.actor_factories[actor_type] = CharacterFactory(self.ecso_context)
                    case "LEVELS":
                        self.actor_factories[actor_type] = LevelFactory(self.ecso_context)
            except IndexError as e:
                print(f"[GAMEMODE] Factory not found: {e}")
        # ### FACTORIES ### #

        # ### ACTOR CONTEXT ### #
        # "CHARACTERS", LEVELS
        # Currently used..
        self.characters = []
        self.levels = []
        # ### ACTOR CONTEXT ### #

        # ### STACKS ### #
        self.card_stacks: dict[str, list] = {}

        # ### STACKS ### #

        # ### GAME STATES ### #
        self.is_started = False
        self.is_finished = False
        # ### GAME STATES ### #

    def initialise(self, selected_character: int, flags: int) -> bool:
        # ### Generate all character classes and at selected
        self.actor_factories["CHARACTERS"].fabricate_all()
        self.characters.append(self.ecso_context.get_object("CHARACTERS", selected_character))

        # ### Generate all card entities ### #
        self.actor_factories["CARDS"].fabricate_all()

        # ### Generate stacks: Draw stack, Hand (stack) ### #
        self.__create_stacks()

        # ### Generate a level to start the game with
        self.actor_factories["LEVELS"].generate_level()
        self.levels.append(self.ecso_context.get_object("LEVELS", 5))

        self.is_started = True
        return True

    def __create_stacks(self) -> None:
        # ### DRAW STACK ### #
        # Stack where cards are drawn from after each round
        # TIER-0 IMPLEMENTATION: Stack composition with cards only listed in chararcter object
        stack_name = "DRAW"
        if stack_name not in self.card_stacks:
            self.card_stacks[stack_name] = []

        stack_composition = self.characters[0].get_stack_composition()
        temporary_index = 0
        for card in stack_composition:
            if temporary_index % 2 == 0:  # Skips the card amount (As long as the "stack_composition" stays like this)
                for _ in range(stack_composition[temporary_index + 1]):
                    entity_id = self.ecso_context.get_entity(C_DISPLAY_NAME, card)
                    copied_card = self.actor_factories["CARDS"].copy_entity(entity_id)
                    self.card_stacks["DRAW"].append(copied_card)
                    print("[GAMEMODE] Stack composition with id: ", entity_id)

            temporary_index += 1

        print(self.card_stacks["DRAW"])
        self.card_stacks["DRAW"] = self.shuffle_stack(self.card_stacks["DRAW"], 10)
        print(self.card_stacks["DRAW"])
        # ### DRAW STACK ### #

        # ### HAND STACK ### #
        stack_name = "HAND"
        if stack_name not in self.card_stacks:
            self.card_stacks[stack_name] = []

        # Iterate through all cards in the draw stack
        draw_amount = 5
        for _ in range(draw_amount):
            self.characters[0].add_card_to_hand(self.card_stacks["DRAW"].pop())
        print("[GAMEMODE] Cards drawn from character: ", 0)
        # ### HAND STACK ### #

    def shuffle_stack(self, stack: list, times: int) -> list:
        for _ in range(times):
            random_index_1 = randint(0, len(stack) - 1)
            random_index_2 = randint(0, len(stack) - 1)
            temporary_id = stack[random_index_1]
            stack[random_index_1] = stack[random_index_2]
            stack[random_index_2] = temporary_id
        print("[GAMEMODE] Stack shuffled!")
        return stack

    def create_actors(self, type: str, amount) -> None:
        pass

    def create_specified_actors(self, type: str, amount: int, id: int):
        # TODO: If method is necessary think about the implementation.
        pass

    def get_sprites(self) -> pygame.sprite.Group:
        return self.ecso_context.list_of_sprites

    def update(self) -> None:
        self.levels[0].update()
        self.renderer.add_sprites(self.levels[0].get_sprites())  # Adds all sprites from the active level to the renderers sprite group

        # self.levels[0].environment["BACKGROUND1"][0].rect.x += 1  # Debug
        # self.levels[0].environment["BACKGROUND2"][0].rect.y += 1
