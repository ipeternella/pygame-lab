"""
Module with some maps of the levels.
"""

import os
from typing import List

import pygame
from pygame import Rect
from pygame.surface import Surface

from src.player import Player
from src.scrolling import Scroll
from src.settings import ROOT_DIR
from src.settings import TILE_SIZE


def load_level_map(map_name: str, map_assets_folder: str = "assets/maps/") -> List[List[str]]:
    """
    Reads a map level file and transforms it into a matrix of tile strings.
    """
    tile_map: List[List[str]] = []
    level_map_path = ROOT_DIR.joinpath(map_assets_folder, map_name)

    with open(level_map_path) as map_file:
        all_map_data = map_file.read()
        map_rows = all_map_data.split("\n")

        for row in map_rows:
            tile_map.append([tile for tile in row])

    return tile_map


def render_level_map(
    display: Surface, level_images: List[Surface], level_map: List[List[str]], player: Player, scroll: Scroll
) -> List[Rect]:
    """
    Blits all the map tiles on a Pygame's display image (Surface). Also returns a list of rects.
    """
    tile_rects: List[Rect] = []

    y = 0
    for row in level_map:
        x = 0
        for tile in row:

            if tile == "0":
                display.blit(level_images[0], (x * TILE_SIZE - scroll.offset_x, y * TILE_SIZE - scroll.offset_y))

            if tile == "1":
                display.blit(level_images[1], (x * TILE_SIZE - scroll.offset_x, y * TILE_SIZE - scroll.offset_y))

            # for collisions (anything != air) -> we use rects (blitting: images, collision: rects)
            if tile != ".":
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            x += 1

        y += 1

    return tile_rects
