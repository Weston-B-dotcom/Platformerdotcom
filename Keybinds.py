import pygame

class Keybind:
    def __init__(self, mods: int = 0, key: int = 0):
        self.mods = mods
        self.key = key

    def IsValid(self, mods: int, key: int) -> bool:
        return key == self.key and self.mods & mods == self.mods

    def Rebind(self, rebinds: tuple[int|None, int|None]) -> None:
        self.mods = self.mods if rebinds[0] is None else rebinds[0]
        self.key = self.key if rebinds[1] is None else rebinds[1]

class Keybinds:
    UP: Keybind = Keybind(0, pygame.K_UP)

    @staticmethod
    def to_json() -> dict[str, tuple[int, int]]:
        return {
            "up": (Keybinds.UP.mods, Keybinds.UP.key)
        }

    @staticmethod
    def from_json(data: dict[str, tuple[int, int]]) -> None:
        Keybinds.UP.Rebind(data.get("up", [None, None]))
