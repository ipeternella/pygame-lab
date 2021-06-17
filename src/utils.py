"""
Module with some utilities.
"""
import os

import pygame
from pygame.surface import Surface

from src.settings import ASSETS_DIR


def load_image_asset(image_path: str) -> Surface:
    """
    Loads an image from disk with Pygame that is relative to the ASSETS_DIR.
    """
    return pygame.image.load(os.path.join(ASSETS_DIR, image_path))
