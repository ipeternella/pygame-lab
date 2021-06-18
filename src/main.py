import os
import sys

# flake8: noqa E402 (top-level import)
main_path = os.path.dirname(__file__)
sys.path.append(os.path.join(main_path, ".."))

import pygame
from pygame.surface import Surface
from pygame.time import Clock

from src.collisions import move
from src.exit import game_over
from src.inputs import capture_player_inputs
from src.maps import LEVEL_MAP_01
from src.maps import render_level_map
from src.player import Player
from src.settings import GAME_FPS
from src.settings import WINDOW_SIZE
from src.settings import WINDOW_TITLE
from src.utils import load_image_asset


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

    # player
    player = Player(50, 50, player_img)

    # main game loop
    while True:
        raw_display.fill((146, 244, 255))  # clears the display
        tile_rects = render_level_map(raw_display, [grass_img, dirt_img], LEVEL_MAP_01)

        # input capturing
        captured_input = capture_player_inputs()

        # input handling by entities (updating)
        game_over(captured_input)
        player.update(captured_input)

        # moving and collisions
        move(player.rect, player.speed, tile_rects)

        # scale display is what is blit on the game screen
        raw_display.blit(player_img, (player.rect.x, player.rect.y))
        scaled_display = pygame.transform.scale(raw_display, WINDOW_SIZE)
        game_screen.blit(scaled_display, (0, 0))

        pygame.display.update()
        game_clock.tick(GAME_FPS)


if __name__ == "__main__":
    main()
