from GameInstance import Instance
from Player import Player
from Levels import Level
from Interaction import Interaction, InteractionType, DataType, OperatorType, BinaryType, UnaryType
from typing import Any
from pygame import Rect, Color, Vector2
from dataclasses import dataclass
import math

@dataclass
class ReturnWrapper:
    data: Any

def parseOperation(interaction: Interaction, instance: Instance, player: Player, level: Level):
    """Description

    Args:
        interaction (Interaction): description
        instance (Instance): description
        player (Player): description
        level (Level): description
    """
    match OperatorType(interaction.data["operator_type"]):
        case OperatorType.UNARY:
            match UnaryType(interaction.data["operator"]):
                case UnaryType.NOT:
                    return not parseInteraction(interaction.args[0], instance, player, level)
                case UnaryType.ABS:
                    return abs(parseInteraction(interaction.args[0], instance, player, level))
                case UnaryType.FLOOR:
                    return math.floor(parseInteraction(interaction.args[0], instance, player, level))
                case UnaryType.CEIL:
                    return math.ceil(parseInteraction(interaction.args[0], instance, player, level))
                case UnaryType.ROUND:
                    return round(parseInteraction(interaction.args[0], instance, player, level))
        case OperatorType.BINARY:
            match BinaryType(interaction.data["operator"]):
                case BinaryType.EQUAL:
                    return parseInteraction(interaction.args[0], instance, player, level) == parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.NOT_EQUAL:
                    return parseInteraction(interaction.args[0], instance, player, level) != parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.GREATER:
                    return parseInteraction(interaction.args[0], instance, player, level) > parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.LESSER:
                    return parseInteraction(interaction.args[0], instance, player, level) < parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.EQUAL_GREATER:
                    return parseInteraction(interaction.args[0], instance, player, level) >= parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.EQUAL_LESSER:
                    return parseInteraction(interaction.args[0], instance, player, level) <= parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.AND:
                    return parseInteraction(interaction.args[0], instance, player, level) and parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.OR:
                    return parseInteraction(interaction.args[0], instance, player, level) or parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.ADD:
                    return parseInteraction(interaction.args[0], instance, player, level) + parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.SUBTRACT:
                    return parseInteraction(interaction.args[0], instance, player, level) - parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.MULTIPLY:
                    return parseInteraction(interaction.args[0], instance, player, level) * parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.DIVIDE:
                    return parseInteraction(interaction.args[0], instance, player, level) / parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.POW:
                    return math.pow(parseInteraction(interaction.args[0], instance, player, level), parseInteraction(interaction.args[1], instance, player, level))
                case BinaryType.MOD:
                    return parseInteraction(interaction.args[0], instance, player, level) % parseInteraction(interaction.args[1], instance, player, level)
                case BinaryType.MIN:
                    return min(parseInteraction(interaction.args[0], instance, player, level), parseInteraction(interaction.args[1], instance, player, level))
                case BinaryType.MAX:
                    return max(parseInteraction(interaction.args[0], instance, player, level), parseInteraction(interaction.args[1], instance, player, level))
            ...
    return None

def parseLiteral(interaction: Interaction, instance: Instance, player: Player, level: Level):
    """Description

    Args:
        interaction (Interaction): description
        instance (Instance): description
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

def parseConditional(interaction: Interaction, instance: Instance, player: Player, level: Level) -> None:
    """Description

    Args:
        interaction (Interaction): description
        instance (Instance): description
        player (Player): description
        level (Level): description
    """
    if parseInteraction(interaction.args[0], instance, player, level):
        return parseInteraction(interaction.args[1], instance, player, level)
    else:
        return parseInteraction(interaction.args[2], instance, player, level)

def parseBlock(interaction: Interaction, instance: Instance, player: Player, level: Level):
    for inter in interaction.args:
        evaluated = parseInteraction(inter, instance, player, level)
        if isinstance(evaluated, ReturnWrapper):
            return evaluated.data
    return None

def parseInteraction(interaction: Interaction, instance: Instance, player: Player, level: Level):
    """Description

    Args:
        interaction (Interaction): description
        instance (Instance): description
        player (Player): description
        level (Level): description
    """
    match interaction.interaction_type:
        case InteractionType.set_value:
            match interaction.data["mode"]:
                case "local":
                    level.data[interaction.data["key"]] = parseInteraction(interaction.args[0], instance, player, level)
                case "global":
                    instance.data[interaction.data["key"]] = parseInteraction(interaction.args[0], instance, player, level)
            return None
        case InteractionType.get_value:
            match interaction.data["mode"]:
                case "local":
                    return level.data[interaction.data["key"]]
                case "global":
                    return instance.data[interaction.data["key"]]
            return None
        case InteractionType.set_stage:
            instance.current_level = parseInteraction(interaction.args[0], instance, player, level)
            return None
        case InteractionType.get_stage:
            return level.name
        case InteractionType.get_player:
            return player
        case InteractionType.get_platform:
            return level.platforms[interaction.data["platform_id"]]
        case InteractionType.set_field:
            setattr(parseInteraction(interaction.args[0], instance, player, level), interaction.data["field"], parseInteraction(interaction.args[1], instance, player, level))
            return None
        case InteractionType.get_field:
            return getattr(parseInteraction(interaction.args[0], instance, player, level), interaction.data["field"])
        case InteractionType.operation:
            return parseOperation(interaction, instance, player, level)
        case InteractionType.literal_value:
            return parseLiteral(interaction, instance, player, level)
        case InteractionType.call_method:
            eval(f'''return getattr(parseInteraction(interaction.args[0], instance, player, level), interaction.data["method"])({", ".join([str(parseInteraction(interaction.args[i], instance, player, level)) for i in range(1, len(interaction.args))])})''')
        case InteractionType.conditional:
            return parseConditional(interaction, instance, player, level)
        case InteractionType.block:
            return parseBlock(interaction, instance, player, level)
        case InteractionType.return_statement:
            return ReturnWrapper(parseInteraction(interaction.args[0], instance, player, level))
        case InteractionType.none:
            return None