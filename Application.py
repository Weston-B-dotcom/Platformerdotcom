from DataValues import Constants
from DataValues.TypeAliases import modInfo, dictStrStr
from typing import NamedTuple
from GameInstance import Instance
from Player import Player
from Camera import Camera
from pygame import Rect, Surface, Clock, display
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
        """The screen used in the application."""

        self.manager = manager
        """The manager for the screen in the application."""

        self.clock = clock
        """The clock used in the application."""

        self.delta_time: float = 0
        self.accumulated_time: float = 0

        self.camera: Camera = Camera()

    def StepDeltaTime(self):
        self.delta_time = min(self.clock.tick(Constants.FPS) / 1000, Constants.DELTA_TIME)
        self.accumulated_time += self.delta_time


    class SaveData(NamedTuple):
        name: str
        version: str
        mods: dictStrStr

# Mods have:
#  - ID (str)
#  - Name (str)
#  - Description (str)
#  - Version (str)
#  - Dependencies (dict[str, str])