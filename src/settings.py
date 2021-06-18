"""
Settings used by the game.
"""
import os
from pathlib import Path
from typing import Tuple

ROOT_DIR: Path = Path(__file__).resolve().parent.parent  # root of the project (same level as 'src')
ASSETS_DIR: Path = os.path.join(ROOT_DIR, "assets/")  # type: ignore

WINDOW_TITLE = "A Pygame window!"
WINDOW_SIZE: Tuple[int, int] = (600, 400)
GAME_FPS = 60

TILE_SIZE = 16
