from Application import Application
from DataValues import Assets, Constants
from pygame import Vector2, Rect
from pygame.gfxdraw import box, rectangle
from enum import Enum, auto
from typing import Any
import pygame

class ScreenType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    MAIN_MENU = auto()
    LEVELS    = auto()
    GAME      = auto()

class Platformer:
    def __init__(self, app: Application|None = None):
        self.running: bool|None = None
        self.app = app
        self.screen: ScreenType = ScreenType.MAIN_MENU
    
    def run(self):
        while self.running:
            self.app.StepDeltaTime()
            mods: int = pygame.key.get_mods()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False

                self.app.manager.process_events(event)

        match self.screen:
            case ScreenType.MAIN_MENU:
                ...
            case ScreenType.LEVELS:
                ...
            case ScreenType.GAME:
                ...

        self.app.manager.update(self.app.delta_time)

        self.app.screen.fill(Assets.BLACK)
        level_origin_screen_pos: Vector2 = -self.app.camera.pos
        #box(self.app.screen, Rect(level_origin_screen_pos, self.level.size), self.level.background)
        match self.screen:
            case ScreenType.MAIN_MENU:
                ...
            case ScreenType.LEVELS:
                ...
            case ScreenType.GAME:
                ...

        self.app.manager.draw_ui(self.app.screen)

        pygame.display.flip()

    def init(self):
        ...