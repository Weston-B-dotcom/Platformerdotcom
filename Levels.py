from DataValues import Constants, Assets
from DataValues.TypeAliases import color_t, str_dict_t
from Platform import Platform
from Interactions import Interaction

class Level:
    def __init__(self, name: str, tags: list[str], platforms: list[Platform], interactions: dict[str, list[Interaction]], background: color_t = Assets.BLACK):
        self.name = name
        self.tags = tags
        self.platforms = platforms
        self.top_collision_interactions = interactions.get("top_collision", [])
        self.bottom_collision_interactions = interactions.get("bottom_collision", [])
        self.side_collision_interactions = interactions.get("side_collision", [])
        self.frame_interactions = interactions.get("frame", [])
        self.background = background
        self.data: str_dict_t = {}

    def to_dict(self) -> str_dict_t:
        return {
            "name": self.name,
            "tags": self.tags,
            "platforms": self.platforms,
            "interactions": {
                "top_collision": [inter.to_dict() for inter in self.top_collision_interactions],
                "bottom_collision": [inter.to_dict() for inter in self.bottom_collision_interactions],
                "side_collision": [inter.to_dict() for inter in self.side_collision_interactions],
                "frame": [inter.to_dict() for inter in self.frame_interactions]
            },
            "background": self.background
        }

    @classmethod
    def from_dict(cls, data: str_dict_t) -> "Level":
        return cls(data["name"], data["tags"], data["platforms"],
        {
            inter_type: [Interaction.from_dict(inter) for inter in inters] for inter_type, inters in data.get("interactions", {})
        }, data["background"])