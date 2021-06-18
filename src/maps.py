"""
Module with some maps of the levels.
"""

from typing import List

import pygame
from pygame import Rect
from pygame.surface import Surface

from src.settings import TILE_SIZE

LEVEL_MAP_01 = [
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "2", "2", "2", "2", "2", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2", "2"],
    ["1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
]


def render_level_map(display: Surface, level_images: List[Surface], level_map: List[List[str]]) -> List[Rect]:
    """
    Blits all the map tiles on a Pygame's display image (Surface). Also returns a list of rects.
    """
    tile_rects: List[Rect] = []
    grass_img = level_images[0]
    dirt_img = level_images[1]

    y = 0
    for row in level_map:
        x = 0
        for tile in row:
            if tile == "1":
                display.blit(dirt_img, (x * TILE_SIZE, y * TILE_SIZE))

            if tile == "2":
                display.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))

            # for collisions (anything != air) -> we use rects (blitting: images, collision: rects)
            if tile != "0":
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            x += 1

        y += 1

    return tile_rects
