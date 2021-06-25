"""
Module with the main game loop.
"""

import pygame
from pygame.surface import Surface
from pygame.time import Clock

from src.animations import SpriteSheetParser
from src.collisions import move
from src.exit import exit_if_captured_quit
from src.inputs import capture_player_inputs
from src.maps import TiledMap
from src.player import Player
from src.scrolling import Scroll
from src.settings import CLEAR_DISPLAY_RGB
from src.settings import GAME_FPS
from src.settings import RAW_DISPLAY_SIZE
from src.settings import WINDOW_SIZE
from src.settings import WINDOW_TITLE


def main():
    """
    Entry point which runs the main game loop.
    """

    pygame.init()
    game_clock = Clock()

    # main screen
    game_screen: Surface = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    pygame.display.set_caption(WINDOW_TITLE)

    # raw_display is the main blit Surface which is scaled later
    raw_display = pygame.Surface(RAW_DISPLAY_SIZE)

    # images
    tiled_level_01 = TiledMap("tiled-level-01.tmx")
    spritesheet_parser = SpriteSheetParser()

    # loading player's spritesheets
    spritesheet_parser.load_spritesheet("hero")
    player_animations = spritesheet_parser.build_animation_repository()

    # player
    player = Player(10, 10, player_animations)
    scroll = Scroll(0.0, 0.0)

    # main game loop
    while True:
        raw_display.fill(CLEAR_DISPLAY_RGB)  # clears the display

        scroll.update(player.rect.x, player.rect.y)  # update scrolling according to last player's updated position
        tile_rects = tiled_level_01.render(raw_display, scroll)

        # input capturing
        captured_input = capture_player_inputs()

        # input handling by entities (updating)
        exit_if_captured_quit(captured_input)
        player.update(captured_input)
        move(player.rect, player.speed, tile_rects)  # update player + collisions

        # scale display is what is blit on the game screen
        raw_display.blit(player.image, (player.rect.x - scroll.offset_x, player.rect.y - scroll.offset_y))
        scaled_display = pygame.transform.scale(raw_display, WINDOW_SIZE)
        game_screen.blit(scaled_display, (0, 0))

        pygame.display.update()
        game_clock.tick(GAME_FPS)


if __name__ == "__main__":
    main()
