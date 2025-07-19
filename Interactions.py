from unittest import case

from DataValues.TypeAliases import str_dict_t
from Player import Player
from Levels import Level
from enum import Enum, auto
from typing import Any
from pygame import Rect, Color, Vector2
from dataclasses import dataclass
from operator import xor
import pygame, math

@dataclass
class ReturnWrapper:
    data: Any

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

a = pygame.Rect(0, 0, 12, 10)
a.colliderect(pygame.Rect(0, 0, 43, 53))

class Interaction:
    def __init__(self, interaction_type: InteractionType, args: list["Interaction"], data: str_dict_t):
        self.interaction_type = interaction_type
        self.args = args
        self.data = data

    def to_dict(self) -> str_dict_t:
        return {
            "interaction_type": self.interaction_type.name,
            "args": [arg.to_dict() for arg in self.args],
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data: str_dict_t) -> "Interaction":
        return cls(InteractionType(data["interaction_type"]), [Interaction.from_dict(arg) for arg in data.get("args", [])], data.get("data", {}))

def parseOperation(interaction: Interaction, player: Player, level: Level) -> bool:
    """Description

    Args:
        interaction (Interaction): description
        player (Player): description
        level (Level): description
    """
    match OperatorType(interaction.data["operator_type"]):
        case OperatorType.UNARY:
            match UnaryType(interaction.data["operator"]):
                case UnaryType.NOT:
                    return not parseInteraction(interaction.args[0], player, level)
                case UnaryType.ABS:
                    return abs(parseInteraction(interaction.args[0], player, level))
                case UnaryType.FLOOR:
                    return math.floor(parseInteraction(interaction.args[0], player, level))
                case UnaryType.CEIL:
                    return math.ceil(parseInteraction(interaction.args[0], player, level))
                case UnaryType.ROUND:
                    return round(parseInteraction(interaction.args[0], player, level))
        case OperatorType.BINARY:
            match BinaryType(interaction.data["operator"]):
                case BinaryType.EQUAL:
                    return parseInteraction(interaction.args[0], player, level) == parseInteraction(interaction.args[1], player, level)
                case BinaryType.NOT_EQUAL:
                    return parseInteraction(interaction.args[0], player, level) != parseInteraction(interaction.args[1], player, level)
                case BinaryType.GREATER:
                    return parseInteraction(interaction.args[0], player, level) > parseInteraction(interaction.args[1], player, level)
                case BinaryType.LESSER:
                    return parseInteraction(interaction.args[0], player, level) < parseInteraction(interaction.args[1], player, level)
                case BinaryType.EQUAL_GREATER:
                    return parseInteraction(interaction.args[0], player, level) >= parseInteraction(interaction.args[1], player, level)
                case BinaryType.EQUAL_LESSER:
                    return parseInteraction(interaction.args[0], player, level) <= parseInteraction(interaction.args[1], player, level)
                case BinaryType.AND:
                    return parseInteraction(interaction.args[0], player, level) and parseInteraction(interaction.args[1], player, level)
                case BinaryType.OR:
                    return parseInteraction(interaction.args[0], player, level) or parseInteraction(interaction.args[1], player, level)
                case BinaryType.ADD:
                    return parseInteraction(interaction.args[0], player, level) + parseInteraction(interaction.args[1], player, level)
                case BinaryType.SUBTRACT:
                    return parseInteraction(interaction.args[0], player, level) - parseInteraction(interaction.args[1], player, level)
                case BinaryType.MULTIPLY:
                    return parseInteraction(interaction.args[0], player, level) * parseInteraction(interaction.args[1], player, level)
                case BinaryType.DIVIDE:
                    return parseInteraction(interaction.args[0], player, level) / parseInteraction(interaction.args[1], player, level)
                case BinaryType.POW:
                    return math.pow(parseInteraction(interaction.args[0], player, level), parseInteraction(interaction.args[1], player, level))
                case BinaryType.MOD:
                    return parseInteraction(interaction.args[0], player, level) % parseInteraction(interaction.args[1], player, level)
                case BinaryType.MIN:
                    return min(parseInteraction(interaction.args[0], player, level), parseInteraction(interaction.args[1], player, level))
                case BinaryType.MAX:
                    return max(parseInteraction(interaction.args[0], player, level), parseInteraction(interaction.args[1], player, level))
            ...
    return None

def parseLiteral(interaction: Interaction, player: Player, level: Level):
    """Description

    Args:
        interaction (Interaction): description
        player (Player): description
        level (Level): description
    """
    match DataType(interaction.data["type"]):
        case DataType.STRING:
            return interaction.data["value"]
        case DataType.INTEGER:
            return int(interaction.data["value"])
        case DataType.BOOLEAN:
            return bool(interaction.data["value"])
        case DataType.REAL:
            return float(interaction.data["value"])
        case DataType.RECT:
            return Rect(interaction.data["value"])
        case DataType.VEC2:
            return Vector2(interaction.data["value"])
        case DataType.COLOR:
            return Color(interaction.data["value"])
    return None

def parseConditional(interaction: Interaction, player: Player, level: Level) -> None:
    """Description

    Args:
        interaction (Interaction): description
        player (Player): description
        level (Level): description
    """
    if parseInteraction(interaction.args[0], player, level):
        return parseInteraction(interaction.args[1], player, level)
    else:
        return parseInteraction(interaction.args[2], player, level)

def parseBlock(interaction: Interaction, player: Player, level: Level):
    for inter in interaction.args:
        evaluated = parseInteraction(inter, player, level)
        if isinstance(evaluated, ReturnWrapper):
            return evaluated.data
    return None

def parseInteraction(interaction: Interaction, player: Player, level: Level):
    """Description

    Args:
        interaction (Interaction): description
        player (Player): description
        level (Level): description
    """
    match interaction.interaction_type:
        case InteractionType.set_value:
            level.data[interaction.data["key"]] = parseInteraction(interaction.args[0], player, level)
            return None
        case InteractionType.get_value:
            return level.data[interaction.data["key"]]
        case InteractionType.set_stage:
            # TODO: Implement this once the global is in.
            return None
        case InteractionType.get_stage:
            return level.name
        case InteractionType.get_player:
            return player
        case InteractionType.get_platform:
            return level.platforms[interaction.data["platform_id"]]
        case InteractionType.set_field:
            setattr(parseInteraction(interaction.args[0], player, level), interaction.data["field"], parseInteraction(interaction.args[1], player, level))
            return None
        case InteractionType.get_field:
            return getattr(parseInteraction(interaction.args[0], player, level), interaction.data["field"])
        case InteractionType.operation:
            return parseOperation(interaction, player, level)
        case InteractionType.literal_value:
            return parseLiteral(interaction, player, level)
        case InteractionType.call_method:
            eval(f'''return getattr(parseInteraction(interaction.args[0], player, level), interaction.data["method"])({", ".join([str(parseInteraction(interaction.args[i], player, level)) for i in range(1, len(interaction.args))])})''')
        case InteractionType.conditional:
            return parseConditional(interaction, player, level)
        case InteractionType.block:
            return parseBlock(interaction, player, level)
        case InteractionType.return_statement:
            return ReturnWrapper(parseInteraction(interaction.args))
        case InteractionType.none:
            return None