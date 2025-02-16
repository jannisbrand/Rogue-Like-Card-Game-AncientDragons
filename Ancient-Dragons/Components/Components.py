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


@dataclass
class C_DISPLAY_NAME():
    """If assigned entities have an accessible name
    """
    value: str = "DEFAULT_NAME"


@dataclass
class C_DISPLAY_TEXT():
    """If assigned entities have an accessible text
    """
    value: str = "DEFAULT_TEXT"


@dataclass
class C_CARD_COSTS():
    value: int = 0


@dataclass
class C_CHARACTER_AFFILIATION():
    """If assigned entities can are bound to another entity or object
    (TODO:)
    """
    value: int = -1


@dataclass
class C_CARD_TYPE():
    """If assigned card entities have an specified type
    """
    value: str = "DEFAULT_TYPE"


@dataclass
class C_IMAGE_PATH():
    """If assigned entities have a path to an exitsting image
    """
    value: str = ""
