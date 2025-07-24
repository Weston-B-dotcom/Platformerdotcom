from DataValues.TypeAliases import dictStrAny, dictStrStr

class Instance:
    """Description

    Args:
        name (str): The name of the game instance.
        mods (dict[str, str]): The key is the ID of the mod, and the value is the version last used in the game instance.
        version (str): The version of the game that the instance was last loaded in.
        data (str_dict_t): Persistent data used by the game instance.
    """
    def __init__(self, name: str, mods: dictStrStr, version: str, data: dictStrAny):
        self.name = name
        self.mods = mods
        self.version = version
        self.data = data
        self.stages: dict[str, int] = {}
        self.start_level: str = ""
        self.current_level: str = ""

    def load_mods(self):
        # TODO: Implement This.
        ...

    def load_stages(self):
        ...

    def SetStage(self, stage_id: str, checkpoint: int = 0):
        ...

    def to_json(self):
        return {
            "name": self.name,
            "mods": self.mods,
            "version": self.version,
            "data": self.data
        }

    @classmethod
    def from_json(cls, data: dictStrAny):
        return cls(data["name"], data["mods"], data["version"], data["data"])

# Needs to know:
#  - Mods loaded with, and versions (dict[str, str])
#  - Persistant Save Data (str_dict_t)
#  - All loaded stages (Loaded by mods)
#  - Version of game (str)

# Mods have:
#  - ID (str)
#  - Name (str)
#  - Description (str)
#  - Version (str)
#  - Dependencies (dict[str, str])