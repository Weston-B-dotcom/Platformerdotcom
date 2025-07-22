# Game Constants
from typing import final
from pygame import Vector2, Rect

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
SCREEN_SIZE: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS: int = 60
DELTA_TIME: float = 1 / FPS
COYOTE_TIME_LIMIT: float = 0.1 # Time player can jump after leaving a platform in seconds

# Player properties
PLAYER_WIDTH: int = 40
PLAYER_HEIGHT: int = 60
PLAYER_SIZE: tuple[int, int] = (PLAYER_WIDTH, PLAYER_HEIGHT)
PLAYER_SPEED: int = 5
JUMP_STRENGTH: int = -15
GRAVITY: float = 0.8

# Game properties
VERSION: str = "0.1.0.0"
"""Major, Minor, Patch, Build"""

# Editor Properties
HANDLE_HALF_SIZE: Vector2 = Vector2(7, 7)
HANDLE_SIZE: Vector2 = HANDLE_HALF_SIZE * 2 + Vector2(1, 1)
ONE_VECTOR: Vector2 = Vector2(1, 1)
ZERO_VECTOR: Vector2 = Vector2(0, 0)