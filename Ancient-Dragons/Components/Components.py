from dataclasses import dataclass


@dataclass
class C_ATTACK():
    """If assigned damage is applied to a selected opponent
    """
    value: int = 0


@dataclass
class C_DEFENSE():
    """If assigned incoming damage is reduced by its value.
    If damage < value the damage is 0
    """
    value: int = 0
