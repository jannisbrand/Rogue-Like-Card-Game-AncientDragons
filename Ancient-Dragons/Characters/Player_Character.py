from typing import Callable
from Characters.Base import Character
from Sprites.Base import Sprite


class PlayerCharacter(Character):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.stack_composition = ["Strike", 15, "Defend", 9, "Pummel", 6]  # TODO: ...Names of cards the draw stack should be made of
        self.card_hand: list[int] = []  # Ids of cards in the card stack
        self.mana: int   # Currency to play cards
        self.gold: int   # Currency to shop

        self.is_alive = True
        self.sprite = Sprite
        self.active_effects = [int]

        self.on_mana_changed = Callable
        self.on_gold_changed = Callable
        self.on_card_added = Callable
        self.on_card_removed = Callable

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

    def add_card_to_hand(self, entity: int):
        self.card_hand.append(entity)
        print("[CHARACTER] Card drawn: ", entity)

    def get_cards_on_hand(self) -> list:
        return self.card_hand
