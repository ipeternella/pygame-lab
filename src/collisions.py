"""
Module with functions related to detect collisions.
"""

from typing import Dict
from typing import List
from typing import Tuple

from pygame import Rect


def get_collisions(player_rect: Rect, tiles: List[Rect]) -> List[Rect]:
    return [tile for tile in tiles if player_rect.colliderect(tile)]


def move(player_rect: Rect, player_speed: List[int], tiles: List[Rect]) -> Tuple[Rect, Dict[str, bool]]:
    """
    Updates the player's rect (x, y) position by applying its velocity vectory in (x, y) coordinates.
    After updating the position with the speed, collisions are checked in order to reposition the player.
    """
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}

    # x axis handling
    player_rect.x += player_speed[0]
    collisions_tiles_x = get_collisions(player_rect, tiles)

    for tile in collisions_tiles_x:
        if player_speed[0] > 0:
            player_rect.right = tile.left
            collision_types["right"] = True
        else:
            player_rect.left = tile.right
            collision_types["left"] = True

    # y axis handling
    player_rect.y += player_speed[1]
    collisions_tiles_y = get_collisions(player_rect, tiles)

    for tile in collisions_tiles_y:
        if player_speed[1] > 0:
            player_rect.bottom = tile.top
            collision_types["bottom"] = True
        else:
            player_rect.top = tile.bottom
            collision_types["top"] = True

    return player_rect, collision_types
