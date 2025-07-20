from typing import TypeAlias, Any

#region Dictionaries
dictStrAny: TypeAlias = dict[str, Any]
dictStrStr: TypeAlias = dict[str, str]
#endregion

#region Wrappers
Tvec2: TypeAlias = tuple[int, int]
Tcolor: TypeAlias = tuple[int, int, int]
#endregion

#region Info Tuples
platformPoint: TypeAlias = tuple[int, int, int, int, float]
modInfo: TypeAlias = tuple[str, str, str, dictStrStr]
#endregion