from pygame_gui.core import ObjectID

from Application import Application
from Player import Player
from DataValues import Assets, Constants
from pygame import Vector2, Rect
from pygame.gfxdraw import box, rectangle
from pygame_gui.elements import UIButton
from enum import Enum, auto
from typing import Any
import pygame

class ScreenType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    NONE      = auto()
    MAIN_MENU = auto()
    SAVES     = auto()
    MODS      = auto()
    SETTINGS  = auto()
    LEVELS    = auto()
    GAME      = auto()

class Platformer:
    def __init__(self, app: Application|None = None):
        self.running: bool|None = None
        self.app = app
        self.screen: ScreenType = ScreenType.MAIN_MENU
        self.player: Player = Player(100, Constants.SCREEN_HEIGHT - 100)
    
    def run(self):
        while self.running:
            self.app.StepDeltaTime()
            mods: int = pygame.key.get_mods()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.KEYDOWN:
                        match self.screen:
                            case ScreenType.MAIN_MENU:
                                ...
                            case ScreenType.LEVELS:
                                ...
                            case ScreenType.GAME:
                                match event.key:
                                    case pygame.K_UP | pygame.K_w | pygame.K_SPACE:
                                        self.player.jump()

                self.app.manager.process_events(event)

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

            match self.screen:
                case ScreenType.MAIN_MENU:
                    ...
                case ScreenType.LEVELS:
                    ...
                case ScreenType.GAME:
                    self.player.stop()
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        self.player.go_left()
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        self.player.go_right()

            self.app.manager.update(self.app.delta_time)

            self.app.screen.fill(Assets.BLACK)
            level_origin_screen_pos: Vector2 = -self.app.camera.pos

            match self.screen:
                case ScreenType.MAIN_MENU:
                    ...
                case ScreenType.LEVELS:
                    ...
                case ScreenType.GAME:
                    #box(self.app.screen, Rect(level_origin_screen_pos, self.level.size), self.level.background)
                    ...

            self.app.manager.draw_ui(self.app.screen)

            pygame.display.flip()

    def init(self):
        self.app.manager.clear_and_reset()
        self.running = True
        self.app.camera.pos = Vector2(0, 0)

        #region Main Menu UI
        for i, (button_type, func) in enumerate([
            ("Saves", lambda: self.SetScreenMode(ScreenType.SAVES)),
            ("Mods", lambda: self.SetScreenMode(ScreenType.MODS)),
            ("Settings", lambda: self.SetScreenMode(ScreenType.SETTINGS))]):
            UIButton(Rect(20, (i * 200) + 20, Constants.SCREEN_WIDTH - 100, 100), button_type, self.app.manager, object_id=ObjectID(button_type, "@round_big_button"), command= func)
        #endregion

        #region Saves UI

        #endregion

        #region Mods UI
        #endregion

        #region Settings UI
        #endregion

        #region Levels UI
        #endregion

        #region Game UI
        #endregion

        return not self.running, "Game"

    def SetScreenMode(self, screen_mode: ScreenType):
        match self.screen:
            case ScreenType.NONE:
                ...
            case ScreenType.SAVES:
                ...
            case ScreenType.MODS:
                ...
            case ScreenType.SETTINGS:
                ...
        self.screen = screen_mode
        match self.screen:
            case ScreenType.NONE:
                ...
            case ScreenType.SAVES:
                ...
            case ScreenType.MODS:
                ...
            case ScreenType.SETTINGS:
                ...
