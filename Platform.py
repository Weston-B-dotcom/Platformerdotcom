from DataValues.TypeAliases import Tvec2, Tcolor, platformPoint, dictStrAny
from pygame.sprite import Sprite
import pygame, json, enum

# --- Platform Class ---
class Behaviors(enum.Enum):
    none = 0
    reverse = 1
    snap = 2

class Platform(Sprite):
    def __init__(self, pos: Tvec2, size: Tvec2, color: Tcolor, points: list[platformPoint] = None, behavior: Behaviors = Behaviors.none):
        super().__init__()
        self.color = color
        self.points: list[platformPoint] = [] if points is None else points
        self.behavior = behavior
        self.image: pygame.Surface = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def Resize(self, new_size: pygame.Vector2):
        self.image = pygame.Surface(new_size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def to_dict(self) -> dictStrAny:
        return {
            'pos': self.rect.topleft,
            'size': self.rect.size,
            'color': self.color,
            'points': self.points,
            'behavior': self.behavior.value
        }

    @classmethod
    def from_dict(cls, data: dictStrAny) -> "Platform":
        return cls(data['pos'], data['size'], data['color'], data['points'], Behaviors(data['behavior']))