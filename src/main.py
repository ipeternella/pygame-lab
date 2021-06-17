import os
import sys

# flake8: noqa E402 (top-level import)
main_path = os.path.dirname(__file__)
sys.path.append(os.path.join(main_path, ".."))

from typing import List

import pygame
from pygame import Rect
from pygame import time
from pygame.surface import Surface
from pygame.time import Clock

from src.inputs import capture_player_inputs
from src.player import Player
from src.settings import GAME_FPS
from src.settings import WINDOW_SIZE
from src.settings import WINDOW_TITLE
from src.utils import load_image_asset

TILE_SIZE = load_image_asset("img/grass.png").get_width()

# map
game_map = [
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
    ["2", "2", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "2", "2"],
    ["1", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "2", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
]


def main():
    pygame.init()
    game_clock = Clock()

    # main screen
    game_screen: Surface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    pygame.display.set_caption(WINDOW_TITLE)

    # raw_display is the main blit Surface which is scaled later
    raw_display = pygame.Surface((300, 200))

    # images
    grass_img = load_image_asset("img/grass.png")
    dirt_img = load_image_asset("img/dirt.png")
    player_img = load_image_asset("img/hero.png")
    # player_img.set_colorkey((255, 255, 255))  # color key sets the pixel color to be transparent
    player = Player(50, 50, player_img)

    # main game loop
    while True:
        raw_display.fill((146, 244, 255))
        raw_display.blit(player_img, (player.rect.x, player.rect.y))

        # map processing
        tile_rects: List[Rect] = []

        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == "1":
                    raw_display.blit(dirt_img, (x * TILE_SIZE, y * TILE_SIZE))

                if tile == "2":
                    raw_display.blit(grass_img, (x * TILE_SIZE, y * TILE_SIZE))

                if tile != "0":  # for collisions (anything != air)
                    tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                x += 1

            y += 1

        # input capturing
        captured_inputs = capture_player_inputs()

        # input handling by entities
        if captured_inputs.should_quit:
            pygame.quit()
            sys.exit(0)

        player.update(captured_inputs)

        # scale display is what is blit on the game screen
        scaled_display = pygame.transform.scale(raw_display, WINDOW_SIZE)
        game_screen.blit(scaled_display, (0, 0))

        pygame.display.update()
        game_clock.tick(GAME_FPS)


if __name__ == "__main__":
    main()
