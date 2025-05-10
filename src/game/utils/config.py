"""
Game configuration and constants.
"""
from typing import Final, Dict, Tuple
import os
from pathlib import Path

# Screen Configuration
SCREEN_WIDTH: Final[int] = 800
SCREEN_HEIGHT: Final[int] = 600
FPS: Final[int] = 60

# Directory Paths
ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent.parent
ASSETS_DIR: Final[Path] = ROOT_DIR / "assets"
BG_ASSETS_DIR: Final[Path] = ASSETS_DIR / "backgrounds"
SPRITE_ASSETS_DIR: Final[Path] = ASSETS_DIR / "sprites"

# Game Physics
GRAVITY: Final[float] = 0.8
JUMP_SPEED: Final[float] = -15
MOVE_SPEED: Final[float] = 5

# Colors
COLORS: Final[Dict[str, Tuple[int, int, int]]] = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0)
}

# Game States
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

# Score Configuration
COIN_VALUE: Final[int] = 10
HIGH_SCORE_FILE: Final[Path] = ROOT_DIR / "highscores.json"

def get_asset_path(filename: str) -> Path:
    """Get the full path for an asset file."""
    return ASSETS_DIR / filename

def get_background_path(filename: str) -> Path:
    """Get the full path for a background asset."""
    return BG_ASSETS_DIR / filename

def get_sprite_path(filename: str) -> Path:
    """Get the full path for a sprite asset."""
    return SPRITE_ASSETS_DIR / filename 