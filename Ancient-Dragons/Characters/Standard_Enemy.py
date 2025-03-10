

from Characters.Base import Character


class StandardEnemy(Character):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.attack_damage = 0

    def set_attack_damage(self, value: int):
        try:
            self.attack_damage = value
        except ValueError as e:
            print("[ENEMY][DATA]", e)
        except AttributeError as e:
            print("[ENEMY][DATA]", e)

    def get_attack_damage(self) -> int:
        try:
            return self.attack_damage
        except AttributeError as e:
            print("[ENEMY][DATA]", e)
