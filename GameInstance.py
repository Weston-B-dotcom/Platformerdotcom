from DataValues.TypeAliases import str_dict_t

class Instance:
    """Description

    Args:
        mods (dict[str, str]): The key is the id of the mod, and the value is the version last used in the game instance.
        version (str): The version of the game that the instance was last loaded in.
        data (str_dict_t): Persistent data used by the game instance.
    """
    def __init__(self, mods: dict[str, str], version: str, data: str_dict_t):
        self.mods = mods
        self.version = version
        self.data = data


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