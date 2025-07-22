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
    
    def Tuple(self) -> tuple[int, int]:
        return (self.mods, self.key)

class Keybinds:
    GRID_DECREASE_ONE: Keybind = Keybind(pygame.KMOD_LCTRL, pygame.K_LEFT)
    GRID_INCREASE_ONE: Keybind = Keybind(pygame.KMOD_LCTRL, pygame.K_RIGHT)
    GRID_DECREASE_TEN: Keybind = Keybind(pygame.KMOD_LCTRL & pygame.KMOD_LSHIFT, pygame.K_LEFT)
    GRID_INCREASE_TEN: Keybind = Keybind(pygame.KMOD_LCTRL & pygame.KMOD_LSHIFT, pygame.K_RIGHT)

    @staticmethod
    def to_json() -> dict[str, tuple[int, int]]:
        return {
            key.lower(): value.Tuple() for key, value in Keybinds.__dict__.items() if isinstance(value, Keybind)
        }

    @staticmethod
    def from_json(data: dict[str, tuple[int, int]]) -> None:
        for key, _ in Keybinds.__dict__.items():
            if key.lower() in data:
                Keybinds.__dict__[key].Rebind(data[key.lower()])