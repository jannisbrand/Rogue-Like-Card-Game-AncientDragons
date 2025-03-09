from typing import Callable
from Characters.Base import Character
from Sprites.Base import Sprite


class PlayerCharacter(Character):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.stack_composition = ["Strike", 15, "Defend", 9, "Pummel", 6]  # TODO: ...Names of cards the draw stack should be made of
        self.card_hand: int  # Id of an CardStack game object
        self.mana: int   # Currency to play cards
        self.gold: int   # Currency to shop

        self.is_alive = True
        self.sprite = Sprite
        self.active_effects = [int]

        self.on_mana_changed = None
        self.on_gold_changed = None
        self.on_card_added = None
        self.on_card_removed = None

    def get_mana(self) -> int:
        return self.mana

    def set_mana(self, value):
        self.mana = value

    def get_gold(self) -> int:
        return self.gold

    def set_gold(self, value):
        self.gold = value

    def get_stack_composition(self) -> list:
        return self.stack_composition

    def set_stack(self, stack: int):
        try:
            self.card_hand = stack
        except AttributeError as e:
            print("[CHARACTER][PLAYER]", e)

    def get_stack(self) -> int:
        try:
            return self.card_hand
        except AttributeError as e:
            print("[CHARACTER][PLAYER]", e)
