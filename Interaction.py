from enum import Enum, auto
from typing import Any
from DataValues.TypeAliases import dictStrAny

class InteractionType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    none             = auto()
    set_value        = auto()
    get_value        = auto()
    set_stage        = auto()
    get_stage        = auto()
    get_player       = auto()
    get_platform     = auto()
    set_field        = auto()
    get_field        = auto()
    operation        = auto()
    literal_value    = auto()
    call_method      = auto()
    conditional      = auto()
    block            = auto()
    return_statement = auto()

class DataType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return name.lower()

    STRING  = auto()
    INTEGER = auto()
    BOOLEAN = auto()
    REAL    = auto()
    RECT    = auto()
    VEC2    = auto()
    COLOR   = auto()

class OperatorType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return name.lower()

    UNARY  = auto()
    BINARY = auto()

class UnaryType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return name.lower()

    NOT   = auto()
    ABS   = auto()
    FLOOR = auto()
    CEIL  = auto()
    ROUND = auto()

class BinaryType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return name.lower()

    EQUAL         = auto()
    NOT_EQUAL     = auto()
    GREATER       = auto()
    LESSER        = auto()
    EQUAL_GREATER = auto()
    EQUAL_LESSER  = auto()
    AND           = auto()
    OR            = auto()
    ADD           = auto()
    SUBTRACT      = auto()
    MULTIPLY      = auto()
    DIVIDE        = auto()
    POW           = auto()
    MOD           = auto()
    MIN           = auto()
    MAX           = auto()

class Interaction:
    def __init__(self, interaction_type: InteractionType, args: list["Interaction"], data: dictStrAny):
        self.interaction_type = interaction_type
        self.args = args
        self.data = data

    def to_dict(self) -> dictStrAny:
        return {
            "interaction_type": self.interaction_type.name,
            "args": [arg.to_dict() for arg in self.args],
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data: dictStrAny) -> "Interaction":
        return cls(InteractionType(data["interaction_type"]), [Interaction.from_dict(arg) for arg in data.get("args", [])], data.get("data", {}))
