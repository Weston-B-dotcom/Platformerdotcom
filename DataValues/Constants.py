# Game Constants
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
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
