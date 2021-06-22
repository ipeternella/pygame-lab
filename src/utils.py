"""
Module with some utilities.
"""
import os

import pygame
from pygame.surface import Surface

from src.settings import ROOT_DIR


def load_image_asset(image_path: str, assets_dir="assets/") -> Surface:
    """
    Loads an image from disk with Pygame. Returns a pygame Surface.
    """
    img_asset_path = ROOT_DIR.joinpath(assets_dir, image_path)

    return pygame.image.load(img_asset_path)
