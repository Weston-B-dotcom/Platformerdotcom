from DataValues.TypeAliases import vec2_t, color_t, platform_point_t, str_dict_t
import pygame, json, enum

# --- Platform Class ---
class Behaviors(enum.Enum):
    none = 0
    reverse = 1
    snap = 2

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos: vec2_t, size: vec2_t, color: color_t, points: list[platform_point_t] = None, behavior: Behaviors = Behaviors.none):
        super().__init__()
        self.color = color
        self.points: list[platform_point_t] = [] if points is None else points
        self.behavior = behavior
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def to_dict(self) -> str_dict_t:
        return {
            'pos': self.rect.topleft,
            'size': self.rect.size,
            'color': self.color,
            'points': self.points,
            'behavior': self.behavior.value
        }

    @classmethod
    def from_dict(cls, data: str_dict_t) -> "Platform":
        return cls(data['pos'], data['size'], data['color'], data['points'], Behaviors(data['behavior']))