from DataValues.TypeAliases import modInfo, dictStrStr
from typing import NamedTuple
from GameInstance import Instance
from Player import Player
from pygame import Rect, Surface, Clock
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UILabel, UIScrollingContainer, UIButton, UITextBox, UITextEntryLine, UIStatusBar

class Application:
    """Definition

    Args:
        version (str): The version of the application.
        screen (Surface): The screen of the display.
        manager (UIManager): The UIManager used by the game.
        clock (Clock): The clock to use.
    """
    def __init__(self, version: str, screen: Surface, manager: UIManager, clock: Clock):
        self.mods: dict[str, modInfo] = {}
        """The ID of the mods correlating to the Name, Description, Version, and Dependencies respectively."""

        self.version = version
        """The version of the application."""

        self.game_instance: Instance
        self.player: Player

        self.screen = screen
        """"""
        self.manager = manager
        """"""
        self.clock = clock
        """"""

        self.delta_time: float = 0
        self.accumulated_time: float = 0

    class SaveData(NamedTuple):
        name: str
        version: str
        mods: dictStrStr

# List of saves
#

# name: str, mods: dict[str, str], version: str

# Mods (All their info, whether they are enabled/disabled, etc)
# Configuration settings?
#

# Mods have:
#  - ID (str)
#  - Name (str)
#  - Description (str)
#  - Version (str)
#  - Dependencies (dict[str, str])