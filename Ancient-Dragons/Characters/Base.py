import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, id: int, name: str, image: pygame.Surface):
        self.id = id    # ID
        self.name = name    # Name of the character
        self.image = image
        self.card_entities: set[int]    # Collection of usable cards
        self.health_points: int  # Currency for life
        self.mana_points: int   # Currency to play cards
        self.gold_points: int   # Currency to shop

    def get_image(self) -> pygame.Surface:
        return self.image

    def get_health_points(self) -> int:
        return self.health_points

    def get_mana_points(self) -> int:
        return self.mana_points

    def get_gold_points(self) -> int:
        return self.gold_points
    
    def update(self) -> None:
        # E.G.:
        # Moving image
        # Accessing Cards via ECS context
        # 
        pass
