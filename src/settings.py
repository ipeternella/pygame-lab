"""
Settings used by the game.
"""
from pathlib import Path
from typing import Tuple

ROOT_DIR: Path = Path(__file__).resolve().parent.parent  # root of the project (same level as 'src')

WINDOW_TITLE = "Pygame Lab!"
WINDOW_SIZE: Tuple[int, int] = (600, 400)
RAW_DISPLAY_SIZE: Tuple[int, int] = (300, 200)
CLEAR_DISPLAY_RGB: Tuple[int, int, int] = (128, 163, 224)
GAME_FPS = 60
TILE_SIZE = 16

# gameplay
GRAVITY = 1
JUMP_VELOCITY_Y = 15

# scrolling (gives smooth scrolling effect) -> set 1 for simple scrolling
SCROLLING_OFFSET_FRACTION = 0.05

# maps tags
TMX_OBJECT_PLAYER_NAME = "player"
TMX_OBJECT_COLLIDABLE_NAME = "collidable"
