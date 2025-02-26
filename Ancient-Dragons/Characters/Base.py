import pygame


class Character():
    def __init__(self, id: int, name: str, image: pygame.Surface):
        self.id = id    # ID
        self.name = name    # Name of the character
        self.image = image
        self.stack_composition = ["Strike", 15, "Defend", 9, "Pummel", 6]  # TODO: ...Names of cards the draw stack should be made of
        self.card_hand: list[int] = []  # Ids of cards in the card stack
        self.health_points: int  # Currency for life
        self.mana_points: int   # Currency to play cards
        self.gold_points: int   # Currency to shop

    def get_name(self) -> str:
        return self.name

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_health_points(self) -> int:
        return self.health_points

    def get_mana_points(self) -> int:
        return self.mana_points

    def get_gold_points(self) -> int:
        return self.gold_points

    def get_stack_composition(self) -> list:
        return self.stack_composition

    def add_card_to_hand(self, entity: int):
        self.card_hand.append(entity)
        print("[CHARACTER] Card drawn: ", entity)

    def get_hand(self) -> list:
        return self.card_hand

    def update(self) -> None:
        # E.G.:
        # Moving image
        # Accessing Cards via ECS context
        # 
        pass
