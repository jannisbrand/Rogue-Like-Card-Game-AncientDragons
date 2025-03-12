from typing import Any

from Scenes.Scene import Scene


class SceneHandler():
    def __init__(self):
        self.active_gamemode: int  # Index
        self.gamemodes: list[Any]

    def initialise(self) -> None:
        self.active_gamemode = -1
        self.gamemodes = []

    def add_gamemode(self, gamemode: Any) -> None:
        self.gamemodes.append(gamemode)
        if len(self.gamemodes) == 1:
            self.active_gamemode = 0

    def load_gamemode(self, index: int) -> None:
        self.active_gamemode = index
        gamemode = self.gamemodes[index]
        gamemode.initialise()  # TODO: TEMPORARYYYY

    def __get_gamemode_by_name(self, name: str) -> int:
        try:
            index = 0
            for gamemode in self.gamemodes:
                if gamemode.name == name:
                    return index
                index += 1
            print(f"No gamemode found: {name}")
            return self.active_gamemode
        except AttributeError as e:
            print(f"No gamemode found: {e}")
            return self.active_gamemode

    def update(self) -> None:
        gamemode = self.gamemodes[self.active_gamemode]
        # gamemode.entity_update()
        gamemode.update()
        gamemode.update_entities()
        if gamemode.is_finished:
            match gamemode.next_gamemode:
                case "START":
                    self.load_gamemode(self.__get_gamemode_by_name("START"))
                case "ENDLESS":
                    self.load_gamemode(self.__get_gamemode_by_name("ENDLESS"))
