from typing import Any
from ECSO_Context import ECSO_Context
from Factories.Card_Factory import CardFactory


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
    def __init__(self, id: int, actor_types: list[str]):
        self.id = id
        self.name = "GAMEMODE-DEBUG"
        self.ecso_context = ECSO_Context()  # ECS_Context pro game mode

        # ### FACTORIES ### #
        self.actor_factories: dict[str, Any] = {}
        for actor_type in actor_types:
            try:
                # Initialises the keys. Maybe unecessary
                match actor_type:
                    case "CARDS":
                        self.actor_factories[actor_type] = CardFactory(self.ecso_context)
            except IndexError as e:
                print(f"[GAMEMODE] Factory not found: {e}")
        # ### FACTORIES ### #

        # ### ACTOR CONTEXT ### #
        # "CHARACTERS", LEVELS
        self.object_context: dict[str, list] = {}
        for actor_type in actor_types:
            self.object_context[actor_type] = []  # Initialisation
        # ### ACTOR CONTEXT ### #

        # ### GAME STATES ### #
        self.is_started = False
        self.is_finished = False
        # ### GAME STATES ### #

    def initialise(self, flags: int) -> bool:
        if flags & CARDS_ALL:
            # Bind all cards to the game mode
            self.actor_factories["CARDS"].fabricate_all()

        self.is_started = True
        return True

    def create_actors(self, type: str, amount) -> None:
        pass

    def create_specified_actors(self, type: str, amount: int, id: int):
        # TODO: If method is necessary think about the implementation.
        pass

    def update(self) -> None:
        pass
